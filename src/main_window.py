# Main (first) window
from multiprocessing import Value
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox
import sys
from sc_window import StockWindow
import validators

class MainWindow(QWidget):
    ''' The first window you see upon opening the application. \n
    Attributes:
    - Title (QLabel) : The name of the program. \n
    - LinksBox (QTextEdit) : The textarea to paste links. \n
    - SubmitButton (QPushButton) : The button to start checking stock.\n
    - sleepMessage (QLabel) : The label for the sleep input box\n
    - sleepInputBox (QLineEdit) : The area to input the time to wait before checking again. Must be a number (float). \n
    '''
    def __init__(self) -> None:
        super().__init__()
        self.createDefaultUI()
    

    def createDefaultUI(self) -> None:
        ''' Sets up the UI for the main window. '''
        self.setWindowTitle("Stock Checker")
        self.setGeometry(0, 0, 800, 600)

        # Creating widgets
        self.layout = QVBoxLayout()
        title = QLabel("Stock Checker")
        self.LinksBox = QTextEdit()
        self.LinksBox.setPlaceholderText("Paste your links here...")
        self.sleepMessageBox = QHBoxLayout()
        sleepMessage = QLabel("How many seconds do you want to wait before checking again?")
        self.sleepInputBox = QLineEdit()
        self.sleepMessageBox.addWidget(sleepMessage)
        self.sleepMessageBox.addWidget(self.sleepInputBox)
        self.SubmitButton = QPushButton("Start Checking!")
        self.SubmitButton.clicked.connect(self.moveToStockWindow)

        # Adding widgets
        self.layout.addWidget(title)
        self.layout.addWidget(self.LinksBox)
        self.layout.addLayout(self.sleepMessageBox)
        self.layout.addWidget(self.SubmitButton)
        self.setLayout(self.layout)
        self.show()


    def moveToStockWindow(self) -> None:
        ''' Changes the current window to the stock window.'''
        # TODO Add this to controller class?
        links : list[str] = self.LinksBox.toPlainText().split("\n")
        valid_links = True
        # Catch bad URLs
        if not linksAreValid(links):
            createAlert("Please enter valid links.")
            return
        #Catch bad numerical input
        try:
            sleepTime : float = float(self.sleepInputBox.text())
        except ValueError:
            createAlert("Please set the sleep time to a valid number.")
            return
        self.scWin = StockWindow(links = links, sleepTime = sleepTime)
        self.scWin.show()
        self.hide()

def linksAreValid(links : list) -> bool:
    ''' Checks whether a list of links contains only valid links (links may not actually exist). '''
    for link in links:
        if type(validators.url(link)) == validators.utils.ValidationFailure:
            return False
    return True

def createAlert(msg : str) -> None:
    ''' Creates a QMessageBox with the corresponding message. '''
    alert = QMessageBox()
    alert.setWindowTitle("Error")
    alert.setText(msg)
    alert.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())