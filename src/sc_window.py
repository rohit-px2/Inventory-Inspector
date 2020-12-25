# Stock checking window
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QTextBrowser
import sys
import stock_checker
import concurrent.futures
import multiprocessing
import threading

class StockWindow(QWidget):

    def __init__(self, links : list, sleepTime : float) -> None:
        self.links = links
        self.sleepTime = sleepTime
        self.should_run = True
        super().__init__()
        self.createUI()
        self.work_thread = threading.Thread(target=self.check_stock)
        self.work_thread.start()
    

    def createUI(self) -> None:
        self.setWindowTitle("Stock Checker")
        self.setGeometry(0, 0, 800, 600)
        self.layout = QVBoxLayout()
        title = QLabel("Stock Checker")
        self.StockDisplayBox = QTextBrowser()
        self.StockDisplayBox.setOpenExternalLinks(True)
        self.StockDisplayBox.setOpenLinks(True)
        self.StockDisplayBox.append("Checking links:\n")
        self.StockDisplayBox.setAcceptRichText(True)
        self.StartStopButton = QPushButton("Stop")
        self.StartStopButton.clicked.connect(self.stop_start)
        self.layout.addWidget(title)
        self.layout.addWidget(self.StockDisplayBox)
        self.setLayout(self.layout)
        self.show()

    
    def stop_start(self) -> None:
        if self.StartStopButton.text() == "Start":
            self.should_run = True
            self.StartStopButton.setText("Stop")
        else:
            self.should_run = False
            self.StartStopButton.setText("Start")
        return


    def check_stock(self):
        links = self.links
        sleep_time = self.sleepTime
        storemp = {link : stock_checker.get_domain_name(link) for link in links}
        executr = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        while self.should_run:
            stock_checker.check_stock(links, sleep_time, self.StockDisplayBox, executor=executr, storemap=storemp)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = StockWindow(["hello"], 5.0)
    sys.exit(app.exec_())