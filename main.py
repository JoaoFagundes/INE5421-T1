# Joao Victor Fagunes
# Salomao Rodrigues Jacinto
# INE5421 - Trablho Prático I Junho 2018

import sys
from ui.main_window import MainWindow

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    