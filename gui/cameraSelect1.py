import sys
import cv2 as cv
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class VideoPlayer(QWidget):
    def __init__(self, camera_index=2):
        super().__init__()
        self.initUI(camera_index)

    def initUI(self, camera_index):
        self.layout = QVBoxLayout(self)
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.video_capture = cv.VideoCapture(camera_index)  # Specify the camera index here
        if not self.video_capture.isOpened():
            raise ValueError("Unable to open camera. Check if the camera index is correct.")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(30)  # Update the frame every 30 milliseconds

    def updateFrame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.video_tab = VideoPlayer(camera_index=2)  # Specify the camera index here
        self.setCentralWidget(self.video_tab)

        self.setWindowTitle("OpenCV Camera Selection")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
