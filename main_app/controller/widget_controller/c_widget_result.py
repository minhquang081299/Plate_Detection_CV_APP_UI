from ..widget_ui.widget_result import Ui_Result_Infor
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore

class WidgetResult(QWidget):
    doubleClicked = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui_result = Ui_Result_Infor()
        self.ui_result.setupUi(self)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
