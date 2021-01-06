import sys
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
	main()
