import time
from ..widget_ui.main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGridLayout, QMessageBox
from .c_widget_image import WidgetImage
from .c_widget_video import WidgetVideo
from .c_widget_log import WidgetLog
from ..widget_ui.widget_result import Ui_Result_Info
import os
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from ...models.recognize_plate import DetectPlate
from datetime import datetime
import cv2



class MainWindow(QMainWindow):
    sig_config_model = pyqtSignal(str, str, str, str)
    sig_list_rs = pyqtSignal(list)
    sig_list_path = pyqtSignal(list)
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_start_log.hide()
        self.setWindowTitle("Plate Recognize App")

        self.model_anpr = None
        self.model_recognize = None
        
        #define variables
        self.define_variables()

        self.list_rs_widget = []

        self.connect_btn_signals()
                        
    def define_variables(self):
        self.file_name = ""
        
        self.widget_image = WidgetImage()
        self.widget_video = WidgetVideo()
        self.widget_log = WidgetLog()
        self.ui.qframe_widget.hide()
        self.ui.gridLayout.addWidget(self.widget_image, 0, 1, 2, 1)
        self.ui.gridLayout.addWidget(self.widget_log, 0, 1, 2, 1)
        self.grid_layout_cameras = QGridLayout()
        self.grid_layout_cameras.setContentsMargins(0, 0, 0, 0)
        self.ui.qframe_widget.setLayout(self.grid_layout_cameras)
        # self.grid_layout_cameras.addWidget(self.widget_image, 0, 0)
        self.grid_layout_cameras.addWidget(self.widget_video, 0, 0)
        self.widget_video.hide()
        self.widget_log.hide()
        
        self.current_widget = self.widget_image
        
        self.current_option_index = self.ui.combo_options.currentIndex()

    def clear_scroll_area(self, list_wg):
        for wg in list_wg:
            wg.deleteLater()
        list_wg.clear()
        
    def connect_btn_signals(self):
        self.ui.btn_choose_folder.clicked.connect(self.choose_folder)
        self.ui.combo_options.currentIndexChanged.connect(self.change_option)
        self.ui.btn_start.clicked.connect(self.start)
        self.ui.btn_stop.clicked.connect(self.stop)
        self.ui.btn_load_model.clicked.connect(self.load_model)
        self.widget_video.ui.btn_capture.clicked.connect(self.inference_from_camera)
        
        self.sig_list_rs.connect(self.widget_image.slot_get_list_rs)
        self.ui.btn_start_log.clicked.connect(self.start_log)
        self.sig_list_path.connect(self.widget_log.slot_get_list_rs)

    def get_config_model(self):
        clear_border = self.ui.txt_clear_border.toPlainText()
        psm = self.ui.txt_psm.toPlainText()
        algo = self.ui.cb_algorithm.currentIndex()+1
        morp = self.ui.cb_morphology.currentText()

        print("clear_border: ", clear_border)
        print("psm: ", psm)
        print("algo: ", algo)
        print("morp: ", morp)

        # self.sig_config_model.emit(clear_border, psm, algo, morp)
        return int(clear_border), int(psm), algo, morp
    
    def load_model(self):
        clear_border, psm, algo, morp = self.get_config_model()
        if clear_border == "":
            clear_border = -1
        if psm == "":
            psm = 7

        if not isinstance(clear_border, int) or not isinstance(psm, int):
            QMessageBox.about(self, "Error", "Please input a number")
            return
        self.model_recognize = DetectPlate(int(clear_border), int(psm), algo, morp)
        self.model_anpr = self.model_recognize.load_model_opencv()

        QMessageBox.about(self, "Success", "Load model success")
        
        
    def choose_folder(self):
        if self.current_option_index == 0 or self.current_option_index == 2:
            data_path= str(QFileDialog.getExistingDirectory(
            None, "Select Directory", '/', QFileDialog.DontUseNativeDialog))
            self.imgs_path = []
            self.txt_path = []
            if data_path is not None:
                try:
                    for file in os.listdir(data_path):
                        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG") or file.endswith(
                                ".PNG") or file.endswith(".jpeg") or file.endswith(".JPEG"):
                            self.imgs_path.append(f"{data_path}/{file}")
                        
                        if file.endswith(".txt"):
                            self.txt_path.append(f"{data_path}/{file}")
                except:
                    QMessageBox.about(self, "Error", "No such file or directory")
                    print("No such file or directory")
                    return
        print("file_name: ", data_path)
        print("imgs_path: ", self.imgs_path)
        self.file_name = data_path
        self.ui.qtext_folder_path.setText(self.file_name)

    def inference_from_camera(self):
        self.widget_video.sig_capture_frame.emit(True)
        if self.model_anpr is None:
            QMessageBox.about(self, "Error", "Please load model")
            return
        if self.current_option_index == 1:
            if self.widget_video.frame is not None:
                lp_text, image = self.model_recognize.inference_capture(self.model_anpr, self.widget_video.frame)
                dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.widget_video.ui.qlabel_date_time.setText("Time: "+dt)
                if lp_text is not None:
                    self.widget_video.ui.qlabel_result.setText("Plate Recognize"+lp_text)
                self.widget_video.show_image(self.widget_video.frame, self.widget_video.ui.qlabel_crop_frame)
                self.widget_video.show_image(image, self.widget_video.ui.qlabel_result)
            
            else:
                print("No frame")
        else:
            print("No frame")

    def set_view_log(self):
        self.widget_log.show()
        self.ui.btn_load_model.hide()
        self.ui.cb_algorithm.hide()
        self.ui.cb_morphology.hide()

    def inference_from_folder(self):
        if self.model_anpr is None:
            QMessageBox.about(self, "Error", "Please load model")
            return
        
        if self.current_option_index == 0:
            if self.file_name == "":
                QMessageBox.about(self, "Error", "Please choose a folder")
                return
            
            list_rs = self.model_recognize.inference_from_folder(self.model_anpr, self.imgs_path)
            self.sig_list_rs.emit(list_rs)
            return list_rs
            
    def add_widget_result_to_scroll(self, list_rs):
        self.clear_scroll_area(self.list_rs_widget)
        for rs in list_rs:
            vehicle_widget = Ui_Result_Info()
            vehicle_widget.qlabel_plate.setText(rs[0])
            vehicle_widget.qlabel_time.setText(rs[2])
            vehicle_widget.frame = rs[1]
            img = cv2.resize(rs[1], (300, 300))
            self.widget_video.show_image(img, vehicle_widget.qlabel_image_car)
            vehicle_widget.qlabel_image_car.setScaledContents(True)
            vehicle_widget.doubleClicked.connect(self.widget_image.on_double_click)
            self.widget_image.ui.scrollAreaWidgetContents.layout().addWidget(vehicle_widget)
            self.list_rs_widget.append(vehicle_widget)

    def change_option(self):
        print("change_option: ", self.ui.combo_options.currentIndex())
        self.current_option_index = self.ui.combo_options.currentIndex()
        if self.current_option_index == 0:
            self.file_name = ""
            self.ui.qframe_widget.hide()
            self.ui.gridLayout.addWidget(self.widget_image, 0, 1, 2, 1)
            self.widget_log.hide()
            self.ui.frame_config.show()
            self.widget_image.show()
            self.ui.btn_start_log.hide()
            self.widget_video.hide()
        elif self.current_option_index == 1:
            self.file_name = ""
            self.ui.qframe_widget.show()
            self.widget_image.hide()
            self.widget_log.hide()
            self.ui.btn_start_log.hide()
            self.ui.frame_config.show()
            self.widget_video.show()

        elif self.current_option_index == 2:
            self.file_name = ""
            self.ui.qframe_widget.hide()
            self.widget_image.hide()
            self.ui.frame_config.hide()
            self.widget_log.show()
            self.ui.btn_start_log.show()
            self.ui.btn_start_log.setGeometry(QtCore.QRect(10, 150, 232, 31))
            

    def start(self):
        
        if self.current_option_index == 0:
            fn = self.ui.qtext_folder_path.toPlainText()
            if not fn:
                QMessageBox.about(self, "Error", "Please choose a folder")
                return
            self.widget_video.stop_thread()
            list_rs = self.inference_from_folder()
            self.add_widget_result_to_scroll(list_rs)
            QMessageBox.about(self, "Success", "Inference success")
            
        elif self.current_option_index == 1:
            self.widget_video.start_thread()
            self.ui.btn_start.setEnabled(False)
            self.ui.btn_stop.setEnabled(True)

    def start_log(self):
        if self.current_option_index == 2:
            fn = self.ui.qtext_folder_path.toPlainText()
            if not fn:
                QMessageBox.about(self, "Error", "Please choose a folder")
                return
            
            self.sig_list_path.emit([self.imgs_path, self.txt_path])
            
    
    def stop(self):
        if self.current_option_index == 0:
            self.widget_image.stop()
        elif self.current_option_index == 1:
            self.widget_video.stop_thread()
            self.ui.btn_start.setEnabled(True)
            self.ui.btn_stop.setEnabled(False)
            