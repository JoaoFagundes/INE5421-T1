from ui.main_window_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.message = QMessageBox()

        self.checkStringButton.clicked.connect(self.check_string)

    def check_string(self):
        accepted = False

        if accepted:
            self.message.setText('The string is accepted by the automaton!')
            self.message.show()
        else:
            self.message.setText('The string is NOT accepted by the automaton!')
            self.message.show()
