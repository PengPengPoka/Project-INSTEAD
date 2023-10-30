import sys
import cv2 as cv
from PyQt5.QtCore import QTimer, QTime, QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QTabWidget, QFileDialog, QInputDialog, QRadioButton, QFrame
from PyQt5.QtWidgets import QDialog, QPushButton, QMessageBox, QSlider,QFrame
import configparser
from PyQt5 import uic, QtWidgets
import cv2 as cv
import sys
from PyQt5.QtCore import QRunnable, QObject, QThreadPool, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import datetime
import csv, re
import serial, threading
import subprocess
# import multiprocessingq
import serial
import datetime
import csv
import multiprocessing
import serial.tools.list_ports
import os
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from io import StringIO
import serial
import serial.tools.list_ports
import datetime
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import serial
import datetime
import time
import threading
import os
import sys
import threading
import serial
import datetime
import csv
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from tqdm import tqdm
from PyQt5 import QtCore,QtWidgets

from Camera import Camera

sampling_active = False

class DataSamplingThread(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(str)
    def __init__(self, delay, amount):
        super().__init__()
        self.delay = delay
        self.amount = amount    

    def run(self):
        for i in range(1):
            self.update_signal.emit("Searching for COM ports...")
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                try:
                    # self.update_signal.emit('Found port ' + port.device, port.serial_number)
                    self.update_signal.emit('Found port ' + port.device + ' ' + port.serial_number) 
                    ser = serial.Serial(port.device, 115200, timeout=1)
                    ser.flush()
                    self.update_signal.emit('Connect ' + ser.name)

                    data_to_test = f"{60}#{1}\n"
                    ser.write(data_to_test.encode())
                    serial_data_test = ser.readline().decode('ascii')
                    if serial_data_test == '':
                        self.update_signal.emit("Wrong COM port")
                        raise Exception("Wrong COM port")
                    split_values_test = serial_data_test.split("#")
                    int_values_test = [int(value) for value in split_values_test]
                    if len(int_values_test) < 6:
                        self.update_signal.emit("Wrong COM port")
                        raise Exception("Wrong COM port")

                except:
                    self.update_signal.emit("error")
                    ser.close()
                    continue

                data_to_send = f"{self.delay}#{self.amount}\n"
                ser.write(data_to_send.encode())
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                csv_filename = f"sensor_data_{timestamp}_BOHEA_2_1-{i+1}.csv"

                with open(csv_filename, mode='w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    header = ["Sensor 1", "Sensor 2", "Sensor 3",
                              "Sensor 4", "Sensor 5", "Sensor 6"]
                    csv_writer.writerow(header)

                    # for i in range(int(self.amount)):
                    #     serial_data = ser.readline().decode('ascii')    # read serial data from usb
                    #     split_values = serial_data.split("#")   # split values by #
                    #     int_values = [int(value) for value in split_values]
                    #     # for i in range(6):
                    #     # int_values[i] = round((int_values[i]*3.3/65536), 3)
                    #     print(i+1, int_values)  # Output: [123, 456, 789]
                    #     csv_writer = csv.writer(csv_file)
                    #     csv_writer.writerow(int_values)  # append data to csv file
                    
                   
                    for j in tqdm(range(self.amount), desc=f'Progress ({ser.name})', leave=False):
                        serial_data = ser.readline().decode('ascii')
                        split_values = serial_data.split("#")
                        if len(split_values) != 6:
                            self.update_signal.emit("Received incomplete data:", split_values)
                            continue
                        int_values = [int(value) for value in split_values]
                        # self.data_received.emit(j+1,Sint_values)
                        # print(j + 1, int_values)
                        self.update_signal.emit(f'{j+1} {int_values}\n')
                        csv_writer.writerow(int_values)

                    ser.close()
                    break



class TextStream(StringIO):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def write(self, text):
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.insertPlainText(text)
        self.text_edit.moveCursor(QTextCursor.End)



class DataCollector(QObject):
    data_collected = pyqtSignal(list)

    def __init__(self, delay, amount):
        super().__init__()
        self.delay = delay
        self.amount = amount
        self.collect_data = False
        self.sensor_number = None
        self.serial_port = None

    def start_collection(self):
        global sampling_active
        sampling_active = True

        for sensor_number in range(1, 7):
            try:
                print("Searching for COM ports...")
                ports = list(serial.tools.list_ports.comports())
                for port in ports:
                    try:
                        print('Found port ' + port.device, port.serial_number)
                        ser = serial.Serial(port.device, 115200, timeout=1)
                        ser.flush()
                        print('Connect ' + ser.name)

                        data_to_test = f"{60}#{1}\n"  # data format
                        ser.write(data_to_test.encode())  # send data to usb
                        serial_data_test = ser.readline().decode('ascii')
                        if serial_data_test == '':
                            print("Wrong COM port")
                            raise Exception("Wrong COM port")
                        split_values_test = serial_data_test.split("#")  # split values by #
                        int_values_test = [int(value) for value in split_values_test]
                        if len(int_values_test) < 6:
                            print("Wrong COM port")
                            raise Exception("Wrong COM port")

                        self.serial_port = ser

                    except Exception as e:
                        print(f"Error: {str(e)}")
                        ser.close()
                        continue

                # for _ in range(self.amount):
                #     if not self.collect_data:
                #         break
                while self.collect_data:
                    if not sampling_active:
                        break

                    data_to_send = f"{self.delay}#{self.amount}\n"  # data format
                    self.serial_port.write(data_to_send.encode())  # send data to USB

                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                    csv_filename = f"sensor_data_{timestamp}_BOHEA_AMPAS_6-{self.sensor_number}.csv"

                    with open(csv_filename, mode='w', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        header = ["Sensor 1", "Sensor 2", "Sensor 3",
                                "Sensor 4", "Sensor 5", "Sensor 6"]
                        csv_writer.writerow(header)

                        serial_data = self.serial_port.readline().decode('ascii')  # read serial data from USB
                        while serial_data:
                            split_values = serial_data.split("#")  # split values by #
                            int_values = [int(value) for value in split_values]
                            csv_writer.writerow(int_values)  # append data to csv file
                            self.data_collected.emit(int_values)  # emit data for UI update
                            serial_data = self.serial_port.readline().decode('ascii')  # read next serial data

            except Exception as e:
                print(f"Error: {str(e)}")
            finally:
                if self.serial_port:
                    self.serial_port.close()

        sampling_active = False

    def stop_collection(self):
        self.collect_data = False

    def is_collecting(self):
        return self.collect_data

class Signals(QObject):
    completed = Signal()
    started = Signal()

class Worker(QRunnable):
    def __init__(self,n):
        super().__init__()
        self.n=n
        self.signals = Signals()

    @Slot()
    def run(self):
        self.signals.started.emit(self.n)
        for i in range(5):
            print("Searching for COM ports...")
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                try:
                    print('Found port ' + port.device, port.serial_number)
                    ser = serial.Serial(port.device, 115200, timeout=1)
                    ser.flush()
                    print('Connect ' + ser.name)

                    data_to_test = f"{60}#{1}\n"  # data format
                    ser.write(data_to_test.encode())  # send data to usb
                    serial_data_test = ser.readline().decode('ascii')
                    if serial_data_test == '':
                        print("Wrong COM port")
                        raise Exception("Wrong COM port")
                    split_values_test = serial_data_test.split(
                        "#")   # split values by #
                    int_values_test = [int(value) for value in split_values_test]
                    if int_values_test.__len__() < 6:
                        print("Wrong COM port")
                        raise Exception("Wrong COM port")

                except:
                    print("error")
                    ser.close()
                    continue

                data_to_send = f"{delay}#{amount}\n"  # data format
                ser.write(data_to_send.encode())  # send data to usb

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                csv_filename = f"sensor_data_{timestamp}_BOHEA_AMPAS_6-{i+1}.csv"

                with open(csv_filename, mode='w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    header = ["Sensor 1", "Sensor 2", "Sensor 3",
                            "Sensor 4", "Sensor 5", "Sensor 6"]
                    csv_writer.writerow(header)
                    for i in range(int(amount)):
                        serial_data = ser.readline().decode('ascii')    # read serial data from usb
                        split_values = serial_data.split("#")   # split values by #
                        int_values = [int(value) for value in split_values]
                        # for i in range(6):
                        # int_values[i] = round((int_values[i]*3.3/65536), 3)
                        print(i+1, int_values)  # Output: [123, 456, 789]
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(int_values)  # append data to csv file
                    ser.close()
                    break

        pass
        self.signals.completed.emit(self.n)


class SecondWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:\\Users\\Lyskq\\Downloads\\gui\\config.ui", self)
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
        uic.loadUi("C:\\Users\\Lyskq\\Downloads\\gui\\vision.ui", self)
        self.initUI()
        self.cam_setting = {}
        self.collect_data = True #data collectin control flag
        self.timer_sensor = True
        self.p1 = None
        global global_self
        global_self = self
        self.serial_port = None
        self.found_port = False
        # self.find_port()
        self.data_collection_thread = None
        self.sample_name = ""
        self.last_name=""
        self.shot_count = 1

        # self.data_collection_thread = None
        self.threadpool = QThreadPool()
        
        pass

    def initUI(self):
        self.data_collector = None
        self.cam = Camera()
        self.central_widget = QTabWidget()
        self.layout = QVBoxLayout(self.frame)
        self.video_label = QLabel(self.frame)
        self.layout.addWidget(self.video_label)

        self.camera_frame = QFrame()
        self.camera_layout = QVBoxLayout(self.camera_frame)
        self.layout.addWidget(self.camera_frame)
        
        self.startButton.clicked.connect(self.togglePlayback)
        # self.snapButton.clicked.connect(self.takeScreenshot)
        self.snapButton.clicked.connect(self.save_filename)


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
        # self.startSampling.clicked.connect(self.start_collection)
        self.startSampling.clicked.connect(self.start_sampling)
        self.startSampling.clicked.connect(self.start_timer)
        # self.startSampling.clicked.connect(self.find_port)
        # self.startSampling.clicked.connect(self.startMulti)
        self.stopSampling.clicked.connect(self.stop_collection)
        self.refreshScreen.clicked.connect(self.clearSerial)
        # self.refreshScreen2.clicked.connect(self.clearSerial)
        # self.saveSensor.clicked.connect(self.save_collection)
        self.clearCropped.clicked.connect(self.clearCrop)

        self.log_display.setReadOnly(True)
        sys.stdout = TextStream(self.log_display)

        
        # self.log_display_2.setReadOnly(True)
        # sys.stdout = TextStream(self.log_display_2)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.showTime)
        self.timer2.start(100)

        self.timer3 = QTimer(self)
        self.time3=QTime(0,0)

        # Define your other widgets and actions here

        self.path = "C:\\Users\\Lyskq\\Downloads\\gui\\default_param.txt"
        self.cam.OpenSettings(self.path)

        self.video_capture = cv.VideoCapture(0, cv.CAP_DSHOW)
        # self.setCameraProperties(device)

        if not self.video_capture.isOpened():
            self.showNotDetectedDialog()
            return

        self.cam.setSettings(self.video_capture)

        self.preferred_extension = ""
        # Add a file_layout here
        self.file_frame = QFrame()
        self.file_layout = QVBoxLayout(self.file_frame)
        self.layout.addWidget(self.file_frame)

        # Connect radio button signals
        self.radioButton0.clicked.connect(lambda: self.changeCameraIndex(0))
        self.radioButton1.clicked.connect(lambda: self.changeCameraIndex(1))
        self.radioButton2.clicked.connect(lambda: self.changeCameraIndex(2))

        
        # self.find_port()

    def update_gui(self,data):
        self.text_edit.append(data)

    def start_sampling(self):
            self.log_display.clear()
            # delay = 60
            # amount = 211

            delay_text = self.delay_input.text()
            amount_text = self.amount_input.text()

            if not delay_text or not amount_text:
                QMessageBox.warning(self, 'Warning', 'Please enter delay and amount values.')
                return

            delay = int(delay_text)
            amount = int(amount_text)



            self.thread = DataSamplingThread(delay, amount)
            self.thread.update_signal.connect(self.update_text_edit)
            self.thread.finished.connect(self.thread_finished)
            self.thread.start()

            # data_thread = DataSamplingThread(delay, amount)
            # data_thread.start() 

    def update_text_edit(self, text):
        self.log_display.append(text)

    def thread_finished(self):
        QMessageBox.information(self, "Data collection","complete")
        self.log_display.append("Data collection completed.")



    def start(self):
        pool = QThreadPool.globalInstance()
        for _ in range(1,100):
            worker=Worker()
            worker.signals.completed.connect(self.update)
            pool.start(Worker())

    def update():
        pass

    def clearSerial(self):
        self.log_display.clear()

    def clearCrop(self):
        self.cropShow.clear()

    # def startMulti(self, delay, amount):
    #     self.p1 = multiprocessing.Process(target=self.start_collection, args=(amount,delay))
    #     self.p1.start()

    # def find_port(self):
    #     if self.found_port:
    #         return  # Port already found and initialized

    #     print("Searching for COM ports...")
    #     ports = list(serial.tools.list_ports.comports())
    #     for port in ports:
    #         try:
    #             print('Found port ' + port.device, port.serial_number)
    #             ser = serial.Serial(port.device, 115200, timeout=1)
    #             ser.flush()
    #             print('Connect ' + ser.name)

    #             data_to_test = f"{60}#{1}\n"  # data format
    #             ser.write(data_to_test.encode())  # send data to USB
    #             serial_data_test = ser.readline().decode('ascii')
    #             if serial_data_test == '':
    #                 print("Wrong COM port")
    #                 raise Exception("Wrong COM port")
    #             split_values_test = serial_data_test.split(
    #                 "#")   # split values by #
    #             int_values_test = [int(value) for value in split_values_test]
    #             if len(int_values_test) < 6:
    #                 print("Wrong COM port")
    #                 raise Exception("Wrong COM port")

    #             # If we reached this point, we found the correct port
    #             self.serial_port = ser
    #             self.found_port = True
    #             return

    #         except Exception as e:
    #             print(f"Error: {str(e)}")
    #             ser.close()
    #             continue

    def start_collection(self):
        global sampling_active

        if not sampling_active:
            delay_text = self.delay_input.text()
            amount_text = self.amount_input.text()

            if not delay_text or not amount_text:
                QMessageBox.warning(self, 'Warning', 'Please enter delay and amount values.')
                return

            delay = int(delay_text)
            amount = int(amount_text)

            self.data_collection_thread = DataCollector(delay, amount)
            self.data_collection_thread.data_collected.connect(self.handle_data_collected)

            runnable = DataCollectionRunnable(self.data_collection_thread)
            self.threadpool.start(runnable)
        else:
            QMessageBox.warning(self, 'Warning', 'Sampling process is already active.')


        # if self.data_collector and self.data_collector.is_collecting():
        #     print("Data collection is already running.")
        # else:
        #     delay_text = self.delay_input.text()
        #     amount_text = self.amount_input.text()

        #     if not delay_text:
        #         delay_text = "16"  # Default 500 ms

        #     if not amount_text:
        #         amount_text = "3000"  # Default 360

        #     global amount
        #     global delay
        #     amount = int(amount_text)
        #     delay = int(delay_text)

        #     self.data_collector = DataCollector(delay, amount)
        #     self.data_collector.data_collected.connect(self.handle_data_collected)
        #     self.data_collector.collect_data = True
        #     collector_thread = threading.Thread(target=self.data_collector.start_collection)
        #     collector_thread.start()

    


    def stop_collection(self):
        # self.collect_data = False  
        global sampling_active

        if self.data_collection_thread:
            self.data_collection_thread.stop_collection()
            self.data_collection_thread = None
            sampling_active = False
            self.log_display.append("Data collection stopped.")
        # if self.data_collector:
        #     self.data_collector.stop_collection()
        #     self.data_collector = None
        #     print("Data collection stopped.")
            # self.log_display.append("stopping data collection")

    def handle_data_collected(self):
        # self.log_display.append(f"Collected data: {int_values}")
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

    def start_timer(self):
        self.timer3.timeout.connect(self.update_timer)
        self.timer3.start(1000)

    def stop_timer(self):
        self.timer3.stop()

    def reset_timer(self):
        self.timer3.stop()
        self.time3 = QTime(0, 0)
        # self.sensorTime.setText(self.time3.toString("mm:ss"))

    def update_timer(self):
        self.time3 = self.time3.addSecs(1)
        # self.sensorTime.setText(self.time3.toString("mm:ss"))

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

    def save_filename(self):
        # self.sample_name = self.fileName.text()
        self.sample_name = self.clean_filename(self.fileName.text())
        if not self.sample_name:
            return  

        if self.sample_name != self.last_name:
            self.last_name = self.sample_name
            self.shot_count = 1

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        suggested_file_name = self.get_suggested_file_name()

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", suggested_file_name, "JPEG Files (*.jpg);;All Files (*)", options=options)

        if file_name:
            self.update_shot_count(file_name)
            self.save_image(file_name)
        
    def clean_filename(self, name):
        name = re.sub(r'[\\/:"*?<>|]', '_', name)
        # name = re.sub(r'\s+','_',name)
        name = re.sub(r'\s+',' ',name)
        return name[:100]  


    def update_shot_count(self, file_name):
        directory, file = os.path.split(file_name)

        base_name, ext = os.path.splitext(file)

        if base_name.startswith(self.sample_name):
            parts = base_name.split("_")
            if len(parts) == 2:
                self.shot_count = int(parts[1]) + 1
        else:
            self.shot_count = 1

    def get_suggested_file_name(self):
        test_shot = f"{self.shot_count}"
        base_name = f"{self.sample_name}"
        # while os.path.exists(f"{base_name}.jpg"):
        #     self.shot_count += 1
        #     base_name = f"{self.sample_name}_{self.shot_count}"
        # return f"{base_name}.jpg"

        existing_files = [file for file in os.listdir() if re.match(rf"{base_name}_(\d+)\.jpg", file)]
        existing_numbers = [int(re.search(rf"{base_name}_(\d+)\.jpg", file).group(1)) for file in existing_files if re.search(rf"{base_name}_(\d+)\.jpg", file)]

        # print(f"Suggested base_name: {base_name}")
        # print(f"Existing files: {existing_files}")
        # print(f"Existing numbers: {existing_numbers}")
        # print(f"shot {test_shot}")

        # while self.shot_count in existing_numbers:
        #     self.shot_count += 1

        if self.shot_count > 0 :
            if existing_numbers:
                self.shot_count=max(existing_numbers)+1

        return f"{base_name}_{self.shot_count}"

    def save_image(self, file_name):
        ret, frame = self.video_capture.read()
        if ret:
            extension = ".jpg"
            file_name_with_extension = f"{file_name}{extension}"
            cv.imwrite(file_name_with_extension, frame)

            print(f"Image saved as {file_name_with_extension}")
          
            screenshot_pixmap = QPixmap(file_name_with_extension)
            self.cropShow.setPixmap(screenshot_pixmap)

        message = f"Saved as {file_name}\nDirectory: {os.path.dirname(file_name)}"
        QMessageBox.information(self, "File Saved", message)

    def takeScreenshot(self):
        self.sample_name = self.fileName.text()
        if not self.sample_name:
            return  

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", f"{self.sample_name}_{self.shot_count}.jpg", "JPEG Files (*.jpg);;All Files (*)", options=options)

        if file_name:
            directory, file = os.path.split(file_name)

            base_name, ext = os.path.splitext(file)

            if base_name.startswith(self.sample_name):
                parts = base_name.split("_")
                if len(parts) == 2:
                    self.shot_count = int(parts[1]) + 1

            self.shot_count += 1

            ret, frame = self.video_capture.read()
            if ret:
                extension = ".jpg"
                file_name_with_extension = f"{file_name}{extension}"
                cv.imwrite(file_name_with_extension, frame)

                print(f"Image saved as {file_name_with_extension}")
              
                screenshot_pixmap = QPixmap(file_name_with_extension)
                self.cropShow.setPixmap(screenshot_pixmap)

            message = f"Saved as {file_name}\nDirectory: {os.path.dirname(file_name)}"
            QMessageBox.information(self, "File Saved", message)

        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # self.sample_name = self.fileName.text()

        # # file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG Files (*.jpg);;All Files (*)", options=options)
        # file_name, _ = QFileDialog.getSaveFileName(self, "Save Image",  , "JPEG Files (*.jpg);;All Files (*)", options=options)
        # extention = ".jpg"

        # if file_name:
        #     ret, frame = self.video_capture.read()
        #     if ret:
        #         cv.imwrite((file_name+extention), frame)
        #     print(f"Image saved as {file_name}")
              
        #     screenshot_pixmap = QPixmap(file_name + extention)
        #     self.cropShow.setPixmap(screenshot_pixmap)

        # self.shot_count += 1
        # message = f"Saved as {file_name}\nDirectory: {os.getcwd()}"
        # QMessageBox.information(self, "File Saved", message)
        

    def changeCameraIndex(self, index):
        self.video_capture.release()
        self.video_capture = cv.VideoCapture(index)

    def setPreferredExtension(self, extension):
        self.preferred_extension = extension

    def config_action(self):
        sub_window = SecondWindow()
        sub_window.exec_()

class DataCollectionRunnable(QRunnable):
    def __init__(self, data_collector):
        super().__init__()
        self.data_collector = data_collector

    def run(self):
        self.data_collector.start_collection()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # multi_process = Ui_MainWindow()
    window = Ui_MainWindow()
    window.show()

    # window.find_port()
    # p1 = multiprocessing.Process(target=window.start_collection)
    # p1.start()
    
    # thread_pool = QThreadPool()
    # thread_pool.setMaxThreadCount(4)  # Set the number of threads as needed

    # for n in range(4):  # Adjust this range as needed
    #     worker = Worker(n)
    #     worker.signals.completed.connect(window.update)  # Connect the signal to update function
    #     thread_pool.start(worker)  # Start the worker in the thread pool

    
    sys.exit(app.exec_())