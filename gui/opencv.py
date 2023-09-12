import sys
import cv2 as cv
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget ,QApplication, QInputDialog, QLineEdit,QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
import threading 
import time

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.control_button = QPushButton("Play/Pause")
        self.control_button.clicked.connect(self.togglePlayback)
        self.layout.addWidget(self.control_button)

        self.screenshot_button = QPushButton("Take Screenshot")
        self.screenshot_button.clicked.connect(self.takeScreenshot)
        self.layout.addWidget(self.screenshot_button)

        self.screenshot_button = QPushButton("Open")
        self.screenshot_button.clicked.connect(self.openImage)
        self.layout.addWidget(self.screenshot_button)

        self.video_capture = cv.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.playback = False

        self.setLayout(self.layout)

    def updateFrame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap)

    def togglePlayback(self):
        if self.playback:
            self.timer.stop()
        else:
            self.timer.start(30)  # Adjust interval as needed
        self.playback = not self.playback

    def takeScreenshot(self):
        ret, frame = self.video_capture.read()
        if ret:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "Images (*.png);;All Files (*)")
            if file_name:
                cv.imwrite(file_name, frame)
                QMessageBox.information(self, "Screenshot Saved", "Screenshot saved successfully.")

    def openImage(self):
        if self.playback:
            self.timer.stop()
        else:
            self.timer.start(30)  # Adjust interval as needed
        self.playback = not self.playback

    
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.setWindowTitle("Video Player")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
