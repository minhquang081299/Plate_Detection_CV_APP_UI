
#### Change config folder save and TESSERACT_PATH in resources/config/config.yaml
#### Download code from git
  - `git clone -b dev https://github.com/minhquang081299/Plate_Detection_CV_APP_UI.git`
#### Install library
  - `cd Plate_Detection_CV_APP_UI` 
  - `pip install -r requirements.txt`
  - Download and install [Tesseract-OCR](https://tesseract-ocr.github.io/tessdoc/) v5.0.0 (alpha)
#### Run code
  - Open terminal
  - `python main.py`
#### File logic and algorithm
  - `main_app/recognize_plate.py`
  - `main_app/anprclass.py`
#### UI
1. Process with file image/video/webcam
   - Click choose folder to choose folder you want process
2. Choose algorithm OpenCV and params models
3. Views history Log on UI and file local
   - Double click mount to views result image on history log
   - Click '->' to views next image
