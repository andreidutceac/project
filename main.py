from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QLineEdit, QWidget,   \
    QPushButton, QLabel
from PyQt6.QtGui import QPixmap, QColor, QImage
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QObject, QThread
import cv2 as cv
import sys
import numpy as np
from download import Download
sys.path.append('/yolo/yolov5-master')
from yolo.yolov5master.detect import run
import mobilenet_ssd.mobilenet as mobilenet



class Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Object Detection Camera")
        self.setFixedHeight(600)
        self.setFixedWidth(1000)

        # define buttons, lineedit, titles and frames
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Copy the link here..")

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download)

        self.detection_button = QPushButton("Object Detection", self)
        self.detection_button.clicked.connect(self.detection)

        self.show_button = QPushButton("View Results")
        self.show_button.clicked.connect(self.show_video)

        self.title1 = QLabel("YOLO V5")
        font = self.title1.font()
        font.setPointSize(20)
        self.title1.setFont(font)
        self.title1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.frame1 = QLabel(self)
        self.frame1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        grey = QPixmap(500, 500)
        grey.fill(QColor('darkGray'))
        self.frame1.setPixmap(grey)

        self.title2 = QLabel("MobileNet SSD")
        font = self.title1.font()
        font.setPointSize(20)
        self.title2.setFont(font)
        self.title2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.frame2 = QLabel(self)
        self.frame2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        grey = QPixmap(500, 500)
        grey.fill(QColor('darkGray'))
        self.frame2.setPixmap(grey)


        # display icons
        cv_img = cv.imread('play1.png')
        qt_img = self.convert_cv_qt(cv_img)
        qt_img2 = self.convert_cv_qt(cv_img)
        self.frame1.setPixmap(qt_img)
        self.frame2.setPixmap(qt_img2)


        # create layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.input, 0, 0, 1, 3)
        self.layout.addWidget(self.download_button, 0, 3, 1, 1)
        self.layout.addWidget(self.detection_button, 0, 4, 1, 1)
        self.layout.addWidget(self.show_button, 0, 5, 1, 1)
        self.layout.addWidget(self.title1, 1, 0, 1, 3)
        self.layout.addWidget(self.frame1, 2, 0, 6, 3)
        self.layout.addWidget(self.title2, 1, 3, 1, 3)
        self.layout.addWidget(self.frame2, 2, 3, 6, 3)
        self.setLayout(self.layout)
        self.show()


    # create download-video function
    def download(self):
        link = self.input.text()
        Download(link)


    # run the algorithms
    def detection(self):

        # run Yolo algorithm
        print("Run MobileNet SSD algorithm...")
        mobilenet.filename = "download.mp4"
        mobilenet.main()

        # run MobileNet algorithm
        print("Run YOLO.V5 algorithm... ")
        run(source="download.mp4")
        print("Completed!")


    # show converted videos
    def show_video(self):

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.thread2 = VideoThread2()
        self.thread2.change_pixmap_signal.connect(self.update_image2)
        self.thread2.start()


    # Convert from an opencv image to QPixmap
    def convert_cv_qt(self, cv_img):

        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(400, 350, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

    #Updates the image_label with a new opencv image
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.frame1.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_image2(self, cv_img2):
        qt_img2 = self.convert_cv_qt(cv_img2)
        self.frame2.setPixmap(qt_img2)



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        cap = cv.VideoCapture("yolo.mp4")
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
                cv.waitKey(20)

class VideoThread2(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        cap = cv.VideoCapture("mobilenet.mp4")
        while True:
            ret, cv_img2 = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img2)
                cv.waitKey(20)



app = QApplication(sys.argv)
w = Main_Window()
w.show()
app.exec()