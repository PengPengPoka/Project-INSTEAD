import sys
import cv2 as cv
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QTabWidget, QFileDialog, QInputDialog, QRadioButton, QFrame
from PyQt5.QtWidgets import QDialog, QPushButton, QMessageBox, QSlider,QFrame
import configparser
from PyQt5 import uic, QtWidgets
import cv2 as cv

from Camera import Camera

class SecondWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('/media/Backup/Teh/fix/pasti/config.ui', self)
        self.initUI()
        self.cam_setting = {}

    def initUI(self):
        self.cam = Camera()

        self.frame= QFrame()
        # self.central_widget = QTabWidget()
        self.layout = QVBoxLayout(self.frame)
        self.video_label = QLabel(self.frame)
        self.layout.addWidget(self.video_label)

        self.slider_values = {'exposure': -4, 'brightness': 128, 'contrast': 128, 'saturation': 128, 'sharpness': 128, 'white_balance': 4000, 'gain': 0, 'zoom': 100, 'focus': 35, 'pan': 0, 'tilt': 0}

        self.slider_exposure = self.findChild(QSlider, 'slider_exposure')
        self.slider_contrast = self.findChild(QSlider, 'slider_contrast')
        self.slider_saturation = self.findChild(QSlider, 'slider_saturation')
        self.slider_sharpness = self.findChild(QSlider, 'slider_sharpness')
        self.slider_whitebalance = self.findChild(QSlider, 'slider_whitebalance')
        self.slider_gain = self.findChild(QSlider, 'slider_gain')
        self.slider_zoom = self.findChild(QSlider, 'slider_zoom')
        self.slider_focus = self.findChild(QSlider, 'slider_focus')
        self.slider_pan = self.findChild(QSlider, 'slider_pan')
        self.slider_tilt = self.findChild(QSlider, 'slider_tilt')
        self.slider_brightness = self.findChild(QSlider, 'slider_brightness')

        self.label_exposure = self.findChild(QLabel, 'label_exposure')
        self.label_contrast = self.findChild(QLabel, 'label_contrast')
        self.label_saturation = self.findChild(QLabel, 'label_saturation')
        self.label_sharpness = self.findChild(QLabel, 'label_sharpness')
        self.label_whitebalance = self.findChild(QLabel, 'label_whitebalance')
        self.label_gain = self.findChild(QLabel, 'label_gain')
        self.label_zoom = self.findChild(QLabel, 'label_zoom')
        self.label_focus = self.findChild(QLabel, 'label_focus')
        self.label_pan = self.findChild(QLabel, 'label_pan')
        self.label_tilt = self.findChild(QLabel, 'label_tilt')
        self.label_brightness = self.findChild(QLabel, 'label_brightness')

        self.saveButton = self.findChild(QPushButton, 'saveButton')
        self.saveasButton = self.findChild(QPushButton, 'saveasButton')

        self.slider_exposure.valueChanged.connect(self.updateExposureLabel)
        self.slider_contrast.valueChanged.connect(self.updateContrastLabel)
        self.slider_saturation.valueChanged.connect(self.updateSaturationLabel)
        self.slider_sharpness.valueChanged.connect(self.updateSharpnessLabel)
        self.slider_whitebalance.valueChanged.connect(self.updateWhiteBalanceLabel)
        self.slider_gain.valueChanged.connect(self.updateGainLabel)
        self.slider_zoom.valueChanged.connect(self.updateZoomLabel)
        self.slider_focus.valueChanged.connect(self.updateFocusLabel)
        self.slider_pan.valueChanged.connect(self.updatePanLabel)
        self.slider_tilt.valueChanged.connect(self.updateTiltLabel)
        self.slider_brightness.valueChanged.connect(self.updateBrightnessLabel)

        self.slider_exposure.setRange(-11, -2)
        self.slider_contrast.setRange(0, 255)
        self.slider_saturation.setRange(0, 255)
        self.slider_sharpness.setRange(0, 255)
        self.slider_whitebalance.setRange(2000, 6500)
        self.slider_gain.setRange(0, 255)
        self.slider_zoom.setRange(100, 500)
        self.slider_focus.setRange(0, 250)
        self.slider_pan.setRange(-10, 10)
        self.slider_tilt.setRange(-10, 10)
        self.slider_brightness.setRange(0, 255)

        self.slider_exposure.setValue(-4)
        self.slider_contrast.setValue(128)
        self.slider_saturation.setValue(128)
        self.slider_sharpness.setValue(128)
        self.slider_whitebalance.setValue(4000)
        self.slider_gain.setValue(0)
        self.slider_zoom.setValue(100)
        self.slider_focus.setValue(35)
        self.slider_pan.setValue(0)
        self.slider_tilt.setValue(0)
        self.slider_brightness.setValue(128)

        self.saveButton.clicked.connect(self.saveSettings)
        self.saveasButton.clicked.connect(self.saveSettingsAs)

    def updateExposureLabel(self, value):
        self.label_exposure.setText(f"Exposure: {value}")
        self.slider_values['exposure'] = value


    def updateSaturationLabel(self, value):
        self.label_saturation.setText(f"Saturation: {value}")
        self.slider_values['saturation'] = value

    def updateWhiteBalanceLabel(self, value):
        self.label_whitebalance.setText(f"Whitebalance: {value}")
        self.slider_values['white_balance'] = value

    def updateSharpnessLabel(self, value):
        self.label_sharpness.setText(f"Sharpness: {value}")
        self.slider_values['sharpness'] = value

    def updateGainLabel(self, value):
        self.label_gain.setText(f"Gain: {value}")
        self.slider_values['gain'] = value

    def updateZoomLabel(self, value):
        self.label_zoom.setText(f"Zoom: {value}")
        self.slider_values['zoom'] = value

    def updateFocusLabel(self, value):
        self.label_focus.setText(f"Focus: {value}")
        self.slider_values['focus'] = value

    def updatePanLabel(self, value):
        self.label_pan.setText(f"Pan: {value}")
        self.slider_values['pan'] = value

    def updateTiltLabel(self, value):
        self.label_tilt.setText(f"Tilt: {value}")
        self.slider_values['tilt'] = value

    def updateBrightnessLabel(self, value):
        self.label_brightness.setText(f"Brightness: {value}")
        self.slider_values['brightness'] = value

    def updateContrastLabel(self, value):
        self.label_contrast.setText(f"Contrast: {value}")
        self.slider_values['contrast'] = value

    def saveSettings(self):
        config = configparser.ConfigParser()
        config['CameraSettings'] = self.slider_values

        with open('default_param.txt', 'w') as configfile:
            config.write(configfile)

        notification = QMessageBox(self)
        notification.setWindowTitle("Notification")
        notification.setIcon(QMessageBox.Information)  
        notification.setText("Saved!")
        notification.addButton(QMessageBox.Ok)
        notification.exec_()          

    def saveSettings(self):
        config = configparser.ConfigParser()
        config['CameraSettings'] = self.slider_values

        with open('default_param.txt', 'w') as configfile:
            config.write(configfile)
        

    def saveSettingsAs(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Camera Settings", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            config = configparser.ConfigParser()
            config['CameraSettings'] = self.slider_values

            with open(file_name, 'w') as configfile:
                config.write(configfile)

    # def notificationSaved(self):
    #     notification = QMessageBox(self)
    #     notification.setWindowTitle("Notifikatzion")
    #     notification.setIcon(QMessageBox.Information)  
    #     notification.setText("Saved!")
    #     notification.addButton(QMessageBox.Ok)
    #     notification.exec_()  

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/media/Backup/Teh/vision.ui', self)
        self.initUI()
        self.cam_setting = {}

    def initUI(self):
        self.cam = Camera()
        self.central_widget = QTabWidget()
        self.layout = QVBoxLayout(self.frame)
        self.video_label = QLabel(self.frame)
        self.layout.addWidget(self.video_label)

        self.camera_frame = QFrame()
        self.camera_layout = QVBoxLayout(self.camera_frame)
        self.layout.addWidget(self.camera_frame)
        
        self.radioButton0 = QRadioButton('Camera 0')
        self.radioButton1 = QRadioButton('Camera 1')
        self.radioButton2 = QRadioButton('Camera 2')

        self.camera_layout.addWidget(self.radioButton0)
        self.camera_layout.addWidget(self.radioButton1)
        self.camera_layout.addWidget(self.radioButton2)

        self.startButton.clicked.connect(self.togglePlayback)
        self.snapButton.clicked.connect(self.takeScreenshot)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.playback = False
        
        self.count = 0
        self.start = False
        self.button.clicked.connect(self.get_seconds)
        self.start_button.clicked.connect(self.start_action)
        self.pause_button.clicked.connect(self.pause_action)
        self.reset_button.clicked.connect(self.reset_action)
        self.camConfig.clicked.connect(self.config_action)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.showTime)
        self.timer2.start(100)

        # Define your other widgets and actions here

        self.path = '/media/Backup/Teh/teststack/default_param.txt'
        self.cam.OpenSettings(self.path)

        self.video_capture = cv.VideoCapture(0, cv.CAP_ANY)

        if not self.video_capture.isOpened():
            self.showNotDetectedDialog()
            return

        self.cam.setSettings(self.video_capture)

        self.preferred_extension = ""

        # self.radioButton0 = QRadioButton("Camera 0")
        # self.radioButton1 = QRadioButton("Camera 1")
        # self.radioButton2 = QRadioButton("Camera 2")

        self.radioFile0 = QRadioButton("PNG")
        self.radioFile1 = QRadioButton("JPG")
        self.radioFile2 = QRadioButton("All Files") 

        # Add a file_layout here
        self.file_frame = QFrame()
        self.file_layout = QVBoxLayout(self.file_frame)
        self.layout.addWidget(self.file_frame)

        self.file_layout.addWidget(self.radioFile0)
        self.file_layout.addWidget(self.radioFile1)
        self.file_layout.addWidget(self.radioFile2)

        # Connect radio button signals
        self.radioButton0.clicked.connect(lambda: self.changeCameraIndex(0))
        self.radioButton1.clicked.connect(lambda: self.changeCameraIndex(1))
        self.radioButton2.clicked.connect(lambda: self.changeCameraIndex(2))

        self.radioFile0.clicked.connect(lambda: self.setPreferredExtension("png"))
        self.radioFile1.clicked.connect(lambda: self.setPreferredExtension("jpg"))
        self.radioFile2.clicked.connect(lambda: self.setPreferredExtension(""))



    def showNotDetectedDialog(self):
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('Warning!')
        warning_box.setText('Device is not detected!')
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.exec_()


    def showFailureDialog(self):
        # Create a warning message box
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('Warning!')
        warning_box.setText('Capture has failed!')
        warning_box.setStandardButtons(QMessageBox.Ok)

        # Execute the warning message box
        warning_box.exec_()

    def showTime(self):
        if self.start:
            self.count -= 1

            if self.count == 0:
                self.start = False
                self.label.setText("Completed !!!! ")

        if self.start:
            text = str(self.count / 10) + " s"
            self.label.setText(text)

    def get_seconds(self):
        self.start = False
        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')
        if done:
            self.count = second * 10
            self.label.setText(str(second))

    def start_action(self):
        self.start = True
        if self.count == 0:
            self.start = False

    def pause_action(self):
        self.start = False

    def reset_action(self):
        self.start = False
        self.count = 0
        self.label.setText("timer?")

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
            self.timer.start(30)
        self.playback = not self.playback

    def takeScreenshot(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", f"{self.preferred_extension.upper()} Files (*.{self.preferred_extension});;All Files (*)", options=options)

        if file_name:
            print(f"Image saved as {file_name}")

    def changeCameraIndex(self, index):
        self.video_capture.release()
        self.video_capture = cv.VideoCapture(index)

    def setPreferredExtension(self, extension):
        self.preferred_extension = extension

    def config_action(self):
        sub_window = SecondWindow()
        sub_window.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())