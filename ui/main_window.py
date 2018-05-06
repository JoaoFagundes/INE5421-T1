from ui.main_window_ui import Ui_MainWindow
from ui.not_ok_string_dialog import Ui_Dialog as Ui_not_ok
from ui.ok_string_dialog import Ui_Dialog as Ui_ok
from PyQt5.QtWidgets import QMainWindow, QDialog

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.ok_dialog = QDialog()
        ok_dialog_ui = Ui_ok()
        ok_dialog_ui.setupUi(self.ok_dialog)

        self.not_ok_dialog = QDialog()
        not_ok_dialog_ui = Ui_not_ok()
        not_ok_dialog_ui.setupUi(self.not_ok_dialog)

        self.checkStringButton.clicked.connect(self.check_string)

    def check_string(self):
        accepted = False

        if accepted:
            self.ok_dialog.show()
        else:
            self.not_ok_dialog.show()
