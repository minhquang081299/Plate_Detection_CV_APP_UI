from ..widget_ui.widget_image import Ui_WidgetImage
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtGui
import cv2
from ..widget_ui.widget_result import Ui_Result_Info
from ..widget_controller.c_widget_video import WidgetVideo
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QShortcut, QMessageBox
from PyQt5.QtGui import QKeySequence, QPixmap, QPainter, QPen, QFont, QBrush, QColor, QCursor



class WidgetImage(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_WidgetImage()
        self.ui.setupUi(self)
        self.ui_result = Ui_Result_Info()
        # self.ui_result.setM
        self.wg_video = WidgetVideo()
        self.current_img_index = 0
        self.imgs_list = []
        self.qt_img = None

        QShortcut(QKeySequence(Qt.Key_Left), self, activated=self.move_left)
        QShortcut(QKeySequence(Qt.Key_Right), self, activated=self.move_right)

    def slot_get_list_rs(self, list_rs):
        self.imgs_list = list_rs
        if self.current_img_index == len(list_rs):
            self.current_img_index = 0

        if self.current_img_index == 0:
            perc = 1 / len(self.imgs_list)
            self.ui.progressBar.setValue(perc * 100)

        qt_img = list_rs[self.current_img_index][1]
        self.qt_img = cv2.resize(qt_img,(960,460))
        # rgb_img = self.img.copy()
        # self.wg_video.show_image(rgb_img, self.ui.qlabel_image)

    def move_right(self):
        if self.current_img_index >= len(self.imgs_list):
            self.current_img_index = len(self.imgs_list)
        else:
            self.current_img_index += 1
        if self.current_img_index < len(self.imgs_list):
            perc = (self.current_img_index + 1) / len(self.imgs_list)
        else:
            perc = 1 / len(self.imgs_list)
        
        self.slot_get_list_rs(self.imgs_list)
        self.ui.progressBar.setValue(perc*100)

    def move_left(self):

        if self.current_img_index <= 0:
            self.current_img_index = 0
        else:
            self.current_img_index -= 1

        perc = (self.current_img_index + 1) / len(self.imgs_list)
        self.slot_get_list_rs(self.imgs_list)
        self.ui.progressBar.setValue(perc * 100.)
        


    def paintEvent(self, e) -> None:
        if self.qt_img is not None:
            self.wg_video.show_image(self.qt_img, self.ui.label)
            self.ui.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored)
        # if self.__thread_capture.buffer_frame.qsize() > 0:
        #     frame_cap = self.__thread_capture.buffer_frame.get()
        #     self.frame = frame_cap
        #     self.show_image(frame_cap, self.ui.qlabel_result)
        self.update()

        

    def on_double_click(self):
        sender = self.sender()
        self.ui_result.setMinimumSize(700, 700)
        if sender:
            self.ui_result.qlabel_plate.setText(sender.qlabel_plate.text())
            self.ui_result.qlabel_time.setText(str(sender.qlabel_time.text()))
            self.ui_result.qlabel_image_car.setMinimumSize(700, 700)
            # print('-------------------------------',sender.frame.shape)
            self.wg_video.show_image(sender.frame, self.ui_result.qlabel_image_car)
            self.ui_result.qlabel_image_car.setScaledContents(True)
            self.ui_result.show()
            
        