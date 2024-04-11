import datetime

from .anprclass import CannyANPR, EdgelessANPR, SobelANPR
from imutils import paths
import argparse
import imutils
import sys
import cv2
import os
import shutil
from datetime import datetime
from ..config import FOLDER_SAVE

from .logger import get_logger

log = get_logger(__name__)

test = os.getcwd()
print(test)


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def remove_folder(dir_path):
    try:
        shutil.rmtree(dir_path)
        print(f"Đã xóa folder {dir_path}")
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


class DetectPlate:
    def __init__(self,
                 clear_border=-1,
                 psm=7,
                 algo=1,
                 morp='bh',
                 debug=-1,
                 save=0):
        self.input = input
        self.clear_border = clear_border
        self.morp = morp
        self.psm = psm
        self.algo = algo
        self.debug = debug
        self.save = save
        self.image = None

    @staticmethod
    def create_folder(path:str):
        if os.path.exists(path):
            return
        os.mkdir(path)

    def load_model_opencv(self):
        if self.algo == 1:
            anpr = SobelANPR(self.algo, self.input, morph=self.morp, debug=self.debug > 0,
                             save=self.save > 0)
            print("Sobel")
        elif self.algo == 2:
            anpr = CannyANPR(self.algo, self.input, morph=self.morp, debug=self.debug > 0,
                             save=self.save > 0)
        elif self.algo == 3:
            anpr = EdgelessANPR(self.algo, self.input, morph=self.morp, debug=self.debug > 0,
                                save=self.save > 0)
        else:
            anpr = None
            print('Invalid algorithm choice')
            sys.exit()
        return anpr
    
    

    def inference_capture(self, anpr, image):
        # print("image: ", image)
        if image is not None:
            # originimage =image
            # print("-------------originimage: ", originimage)
            # image = imutils.resize(originimage, width=400, height=400)

            image = cv2.bilateralFilter(image, 3, 105, 105)
            lpText, lpCnt = anpr.find_and_ocr(1, image, psm=self.psm, clearBorder=self.clear_border > 0)

            print("lpText: ", lpText)
            if lpText is not None and lpCnt is not None:
                filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f")

                box = cv2.boxPoints(cv2.minAreaRect(lpCnt))
                box = box.astype("int")
                cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

                (x, y, w, h) = cv2.boundingRect(lpCnt)
                print((x, y, w, h))
                cv2.putText(image, cleanup_text(lpText), (x, y - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                print("[INFO] Registration number: {}".format(lpText))

            if lpText is None:
                lpText = ''
            
            fp = os.path.join(FOLDER_SAVE, 'images_capture_inference')
            
            self.create_folder(fp)
            with open(f'{fp}/{filename}.txt', mode='w') as f:
                    f.write(lpText)
            cv2.imwrite(f"{fp}/{filename}.jpg", image)
            return lpText, image
        
    def inference_from_folder(self, anpr, folder_path):
        # imagePaths = list(paths.list_images(folder_path))
        iteration = 0
        list_result = []
        for imagePath in folder_path:
            iteration += 1
            image = cv2.imread(imagePath)
            originimage = image.copy()
            # image = imutils.resize(originimage, width=400, height=400)

            image = cv2.bilateralFilter(image, 3, 105, 105)
            # anpr.debug_imshow("Bilateral Filter", image, waitKey=True)
            lpText, lpCnt = anpr.find_and_ocr(iteration, image, psm=self.psm, clearBorder=self.clear_border > 0)
            if lpText is not None and lpCnt is not None:
                box = cv2.boxPoints(cv2.minAreaRect(lpCnt))
                box = box.astype("int")
                cv2.drawContours(originimage, [box], -1, (0, 255, 0), 2)

                (x, y, w, h) = cv2.boundingRect(lpCnt)
                print((x, y, w, h))
                cv2.putText(originimage, cleanup_text(lpText), (x, y - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                print("[INFO] Registration number: {}".format(lpText))
                print('origin_image',originimage.shape)
            
            if lpText is None:
                lpText = ''
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            fp = os.path.join(FOLDER_SAVE, 'images_inference')
            self.create_folder(fp)
            with open(f'{fp}/{filename}.txt', mode='w') as f:
                f.write(lpText)
            cv2.imwrite(f"{fp}/{filename}.jpg", originimage)
            list_result.append([lpText, originimage, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        return list_result
        
    

    def main(self, type):

        anpr = self.load_model_opencv()
        return self.inference(anpr, type=type)
    
if __name__ == "__main__":
    img = cv2.imread(r"D:\Company\Code_2\License-Plate-Detection-with-OpenCV\result_edgeless_malaysian\images\20240410100429549640.jpg")
    detect_tool = DetectPlate(input='malaysian', algo=3)
    detect_tool.image = img
    print(detect_tool.main(type="image"))

