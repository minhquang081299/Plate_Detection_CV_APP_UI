import time
import cv2
from ..widget_ui.widget_video import Ui_WidgetVideo
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtGui, QtCore
from queue import Queue
from ..thread.thread_capture import ThreadCapture


class WidgetVideo(QWidget):
    sig_capture_frame = QtCore.pyqtSignal(bool)
    def __init__(self, parent=None, inference_tool=...):
        super().__init__(parent)
        self.ui = Ui_WidgetVideo()
        self.ui.setupUi(self)
        self._init_thread()
        self.connect_signals()
        self.frame = None
        # self.start_thread()
    
    def _init_thread(self):
        self.__thread_capture = ThreadCapture()

    def start_thread(self):
        self.__thread_capture.start()

    def stop_thread(self):
        self.__thread_capture.stop()

    def connect_signals(self):
        # self.ui.btn_capture.clicked.connect(self.capture_image)
        self.sig_capture_frame.connect(self.__thread_capture.slot_get_flag_capture)
        
    def paintEvent(self, e) -> None:
        if self.__thread_capture.buffer_capture.qsize() > 0:
            frame= self.__thread_capture.buffer_capture.get()
            self.frame = frame
            self.show_image(frame, self.ui.qlabel_frame)
        # if self.__thread_capture.buffer_frame.qsize() > 0:
        #     frame_cap = self.__thread_capture.buffer_frame.get()
        #     self.frame = frame_cap
        #     self.show_image(frame_cap, self.ui.qlabel_result)
        self.update()
    
    def capture_image(self):
        self.sig_capture_frame.emit(True)
    
    def show_image(self, rgb_img, qlabel_frame):
        # rgb_img = cv2.resize(rgb_img, (qlabel_frame.width(), qlabel_frame.height()))
        rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)
        qt_img = QtGui.QPixmap.fromImage(
            QtGui.QImage(rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QtGui.QImage.Format_RGB888)).scaled(
            qlabel_frame.width(), qlabel_frame.height())
        qlabel_frame.setPixmap(qt_img)
        
    
    
    