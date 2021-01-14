# Stock checking window
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QTextBrowser
import stock_checker
from concurrent.futures import ThreadPoolExecutor
import threading
from queue import Queue
from time import sleep
import main_window
from html_parse import get_closing_tag
from playsound import playsound

MAX_CONNECTIONS: int = 100

STOP_CODE: int = 1

IDLE_SLEEP: float = 0.05

OOS_TEXT: str = " is Out of Stock"  # comes after item link
INSTOCK_TEXT: str = " is IN STOCK!!!"

# Style for regular text, out-of-stock text, and in-stock text
OOS_TEXT_SS: str = "<p style='color:red; float:left;'>"
IS_TEXT_SS: str = "<p style='color:green; float:left;'>"

# These tag endings are based on what the tags for the styles are.
OOS_TEXT_END: str = get_closing_tag(OOS_TEXT_SS)
IS_TEXT_END: str = get_closing_tag(IS_TEXT_SS)

OOS_MESSAGE = OOS_TEXT_SS + OOS_TEXT + OOS_TEXT_END
INSTOCK_MESSAGE = IS_TEXT_SS + INSTOCK_TEXT + IS_TEXT_END


class StockWindow(QWidget):
    ''' Stock checking window.\n
    Attributes:\n
    - Title (QLabel): The name of the program at the top of the window. \n
    - StockDisplayBox (QTextBrowser) : Where the log is kept. The log includes when the program stops/starts, and whether the links
    are out of stock or not. \n
    - StartStopButton (QPushButton) : The button which starts/stops the program. \n
    Program also contains a separate worker (worker_thread) which will perform the stock checking loop and edit the StockDisplayBox accordingly
    on a separate thread so as to keep the PyQt event loop running.
    '''

    def __init__(self, links: list, sleepTime: float) -> None:
        self.links = links
        self.sleepTime = sleepTime
        # Stock Checking event loop control variables
        super().__init__()
        self.createUI()
        self.thread_init()

    def thread_init(self):
        ''' Initializes the necessary variables and worker thread to run the stock checking event loop.'''
        self.should_continue = True
        self.should_not_stop = True
        self.sleep_interrupt = threading.Event()
        self.queue = Queue(maxsize=0)
        self.work_thread = threading.Thread(target=self.check_stock)
        self.work_thread.start()
        # Since both threads (main & worker) are editing StockDisplayBox at the same time we need a lock
        # to keep it thread-safe (both threads don't access at the same time).
        self.text_lock = threading.Lock()

    def createUI(self) -> None:
        ''' Creates the default UI for the StockWindow.  '''
        self.setWindowTitle("Inventory Inspector")
        self.setGeometry(0, 0, 800, 600)

        # Creating widgets
        self.layout = QVBoxLayout()
        title = QLabel("Inventory Inspector")
        self.StockDisplayBox = QTextBrowser()
        self.StockDisplayBox.setOpenExternalLinks(True)
        self.StockDisplayBox.setOpenLinks(True)
        self.StockDisplayBox.append("Checking links:\n")
        self.StockDisplayBox.setAcceptRichText(True)
        self.StockDisplayBox.setLineWrapMode(QTextEdit.NoWrap)
        self.TextScrollBar = self.StockDisplayBox.verticalScrollBar()
        self.StartStopButton = QPushButton("Stop")
        self.StartStopButton.clicked.connect(self.stop_start)
        # Adding widgets
        self.layout.addWidget(title)
        self.layout.addWidget(self.StockDisplayBox)
        self.layout.addWidget(self.StartStopButton)
        self.setLayout(self.layout)
        self.show()

    def stop_start(self) -> None:
        ''' Stops or starts the stock checking thread depending on the previous state. '''
        if self.StartStopButton.text() == "Start":
            if not self.queue.empty():
                main_window.createAlert("Stock checking has not paused yet. Please wait.")
                return
            self.should_continue = True
            self.sleep_interrupt.clear()
            self.appendToBox("Resumed checking stock.\n")
            self.StartStopButton.setText("Stop")
        else:
            self.queue.put(STOP_CODE)
            self.sleep_interrupt.set()
            self.appendToBox("Pausing...")
            self.StartStopButton.setText("Start")
        return

    def check_stock(self) -> None:
        ''' Checks the stock of the items in self.links and displays the results on the text area corresponding
        to self.StockDisplayBox. \n  '''
        links = self.links
        sleep_time = self.sleepTime
        storemap = {link: stock_checker.get_domain_name(link) for link in links}
        executor = ThreadPoolExecutor(max_workers=MAX_CONNECTIONS)
        while self.should_not_stop:
            if self.should_continue:
                # Need to check whether to keep going or to stop. Since this is
                # a separate thread we are using a message queue
                # TODO Find a way to create alerts on separate thread without running into a QObject::setParent error.
                if not self.queue.empty() and self.queue.get() == STOP_CODE:
                    self.appendToBox("Stock Checking Paused.")
                    self.queue.task_done()
                    self.should_continue = False
                    continue
                pages = list(executor.map(stock_checker.fetch_content, links))
                for i in range(len(pages)):
                    if not self.queue.empty() and self.queue.get() == STOP_CODE:
                        self.appendToBox("Stock Checking Paused.")
                        self.should_continue = False
                        self.queue.task_done()
                        break
                    if stock_checker.is_in_stock(pages[i], stock_checker.get_relevant_dict(storemap[links[i]])):
                        # TODO Make colored stock messages (Out of stock = red, instock = green)
                        self.addInStockText(links[i])
                        playsound(stock_checker.SOUNDPATH)
                    else:
                        self.addOutOfStockText(links[i])
                self.sleep_interrupt.wait(timeout=sleep_time)
            sleep(IDLE_SLEEP)

    def closeEvent(self, event) -> None:
        print("Closing...")
        self.should_continue = False
        self.should_not_stop = False
        self.sleep_interrupt.set()
        self.close()

    def addOutOfStockText(self, link) -> None:
        ''' Adds an "out of stock" message into the stock display box. Out of stock messages will have
        "Out of stock", coloured in red, following the item link (whose font color is black). '''
        html_text = "<a href=" + link + " style='float:left;'>" + link + "</a>" + OOS_MESSAGE
        self.appendHTMLToBox(html_text)

    def addInStockText(self, link) -> None:
        ''' Adds an "in stock" message to the stock display box. In stock messages are coloured in green. '''
        html_text = "<a href=" + link + " style='float:left;'>" + link + "</a>" + INSTOCK_MESSAGE
        self.appendHTMLToBox(html_text)

    def appendHTMLToBox(self, msg: str) -> None:
        ''' Appends the corresponding HTML message to self.StockDisplayBox.\n
        Note: This does not add a newline, unlike appendToBox. '''
        self.text_lock.acquire()
        self.StockDisplayBox.insertHtml(msg + "<br>")
        self.scrollToBottom()
        self.text_lock.release()

    def appendToBox(self, msg: str) -> None:
        ''' Appends the corresponding message to self.StockDisplayBox as plain text. '''
        self.text_lock.acquire()
        self.StockDisplayBox.append(msg)
        self.scrollToBottom()
        self.text_lock.release()

    def scrollToBottom(self):
        self.TextScrollBar.setValue(self.TextScrollBar.maximum())
