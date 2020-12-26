# Stock checking window
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QTextBrowser, QMessageBox
import sys
import stock_checker
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import multiprocessing 
import threading
from queue import Queue
from time import sleep
import main_window

MAX_CONNECTIONS : int = 100

STOP_CODE : int = 1
CONTINUE_CODE : int = 2

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
    def __init__(self, links : list, sleepTime : float) -> None:
        self.links = links
        self.sleepTime = sleepTime
        self.should_continue = True
        self.should_not_stop = True
        self.queue = Queue(maxsize=0)
        super().__init__()
        self.createUI()
        self.work_thread = threading.Thread(target=self.check_stock)
        self.work_thread.start()
        
    
    def createUI(self) -> None:
        self.setWindowTitle("Stock Checker")
        self.setGeometry(0, 0, 800, 600)

        # Creating widgets
        self.layout = QVBoxLayout()
        title = QLabel("Stock Checker")
        self.StockDisplayBox = QTextBrowser()
        self.StockDisplayBox.setOpenExternalLinks(True)
        self.StockDisplayBox.setOpenLinks(True)
        self.StockDisplayBox.append("Checking links:\n")
        self.StockDisplayBox.setAcceptRichText(True)
        self.StartStopButton = QPushButton("Stop")
        self.StartStopButton.clicked.connect(self.stop_start)
        # Adding widgets
        self.layout.addWidget(title)
        self.layout.addWidget(self.StockDisplayBox)
        self.layout.addWidget(self.StartStopButton)
        self.setLayout(self.layout)
        self.show()

    
    def stop_start(self) -> None:
        if self.StartStopButton.text() == "Start":
            if not self.queue.empty():
                main_window.createAlert("Stock checking has not paused yet. Please wait.")
                return
            self.should_continue = True
            self.StockDisplayBox.append("Resumed checking stock.")
            self.StartStopButton.setText("Stop")
        else:
            self.queue.put(STOP_CODE)
            self.StockDisplayBox.append("Pausing...")
            self.StartStopButton.setText("Start")
        return


    def check_stock(self):
        ''' Checks the stock of the items in self.links and displays the results on the text area corresponding
        to self.StockDisplayBox. \n  '''
        links = self.links
        sleep_time = self.sleepTime
        storemap = {link : stock_checker.get_domain_name(link) for link in links}
        executor = ThreadPoolExecutor(max_workers=MAX_CONNECTIONS)
        while self.should_not_stop:
            if self.should_continue:
                # Need to check whether to keep going or to stop. Since this is 
                # a separate thread we are using a message queue
                # TODO Find a way to create alerts on separate thread without running into a QObject::setParent error.
                if not self.queue.empty() and self.queue.get() == STOP_CODE:
                    self.StockDisplayBox.append("Stock Checking Paused.")
                    self.queue.task_done()
                    self.should_continue = False
                    continue
                pages = list(executor.map(stock_checker.fetch_content, links))
                for i in range(len(pages)):
                    if not self.queue.empty() and self.queue.get() == STOP_CODE:
                        self.StockDisplayBox.append("Stock Checking Paused.")
                        self.should_continue = False
                        self.queue.task_done()
                        break
                    if stock_checker.is_in_stock(pages[i], stock_checker.get_relevant_dict(storemap[links[i]])):
                        # TODO Make colored stock messages (Out of stock = red, instock = green)
                        self.StockDisplayBox.append(links[i] + " Is in stock!!!")
                        stock_checker.playsound(stock_checker.SOUNDPATH)
                    else:
                        self.StockDisplayBox.append(links[i] + " Out of stock")
                sleep(sleep_time)
    

    def closeEvent(self, event):
        print("Closing...")
        self.should_continue = False
        self.should_not_stop = False
        self.close()