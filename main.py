from main_app.controller.widget_controller.c_main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import os


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    window.show()
    sys.exit(app.exec_())
