''' Main (first) window of the Stock Checker application '''
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox
from sc_window import StockWindow
import validators


class MainWindow(QWidget):
    ''' The first window you see upon opening the application. \n
    Attributes:
    - Title (QLabel) : The name of the program.
    - LinksBox (QTextEdit) : The textarea to paste links.
    - SubmitButton (QPushButton) : The button to start checking stock.
    - sleepMessage (QLabel) : The label for the sleep input box
    - sleepInputBox (QLineEdit) : The area to input the time to wait before checking again. Must be a number (float).
    '''

    def __init__(self) -> None:
        super().__init__()
        self.createDefaultUI()

    def createDefaultUI(self) -> None:
        ''' Sets up the UI for the main window. '''
        self.setWindowTitle("Inventory Inspector")
        self.setGeometry(0, 0, 800, 600)

        # Creating widgets
        self.layout = QVBoxLayout()
        title = QLabel("Inventory Inspector")
        self.LinksBox = QTextEdit()
        self.LinksBox.setPlaceholderText("Paste your links here...")
        self.sleepMessageBox = QHBoxLayout()
        sleepMessage = QLabel("How many seconds do you want to wait before checking again?")
        self.sleepInputBox = QLineEdit()
        self.sleepMessageBox.addWidget(sleepMessage)
        self.sleepMessageBox.addWidget(self.sleepInputBox)
        self.SubmitButton = QPushButton("Start Inspecting!")
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
        links: list[str] = self.LinksBox.toPlainText().split("\n")
        # Catch bad URLs
        if not linksAreValid(links):
            createAlert("Please enter valid links.")
            return
        # Catch bad numerical input
        try:
            sleepTime: float = float(self.sleepInputBox.text())
        except ValueError:
            createAlert("Please set the sleep time to a valid number.")
            return
        self.scWin = StockWindow(links=links, sleepTime=sleepTime)
        self.scWin.show()
        self.hide()


def linksAreValid(links: list) -> bool:
    ''' Checks whether a list of links contains only valid links (links may not actually exist). '''
    for link in links:
        if type(validators.url(link)) == validators.utils.ValidationFailure:
            return False
    return True


def createAlert(msg: str) -> None:
    ''' Creates a QMessageBox with the corresponding message. '''
    alert = QMessageBox()
    alert.setWindowTitle("Error")
    alert.setText(msg)
    alert.exec_()
