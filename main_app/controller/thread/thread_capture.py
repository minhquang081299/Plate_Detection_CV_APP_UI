from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
from queue import Queue
import cv2
from datetime import datetime
from ...config import FOLDER_SAVE
import os

class ThreadCapture(QThread):
    
    def __init__(self) -> None:
        super().__init__()
        self.__buffer_capture = Queue()
        self.__buffer_frame = Queue()
        self.__max_buffer_size = 10
        self.__thread_active = False
        self.__cap = cv2.VideoCapture(0) # Đổi webcam
        self.__flag_capture = False

    def slot_get_flag_capture(self, flag_capture):
        self.__flag_capture = flag_capture

    @property
    def buffer_capture(self):
        return self.__buffer_capture
    
    @property
    def buffer_frame(self):
        return self.__buffer_frame
    
    @staticmethod
    def create_folder(path:str):
        if os.path.exists(path):
            return
        os.mkdir(path)

    def run(self):
        self.__thread_active = True
        while self.__thread_active:
            ret, frame = self.__cap.read()
            if not ret:
                self.msleep(5000)
                continue

            if self.__flag_capture:
                self.__buffer_frame.put(frame)
                fp = os.path.join(FOLDER_SAVE, 'images_capture')
                self.create_folder(fp)
                file_name = f"{fp}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(file_name, frame)
                self.__flag_capture = False

            if self.__buffer_capture.qsize() < self.__max_buffer_size:
                self.__buffer_capture.put(frame)

    def stop(self):
        self.__thread_active = False