from ..widget_ui.widget_log import Ui_WidgetLog
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
import os


class WidgetLog(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_WidgetLog()
        self.ui.setupUi(self)
        self.ui_result = Ui_Result_Info()
        # self.ui_result.setM
        self.wg_video = WidgetVideo()
        self.current_img_index = 0
        self.imgs_list = []
        self.txt_path = []
        self.list_rs_widget = []
        self.qt_img = None

        QShortcut(QKeySequence(Qt.Key_Left), self, activated=self.move_left)
        QShortcut(QKeySequence(Qt.Key_Right), self, activated=self.move_right)

    def clear_scroll_area(self, list_wg):
        for wg in list_wg:
            wg.deleteLater()
        list_wg.clear()

    def slot_get_list_rs(self, list_rs):
        self.imgs_list = list_rs[0]
        self.txt_path = list_rs[1]
        
        self.clear_scroll_area(self.list_rs_widget)
        for i in range(len(self.txt_path)):
            rs = ''
            with open(self.txt_path[i], 'r') as f:
                for line in f.readlines():
                    rs = line
            name = os.path.basename(self.txt_path[i])
            time_dt = name.split('.')[0]

            file_name = self.txt_path[i].split('.')[0]

            path_img = file_name + '.jpg'
            
            vehicle_widget = Ui_Result_Info()
            vehicle_widget.qlabel_plate.setText(rs)
            vehicle_widget.qlabel_time.setText(time_dt)
            vehicle_widget.frame = cv2.imread(path_img)
            self.wg_video.show_image(vehicle_widget.frame, vehicle_widget.qlabel_image_car)
            vehicle_widget.qlabel_image_car.setScaledContents(True)
            vehicle_widget.doubleClicked.connect(self.on_double_click)
            self.ui.scrollAreaWidgetContents.layout().addWidget(vehicle_widget)
            self.list_rs_widget.append(vehicle_widget)
        
        self.get_img()
        

    def get_img(self):
        if self.current_img_index == len(self.imgs_list):
            self.current_img_index = 0

        if self.current_img_index == 0:
            perc = 1 / len(self.imgs_list)
            self.ui.progressBar.setValue(perc * 100)

        qt_img = cv2.imread(self.imgs_list[self.current_img_index])
        self.qt_img = cv2.resize(qt_img,(960,460))

    def move_right(self):
        if self.current_img_index >= len(self.imgs_list):
            self.current_img_index = len(self.imgs_list)
        else:
            self.current_img_index += 1
        if self.current_img_index < len(self.imgs_list):
            perc = (self.current_img_index + 1) / len(self.imgs_list)
        else:
            perc = 1 / len(self.imgs_list)
        
        self.get_img()
        self.ui.progressBar.setValue(perc*100)

    def move_left(self):

        if self.current_img_index <= 0:
            self.current_img_index = 0
        else:
            self.current_img_index -= 1

        perc = (self.current_img_index + 1) / len(self.imgs_list)
        self.get_img()
        self.ui.progressBar.setValue(perc * 100.)
        

    def paintEvent(self, e) -> None:
        if self.qt_img is not None:
            self.wg_video.show_image(self.qt_img, self.ui.label)
            self.ui.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored)
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
            
        