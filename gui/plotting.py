import sys
import cv2 as cv
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QTabWidget, QFileDialog, QInputDialog, QRadioButton, QFrame
from PyQt5.QtWidgets import QDialog, QPushButton, QMessageBox, QSlider,QFrame
import configparser
from PyQt5 import uic, QtWidgets
import cv2 as cv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import datetime
import csv
import serial, threading

from Camera import Camera

class DataCollectionThread(threading.Thread):
    def __init__(self, delay, amount):
        super().__init__()
        self.delay = delay
        self.amount = amount
        self.collect_data = True
        self.csv_filename = None

    def run(self):
        try:
            ser = serial.Serial('COM7', baudrate=115200)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            self.csv_filename = f"sensor_data_{timestamp}.csv"

            with open(self.csv_filename, mode='w', newline='') as csv_file:
                for i in range(int(self.amount)):
                    if not self.collect_data:
                        break 

                    serial_data = ser.readline().decode('ascii')
                    split_values = serial_data.split("#")
                    int_values = [int(value) for value in split_values]
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(int_values)
        except Exception as e:
            print(f"Error: {str(e)}")

class SecondWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('/media/Backup/Teh/fix banget/config.ui', self)
        self.initUI()
        self.cam_setting = {}
        

    def initUI(self):
        self.cam = Camera()
        self.main = Ui_MainWindow()

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
        self.applyButton = self.findChild(QPushButton, 'applyButton')
        self.applyButton.clicked.connect(self.applyConfig)
        self.cancelButton.clicked.connect(self.close)
        

    def updateExposureLabel(self, value):
        self.label_exposure.setText(f"Exposure: {value}")
        self.slider_values['exposure'] = value
        self.applyCameraSetting('exposure',value)


    def updateSaturationLabel(self, value):
        self.label_saturation.setText(f"Saturation: {value}")
        self.slider_values['saturation'] = value
        self.applyCameraSetting('exposure',value)


    def updateWhiteBalanceLabel(self, value):
        self.label_whitebalance.setText(f"Whitebalance: {value}")
        self.slider_values['white_balance'] = value
        self.applyCameraSetting('whitebalance',value)


    def updateSharpnessLabel(self, value):
        self.label_sharpness.setText(f"Sharpness: {value}")
        self.slider_values['sharpness'] = value
        self.applyCameraSetting('sharpness',value)


    def updateGainLabel(self, value):
        self.label_gain.setText(f"Gain: {value}")
        self.slider_values['gain'] = value
        self.applyCameraSetting('gain',value)


    def updateZoomLabel(self, value):
        self.label_zoom.setText(f"Zoom: {value}")
        self.slider_values['zoom'] = value
        self.applyCameraSetting('zoom',value)


    def updateFocusLabel(self, value):
        self.label_focus.setText(f"Focus: {value}")
        self.slider_values['focus'] = value
        self.applyCameraSetting('focus',value)


    def updatePanLabel(self, value):
        self.label_pan.setText(f"Pan: {value}")
        self.slider_values['pan'] = value
        self.applyCameraSetting('pan',value)


    def updateTiltLabel(self, value):
        self.label_tilt.setText(f"Tilt: {value}")
        self.slider_values['tilt'] = value
        self.applyCameraSetting('tilt',value)


    def updateBrightnessLabel(self, value):
        self.label_brightness.setText(f"Brightness: {value}")
        self.slider_values['brightness'] = value
        self.applyCameraSetting('brightness',value)


    def updateContrastLabel(self, value):
        self.label_contrast.setText(f"Contrast: {value}")
        self.slider_values['contrast'] = value
        self.applyCameraSetting('contrast',value)
    
    def applyCameraSetting(self, parameter_name, value):
        if parameter_name == 'exposure':
            self.main.video_capture.set(cv.CAP_PROP_EXPOSURE, value)
        elif parameter_name == 'brightness':
            self.main.video_capture.set(cv.CAP_PROP_BRIGHTNESS, value)
        elif parameter_name == 'contrast':
            self.main.video_capture.set(cv.CAP_PROP_CONTRAST, value)
        elif parameter_name == 'saturation':
            self.main.video_capture.set(cv.CAP_PROP_SATURATION, value)
        elif parameter_name == 'sharpness':
            self.main.video_capture.set(cv.CAP_PROP_SHARPNESS, value)
        elif parameter_name == 'whitebalance':
            self.main.video_capture.set(cv.CAP_PROP_WB_TEMPERATURE, value)
        elif parameter_name == 'gain':
            self.main.video_capture.set(cv.CAP_PROP_GAIN, value)
        elif parameter_name == 'zoom':
            self.main.video_capture.set(cv.CAP_PROP_ZOOM, value)
        elif parameter_name == 'focus':
            self.main.video_capture.set(cv.CAP_PROP_FOCUS, value)
        elif parameter_name == 'pan':
            self.main.video_capture.set(cv.CAP_PROP_PAN, value)
        elif parameter_name == 'tilt':
            self.main.video_capture.set(cv.CAP_PROP_TILT, value)
    
    # Update the corresponding variable in self.slider_values
        self.slider_values[parameter_name] = value



    def saveSettings(self):
        config = configparser.ConfigParser()
        config['CameraSettings'] = self.slider_values

        with open('default_param.txt', 'w') as configfile:
            config.write(configfile)

        import time
        time.sleep(2) 
        self.show_notification_dialog('Camera parameters saved successfully!')


    def saveSettingsAs(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Camera Settings", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            config = configparser.ConfigParser()
            config['CameraSettings'] = self.slider_values

            with open(file_name, 'w') as configfile:
                config.write(configfile)

    # def setCameraProperties(self,device):
    # Ensure the camera is opened and a valid device is available
        if self.video_capture.isOpened():
            # self.video_capture.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)  # Turn off auto exposure
            # self.video_capture.set(cv.CAP_PROP_AUTO_GAIN, 0)  # Turn off auto gain
            # self.video_capture.set(cv.CAP_PROP_AUTO_WHITE_BALANCE, 0)  # Turn off auto white balance

            # # Set your desired properties here, e.g., exposure, gain, white balance, etc.
            # self.video_capture.set(cv.CAP_PROP_EXPOSURE, self.slider_values['exposure'])
            # self.video_capture.set(cv.CAP_PROP_GAIN, self.slider_values['gain'])
            # self.video_capture.set(cv.CAP_PROP_WHITE_BALANCE_BLUE_U, self.slider_values['white_balance'])
            device.set(cv.CAP_PROP_AUTOFOCUS,0)
            device.set(cv.CAP_PROP_AUTO_WB,0)
            device.set(cv.CAP_PROP_AUTO_EXPOSURE,0)
            self.show_notification_dialog('Camera properties applied!')
        else:
            print("No capture device")

    def applyConfig(self):
        # self.setCameraProperties()
        # self.cam.AutoOff(device)
        # self.cam.getSettings()
        # self.cam.setSettings(device)
        
        # device.set(cv.CAP_PROP_BRIGHTNESS, self.cam_setting['brightness'])
        # device.set(cv.CAP_PROP_CONTRAST, self.cam_setting['contrast'])
        # device.set(cv.CAP_PROP_SATURATION, self.cam_setting['saturation'])
        # device.set(cv.CAP_PROP_SHARPNESS, self.cam_setting['sharpness'])
        # device.set(cv.CAP_PROP_WB_TEMPERATURE, self.cam_setting['white_balance'])
        # device.set(cv.CAP_PROP_GAIN, self.cam_setting['gain'])
        # device.set(cv.CAP_PROP_ZOOM, self.cam_setting['zoom'])
        # device.set(cv.CAP_PROP_FOCUS, self.cam_setting['focus'])
        # device.set(cv.CAP_PROP_EXPOSURE, self.cam_setting['exposure'])
        # device.set(cv.CAP_PROP_PAN, self.cam_setting['pan'])
        # device.set(cv.CAP_PROP_TILT, self.cam_setting['tilt'])

        # self.cam.setSettings(self.slider_values)  
        # self.cam.setSettings(device)

        # Ensure the camera is opened and a valid device is available
        if self.main.video_capture.isOpened():
            # Call the applyConfig method with the current slider values
            self.cam.applyConfig(self.slider_values, self.main.video_capture)
        else:
            print("No capture device")

        self.show_notification_dialog('Camera parameters applied!')
        

    def show_notification_dialog(self, message):
        dialog = QDialog(self)
        dialog.setWindowTitle('Notification')

        layout = QVBoxLayout()
        label = QLabel(message)
        layout.addWidget(label)
        dialog.setLayout(layout)

        dialog.exec_() 

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/media/Backup/Teh/fix banget/vision.ui', self)
        self.initUI()
        self.cam_setting = {}
        self.collect_data = True #data collectin control flag

    def initUI(self):
        self.cam = Camera()
        self.central_widget = QTabWidget()
        self.layout = QVBoxLayout(self.frame)
        self.video_label = QLabel(self.frame)
        self.layout.addWidget(self.video_label)

        self.camera_frame = QFrame()
        self.camera_layout = QVBoxLayout(self.camera_frame)
        self.layout.addWidget(self.camera_frame)
        
        # self.radioButton0 = QRadioButton('Camera 0')
        # self.radioButton1 = QRadioButton('Camera 1')
        # self.radioButton2 = QRadioButton('Camera 2')

        # self.camera_layout.addWidget(self.radioButton0)
        # self.camera_layout.addWidget(self.radioButton1)
        # self.camera_layout.addWidget(self.radioButton2)

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
        self.startSampling.clicked.connect(self.start_collection)
        self.stopSampling.clicked.connect(self.stop_collection)
        self.refreshScreen.clicked.connect(self.clearSerial)
        self.saveSensor.clicked.connect(self.save_collection)
        self.clearCropped.clicked.connect(self.clearCrop)



        self.log_display.setReadOnly(True)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.showTime)
        self.timer2.start(100)

        # Define your other widgets and actions here

        self.path = '/media/Backup/Teh/teststack/default_param.txt'
        self.cam.OpenSettings(self.path)

        self.video_capture = cv.VideoCapture(0, cv.CAP_ANY)
        # self.setCameraProperties(device)

        if not self.video_capture.isOpened():
            self.showNotDetectedDialog()
            return

        self.cam.setSettings(self.video_capture)

        self.preferred_extension = ""

        # self.radioButton0 = QRadioButton("Camera 0")
        # self.radioButton1 = QRadioButton("Camera 1")
        # self.radioButton2 = QRadioButton("Camera 2")

        # self.radioFile0 = QRadioButton("PNG")
        # self.radioFile1 = QRadioButton("JPG")
        # self.radioFile2 = QRadioButton("All Files") 

        # Add a file_layout here
        self.file_frame = QFrame()
        self.file_layout = QVBoxLayout(self.file_frame)
        self.layout.addWidget(self.file_frame)

        # self.file_layout.addWidget(self.radioFile0)
        # self.file_layout.addWidget(self.radioFile1)
        # self.file_layout.addWidget(self.radioFile2)

        # Connect radio button signals
        self.radioButton0.clicked.connect(lambda: self.changeCameraIndex(0))
        self.radioButton1.clicked.connect(lambda: self.changeCameraIndex(1))
        self.radioButton2.clicked.connect(lambda: self.changeCameraIndex(2))

        # self.radioFile0.clicked.connect(lambda: self.setPreferredExtension("png"))
        # self.radioFile1.clicked.connect(lambda: self.setPreferredExtension("jpg"))
        # self.radioFile2.clicked.connect(lambda: self.setPreferredExtension(""))

        # self.screenshot_label = QLabel(self.tab_5)
        

    # def setCameraProperties(self,device):
    # Ensure the camera is opened and a valid device is available
        # if self.video_capture.isOpened():
            # self.video_capture.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)  # Turn off auto exposure
            # # self.video_capture.set(cv.CAP_PROP_AUTO_GAIN, 0)  # Turn off auto gain
            # self.video_capture.set(cv.CAP_PROP_AUTO_WHITE_BALANCE, 0)  # Turn off auto white balance

            # # Set your desired properties here, e.g., exposure, gain, white balance, etc.
            # self.video_capture.set(cv.CAP_PROP_EXPOSURE, self.slider_values['exposure'])
            # # self.video_capture.set(cv.CAP_PROP_GAIN, self.slider_values['gain'])
            # self.video_capture.set(cv.CAP_PROP_WHITE_BALANCE_BLUE_U, self.slider_values['white_balance'])

        #     device.set(cv.CAP_PROP_AUTOFOCUS,0)
        #     device.set(cv.CAP_PROP_AUTO_WB,0)
        #     device.set(cv.CAP_PROP_AUTO_EXPOSURE,0)            

        #     self.show_notification_dialog('Camera properties applied!')
        # else:
        #     print("No capture device")

    def clearSerial(self):
        self.log_display.clear()

    def clearCrop(self):
        self.cropShow.clear()

    def start_collection(self):
        # delay = self.delay_input.text()
        # amount = self.amount_input.text()
        # self.log_display.clear()

        # try:
        #     ser = serial.Serial('COM7', baudrate=115200)
        #     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        #     csv_filename = f"sensor_data_{timestamp}.csv"

        #     with open(csv_filename, mode='w', newline='') as csv_file:
        #         for i in range(int(amount)):
        #             if not self.collect_data:  # cek tadi tombol stopnya kepencet ga
        #                 self.log_display.append("Data collection stopped.")
        #                 break  # Exit  loop

        #             serial_data = ser.readline().decode('ascii')
        #             split_values = serial_data.split("#")
        #             int_values = [int(value) for value in split_values]
        #             csv_writer = csv.writer(csv_file)
        #             csv_writer.writerow(int_values)
        #             self.log_display.append(f"Collected data: {int_values}")
        # except Exception as e:
        #     self.log_display.append(f"Error: {str(e)}")

        # delay = self.delay_input.text()
        # amount = self.amount_input.text()
        # self.log_display.clear()

        # try:
        #     ser = serial.Serial('COM7', baudrate=115200)
        #     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        #     csv_filename = f"sensor_data_{timestamp}.csv"

        #     with open(csv_filename, mode='w', newline='') as csv_file:
        #         for i in range(int(amount)):
        #             if not self.collect_data:  
        #                 self.log_display.append("Data collection stopped.")
        #                 break 

        #             serial_data = ser.readline().decode('ascii')
        #             split_values = serial_data.split("#")
        #             int_values = [int(value) for value in split_values]
        #             csv_writer = csv.writer(csv_file)
        #             csv_writer.writerow(int_values)
        #             self.log_display.append(f"Collected data: {int_values}")
        # except Exception as e:
        #     self.log_display.append(f"Error: {str(e)}")

        # delay = self.delay_input.text()
        # amount = self.amount_input.text()
        # self.log_display.clear()

        # self.data_collection_thread = DataCollectionThread(delay, amount)
        # self.data_collection_thread.start()

        #----
        delay_text = self.delay_input.text()
        amount_text = self.amount_input.text()

        if not delay_text:
            delay_text = "500"  # Default delay of 500 milliseconds

        if not amount_text:
            amount_text = "360"  # Default amount of 360 data points

        delay = int(delay_text)
        amount = int(amount_text)
        # delay = self.delay_input.text()
        # amount = self.amount_input.text()
        self.log_display.clear()

        try:
            ser = serial.Serial('COM7', baudrate=115200)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            csv_filename = f"sensor_data_{timestamp}.csv"

            with open(csv_filename, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                titles = ['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6']
                csv_writer.writerow(titles)
                
                for i in range(int(amount)):
                    if not self.collect_data:
                        self.log_display.append("Data collection stopped.")
                        break
                    
                    serial_data = ser.readline().decode('ascii')
                    split_values = serial_data.split("#")
                    int_values = [int(value) for value in split_values]
                    
                    csv_writer.writerow(int_values)
                    self.log_display.append(f"Collected data: {int_values}")
        except Exception as e:
            self.log_display.append(f"Error: {str(e)}")


    def stop_collection(self):
        self.collect_data = False  
        self.log_display.append("stopping data collection")
    
    def save_collection(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        csv_filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if csv_filename:
            try:
                ser = serial.Serial('COM7', baudrate=115200)
                with open(csv_filename, mode='w', newline='') as csv_file:
                    while True:
                        if not self.collect_data:  
                            self.log_display.append("Data collection stopped.")
                            break 

                        serial_data = ser.readline().decode('ascii')
                        split_values = serial_data.split("#")
                        int_values = [int(value) for value in split_values]
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(int_values)
                        self.log_display.append(f"Collected data: {int_values}")
            except Exception as e:
                self.log_display.append(f"Error: {str(e)}")

        # if self.data_collection_thread and self.data_collection_thread.csv_filename:
        #     options = QFileDialog.Options()
        #     options |= QFileDialog.DontUseNativeDialog
        #     csv_filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv);;All Files (*)", options=options)

        #     if csv_filename:
        #         import shutil
        #         shutil.move(self.data_collection_thread.csv_filename, csv_filename)
        #         self.log_display.append(f"Data saved as {csv_filename}")

    def showNotDetectedDialog(self):
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('Warning!')
        warning_box.setText('Device is not detected!')
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.exec_()

    def showFailureDialog(self):
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('Warning!')
        warning_box.setText('Capture has failed!')
        warning_box.setStandardButtons(QMessageBox.Ok)

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
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # # file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", f"{self.preferred_extension.upper()} Files (*.{self.preferred_extension});;All Files (*)", options=options)
        # file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG Files (*.jpg);;All Files (*)", options=options)

        # cv.imwrite(file_name, image)
        # #filename, array

        # if file_name:
        #     print(f"Image saved as {file_name}")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG Files (*.jpg);;All Files (*)", options=options)
        extention = ".jpg"

        if file_name:
            ret, frame = self.video_capture.read()
            if ret:
                cv.imwrite((file_name+extention), frame)
            print(f"Image saved as {file_name}")
             
            screenshot_pixmap = QPixmap(file_name + extention)
            self.cropShow.setPixmap(screenshot_pixmap)

        # screenshot_pixmap = QPixmap(file_name + extension)
        # screenshot_label.setPixmap(screenshot_pixmap)

        # # Show the second frame
        # second_frame.show()
        
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