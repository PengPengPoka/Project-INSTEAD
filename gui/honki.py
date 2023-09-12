import sys
import cv2 as cv
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTabWidget, QFileDialog, QMessageBox
import threading

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.control_button = QPushButton("Play/Pause")
        self.control_button.clicked.connect(self.togglePlayback)
        self.layout.addWidget(self.control_button)

        self.screenshot_button = QPushButton("Take Screenshot")
        self.screenshot_button.clicked.connect(self.takeScreenshot)
        self.layout.addWidget(self.screenshot_button)

        self.video_selfture = cv.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.playback = False

    def updateFrame(self):
        ret, frame = self.video_selfture.read()
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
            self.timer.start(30)  
        self.playback = not self.playback

    def takeScreenshot(self):
        ret, frame = self.video_selfture.read()
        if ret:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "Images (*.png);;All Files (*)")
            if file_name:
                cv.imwrite(file_name, frame)
                QMessageBox.information(self, "Screenshot Saved", "Screenshot saved successfully.")

   

class CVSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.resolution_button = QPushButton("Set Resolution")
        self.resolution_button.clicked.connect(self.setResolution)
        self.layout.addWidget(self.resolution_button)

        self.exposure_button = QPushButton("Set Exposure")
        self.exposure_button.clicked.connect(self.setExposure)
        self.layout.addWidget(self.exposure_button)

        self.focus_button = QPushButton("Set Focus")
        self.focus_button.clicked.connect(self.setFocus)
        self.layout.addWidget(self.focus_button)

        self.brightness_button = QPushButton("Set Brightness")
        self.brightness_button.clicked.connect(self.setBrightness)
        self.layout.addWidget(self.brightness_button)

        self.contrast_button = QPushButton("Set Contrast")
        self.contrast_button.clicked.connect(self.setContrast)
        self.layout.addWidget(self.contrast_button)

        self.saturation_button = QPushButton("Set Saturation")
        self.saturation_button.clicked.connect(self.setSaturation)
        self.layout.addWidget(self.saturation_button)

        self.hue_button = QPushButton("Set Hue")
        self.hue_button.clicked.connect(self.setHue)
        self.layout.addWidget(self.hue_button)

        self.gain_button = QPushButton("Set Gain")
        self.gain_button.clicked.connect(self.setGain)
        self.layout.addWidget(self.gain_button)

        self.WB_button = QPushButton("Set White Balance")
        self.WB_button.clicked.connect(self.setWhiteBalance)
        self.layout.addWidget(self.WB_button)

    def setResolution(self):
        pass

    def setExposure(self):
        expo = int(input("exposure value: "))
        self.set(cv.CAP_PROP_AUTO_EXPOSURE,0)
        self.set(cv.CAP_PROP_EXPOSURE, expo)
        pass

    def setFocus(self):
        focus = float(input("focus value: "))
        self.set(cv.CAP_PROP_AUTOFOCUS,0)
        self.set(cv.CAP_PROP_FOCUS, focus)
        pass

    def setBrightness(self):
        bright = int(input("brightness value: "))
        self.set(cv.CAP_PROP_BRIGHTNESS,bright)
        pass

    def setContrast(self):
        contrast = int(input("contrast value: "))
        self.set(cv.CAP_PROP_CONTRAST,contrast)
        pass

    def setSaturation(self):
        saturation = int(input("saturation value: "))
        self.set(cv.CAP_PROP_SATURATION,saturation)
        pass

    def setHue(self):
        hue = int(input("hue value: "))
        self.set(cv.CAP_PROP_HUE,hue)
        pass

    def setGain(self):
        gain = int(input("gain value: "))
        self.set(cv.CAP_PROP_GAIN,gain)
        pass

    def setWhiteBalance(self):
        wb = int(input("WB value: "))
        self.set(cv.CAP_PROP_WB_TEMPERATURE,wb)
        pass

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.video_tab = VideoPlayer()
        self.cv_settings_tab = CVSettings()

        self.central_widget.addTab(self.video_tab, "Video Player")
        self.central_widget.addTab(self.cv_settings_tab, "CV Settings")

        self.setWindowTitle("OpenCV Computer Vision App")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
