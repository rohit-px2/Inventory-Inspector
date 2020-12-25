# Stock checking window
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QTextBrowser
import sys
import stock_checker
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import multiprocessing 
import threading
from queue import Queue

class StockWindow(QWidget):

    def __init__(self, links : list, sleepTime : float) -> None:
        self.links = links
        self.sleepTime = sleepTime
        self.should_run = True
        queue = Queue(maxsize=0)
        super().__init__()
        self.createUI()
        # Need a thread separate from main thread which will run the stock checking loop.
        # TODO Make stopping/starting faster (can exit stock check loop instantly) using Queue
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
            self.StockDisplayBox.append("Resumed checking stock.")
            self.should_run = True
            self.StartStopButton.setText("Stop")
        else:
            self.StockDisplayBox.append("Paused checking stock.")
            self.should_run = False
            self.StartStopButton.setText("Start")
        return


    def check_stock(self):
        links = self.links
        sleep_time = self.sleepTime
        storemp = {link : stock_checker.get_domain_name(link) for link in links}
        executr = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        while True:
            if self.should_run:
                stock_checker.check_stock(links, sleep_time, self.StockDisplayBox, executor=executr, storemap=storemp)
    

    def closeEvent(self, event):
        print("Closing...")
        self.should_run = False
        self.work_thread.join()
        self.close()