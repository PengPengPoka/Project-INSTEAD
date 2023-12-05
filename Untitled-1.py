import sys
import configparser
import cv2 as cv
import datetime
import csv, re
import os
import sys
import serial
import numpy as np
import subprocess
import serial.tools.list_ports
from PyQt5.QtCore import QTimer, Qt, QTime,QThread,QDateTime, pyqtSignal,QMutex, QMutexLocker,QThreadPool, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtGui import QImage, QPixmap,QTextCursor, QColor
from PyQt5.QtWidgets import QLabel, QTabWidget, QFileDialog, QInputDialog,QFrame, QSizePolicy,QPushButton,QDialog, QPushButton, QMessageBox, QSlider,QFrame,QSplitter, QLabel, QVBoxLayout,QWidget, QPushButton, QLabel
# from PyQt5.QtWidgets import VBoxLayout
from PyQt5 import QtCore,QtWidgets,uic
from matplotlib import pyplot as plt
from io import StringIO
from tqdm import tqdm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from collections import deque
import numpy as np
import threading
import time
import pandas as pd

from matplotlib.figure import Figure
from Camera import Camera

class RealTimePlot:
    def __init__(self, num_sensors=6, plot_interval=1):
        self.num_sensors = num_sensors
        self.plot_interval = plot_interval

        # Initialize sensor data container
        self.sensor_data = [deque(maxlen=50) for _ in range(num_sensors)]
        self.time_data = deque(maxlen=50)
        
        # Create initial plot
        self.create_plot()

        # Start a separate thread for real-time plotting
        self.plot_thread = threading.Thread(target=self.real_time_plot)
        self.plot_thread.daemon = True
        self.plot_thread.start()

    def get_sensor_reading(self):
        # Replace this function with your actual method to get sensor readings
        return [np.random.rand() for _ in range(self.num_sensors)]

    def create_plot(self):
        plt.ion()  # Turn on interactive mode for real-time plotting
        self.fig, self.ax = plt.subplots()
        self.lines = [self.ax.plot([], label=f"Sensor {i + 1}")[0] for i in range(self.num_sensors)]
        self.ax.legend()
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Sensor Reading')

    def real_time_plot(self):
        while True:
            sensor_readings = self.get_sensor_reading()

            # Update sensor_data container
            for i in range(self.num_sensors):
                self.sensor_data[i].append(sensor_readings[i])

            # Update time_data container
            self.time_data.append(time.time())

            # Update the plot
            self.update_plot()

            time.sleep(self.plot_interval)

    def update_plot(self):
        for i in range(self.num_sensors):
            self.lines[i].set_xdata(np.array(self.time_data))
            self.lines[i].set_ydata(np.array(self.sensor_data[i]))

        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.flush_events()

class AromaPlot(QWidget):
    def __init__(self):
        super(AromaPlot, self).__init__()

        self.figure = Figure()
        self.ax_combined = self.figure.add_subplot(111)
        # self.ax_individual = [self.figure.add_subplot(3, 2, i + 1) for i in range(6)]

        self.button_choose_file = QPushButton("Choose CSV File")
        
        # self.button_choose_file.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.button_choose_file.setFixedSize(200, 40)  

        self.button_choose_file.clicked.connect(self.load_sensor_data)
        self.button_choose_file.setStyleSheet("background-color: #007BFF; color: white; border: none; padding: 10px;")


        # layout = QVBoxLayout()
        # toolbar = NavigationToolbar(self.figure.canvas, self.figure.canvas)
        # toolbar.addAction('save', self.save_plot)
        # layout.addWidget(toolbar)
        # layout.addWidget(self.button_choose_file)
        # layout.addWidget(FigureCanvas(self.figure))
        layout = QVBoxLayout()
        
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        
        toolbar = NavigationToolbar(self.figure.canvas, self)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.button_choose_file, alignment=Qt.AlignCenter)

        layout.addWidget(toolbar)
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)


        self.setLayout(layout)

        # self.DataThread = DataSamplingThread()
        self.line_realtime, = self.ax_combined.plot([], [], label="Real-Time Data")

        self.sensor_data = None
        self.open_csv = False
        self.time_increment = 0.3# Default time increment (1 second)
        self.update_plots()

    def load_sensor_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        csv_name, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options
        )

        if csv_name:
            self.open_csv = not self.open_csv
            self.sensor_data = self.read_csv(csv_name)
            self.update_plots()

    def auto_load_csv(self,csv_filename):
        if self.open_csv == True:
            reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to overwrite?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                print('Overwriting...')
                self.sensor_data = self.read_csv(csv_filename)  
                self.update_plots()

            else:
                print('Cancelled overwrite')
                return
        else:
            self.sensor_data=self.read_csv(self.csvname)
            self.update_plots()

    # def save_plot(self):
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     file_name, _ = QFileDialog.getSaveFileName(
    #         self, "Save Plot", "", "PNG Files (*.png);;All Files (*)", options=options
    #     )

    #     if file_name:
    #         self.figure.savefig(file_name)

    def read_csv(self, csv_name):
        with open(csv_name, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            sensor_data = list(reader)

        return np.array(sensor_data, dtype=float)

    def update_plots(self):
        if self.sensor_data is not None:
            num_rows, num_columns = self.sensor_data.shape

            time_column = np.arange(0, num_rows * self.time_increment, self.time_increment)

            sensor_labels = {
            1: "MQ 7",
            2: "MQ 9",
            3: "TGS 822",
            4: "TGS 2600",
            5: "TGS 2602",
            6: "TGS 2611"
        }


            # Plot combined data
            self.ax_combined.clear()
            
            # for i in range(num_columns):
            #     self.ax_combined.plot(time_column, self.sensor_data[:, i], label=f"Sensor {i + 1}")
            
            for i in range(num_columns):
                sensor_label = sensor_labels.get(i + 1, f"Sensor {i + 1}")
                self.ax_combined.plot(time_column, self.sensor_data[:, i], label=sensor_label)


            self.ax_combined.set_xlabel("Time (s)")
            self.ax_combined.set_ylabel("Sensor Values")
            self.ax_combined.legend()

            # Plot individual data
            # for i in range(num_columns):
            #     self.ax_individual[i].clear()
            #     self.ax_individual[i].plot(time_column, self.sensor_data[:, i], label=f"Sensor {i + 1}")
            #     self.ax_individual[i].set_xlabel("Time (s)")
            #     self.ax_individual[i].set_ylabel("Sensor Values")
            #     self.ax_individual[i].legend()

            self.figure.tight_layout()
            self.figure.canvas.draw()
    
    @Slot(np.ndarray)
    def update_realtime_slot(self, data):
        self.update_realtime(data)
            
    def update_realtime(self, data):
        if data.size > 0:
            num_rows, num_columns = data.shape
            time_column = np.arange(0, num_rows * self.time_increment, self.time_increment)

            # Update Line2D data
            self.line_realtime.set_data(time_column, data)

            # Adjust axis limits if needed
            self.ax_combined.relim()
            self.ax_combined.autoscale_view()

            # Redraw the figure
            self.figure.tight_layout()
            self.figure.canvas.draw()
        
    # def update_realtime(self,data):
    #     if data.size > 0:
    #         # num_columns=data.size
    #         num_rows, num_columns = data.shape
    #         time_column = np.arange(0, num_rows * self.time_increment, self.time_increment)

    #         self.ax_combined.clear()
    #         for i in range(num_columns):
    #             self.ax_combined.plot(time_column, data, label="Real-Time Data")
    #         self.ax_combined.set_xlabel("Time (s)")
    #         self.ax_combined.set_ylabel("Sensor Values")
    #         self.ax_combined.legend()

    #         self.figure.tight_layout()
    #         self.figure.canvas.draw()

    # def update_realtime(self, data):
    #     if data.size > 0:
    #         num_rows, num_columns = data.shape
    #         time_column = np.arange(0, num_rows * self.time_increment, self.time_increment)

    #         self.ax_combined.clear()  # Clear the axes only once
    #         for i in range(num_columns):
    #             self.ax_combined.plot(time_column, data[:, i], label=f"Real-Time Data {i + 1}")

    #         self.ax_combined.set_xlabel("Time (s)")
    #         self.ax_combined.set_ylabel("Sensor Values")
    #         self.ax_combined.legend()

    #         self.figure.tight_layout()
    #         self.figure.canvas.draw()

class DataSamplingThread(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(str)
    data_signal = QtCore.pyqtSignal(np.ndarray)
    repetition_signal = QtCore.pyqtSignal(int)
    filename_signal = QtCore.pyqtSignal(str)

    def __init__(self, delay, amount,repetition,csv_name):
        super().__init__()
        self.delay = delay
        self.amount = amount    
        self.repetition = repetition
        self.csv_name = csv_name


    def run(self):
        default_folder = os.path.expanduser("~\\Documents\\Project_INSTEAD\\") 
        for i in range(self.repetition):
            self.update_signal.emit("Searching for COM ports...")
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                try:
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
                
                self.repetition_signal.emit(i+1)
                data_to_send = f"{self.delay}#{self.amount}\n"
                ser.write(data_to_send.encode())
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                csv_filename = os.path.join(default_folder, f"sensor_data_{timestamp}_{self.csv_name}_{i+1}.csv")
                self.filename_signal.emit(csv_filename)
                self.csvname= csv_filename

                with open(csv_filename, mode='w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    header = ["Sensor 1", "Sensor 2", "Sensor 3",
                              "Sensor 4", "Sensor 5", "Sensor 6"]
                    csv_writer.writerow(header)
                   
                    for j in tqdm(range(self.amount), desc=f'Progress ({ser.name}) Data ({i})', leave=False):
                        serial_data = ser.readline().decode('ascii')
                        split_values = serial_data.split("#")
                        if len(split_values) != 6:
                            self.update_signal.emit(f"Received incomplete data: {split_values}")
                            # self.data_signal.emit(np.ndarray([], dtype=float))

                            continue
                        int_values = [int(value) for value in split_values]

                        self.update_signal.emit(f'{j+1} {int_values}\n')
                        csv_writer.writerow(int_values)
                        # self.data_signal.emit(np.array(int_values))
                        self.data_signal.emit(np.array(int_values))

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

class SecondWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        x = os.path.expanduser("~\\Documents\\Project_INSTEAD\\src\\config.ui") 
        uic.loadUi(x, self)

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

    # Ensure the camera is opened and a valid device is available
        if self.video_capture.isOpened():
            # device.set(cv.CAP_PROP_AUTOFOCUS,0)
            # device.set(cv.CAP_PROP_AUTO_WB,0)
            # device.set(cv.CAP_PROP_AUTO_EXPOSURE,0)
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
    update_lcd_signal = pyqtSignal(int)
    file_name_signal = pyqtSignal(str)
    file_name = ""

    def __init__(self):

        super().__init__()
        vision =os.path.expanduser("~\\Documents\\Project_INSTEAD\\src\\vision_revisi.ui")
        # uic.loadUi("C:\\Users\\Lyskq\\Downloads\\gui\\vision.ui", self)
        uic.loadUi(vision, self)
        self.initUI()
        self.cam_setting = {}
        self.collect_data = True #data collectin control flag
        self.timer_sensor = True
        self.p1 = None
        self.image_active = False

        global global_self
        global_self = self
        self.serial_port = None
        self.found_port = False
        self.data_collection_thread = None
        self.sample_name = ""
        self.last_name=""
        self.file_name = ""
        self.open_csv = False

        self.shot_count = 1

        self.threadpool = QThreadPool()
        self.update_lcd_signal.connect(self.update_repetition_lcd)
        

        self.img_path = None
        self.img = None
        self.x = 0
        self.y = 0
        self.radius = 0

        # self.DataThread = DataSamplingThread()

        self.aroma_widget =AromaPlot()
        self.tabWidget.addTab(self.aroma_widget, "Aroma Analysis")

        splitter = QSplitter(self)
        splitter.addWidget(self.tabWidget)  

        self.setCentralWidget(splitter)
        
        # self.ImageCheck()

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
        
        self.startButton_2.clicked.connect(self.togglePlayback)
        self.startButton.clicked.connect(self.togglePlayback)
        self.snapButton.clicked.connect(self.save_filename)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.playback = False
        
        self.count = 0
        self.start = False
    


        self.camConfig.clicked.connect(self.config_action)
        self.startSampling.clicked.connect(self.start_sampling)
        self.startSampling.clicked.connect(self.start_timer)

        self.refreshScreen.clicked.connect(self.clearSerial)
        self.open_folder.clicked.connect(self.openFolder)
        self.open_folder_2.clicked.connect(self.openFolder)
        self.pixelData.clicked.connect(self.getHist)

        self.log_display.setReadOnly(True)
        sys.stdout = TextStream(self.log_display)
        self.log_display.clear()
        

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.showTime)
        self.timer2.start(100)

        self.timer3 = QTimer(self)
        self.time3=QTime(0,0)

        # Define your other widgets and actions here

        # self.path = "C:\\Users\\Lyskq\\Downloads\\gui\\default_param.txt"
        self.path = os.path.expanduser("~\\Documents\\Project_INSTEAD\\src\\default_param.txt") 
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

        # self.cameraSelect = QtWidgets.QComboBox(self)
        self.cameraSelect.addItem("Camera 1", 0)
        self.cameraSelect.addItem("Camera 2", 1)
        self.cameraSelect.addItem("Camera 3", 2)
        # self.cameraSelect.currentIndexChanged.connect(self.handleCameraSelection)
        # self.cameraSelect.currentIndexChanged.connect(lambda index: self.changeCameraIndex(self.cameraSelect.itemData(index)))
        self.cameraSelect.currentIndexChanged.connect(lambda index: self.changeCameraIndex(index))

        self.xValue.valueChanged.connect(self.update_sliders)
        self.xValue.valueChanged.connect(self.updateXValue)

        self.yValue.valueChanged.connect(self.update_sliders)
        self.yValue.valueChanged.connect(self.updateYValue)

        self.radValue.valueChanged.connect(self.update_sliders)
        self.radValue.valueChanged.connect(self.updateradValue)

        self.x_spin.valueChanged.connect(self.updateXValue)
        self.y_spin.valueChanged.connect(self.updateYValue)
        self.rad_spin.valueChanged.connect(self.updateradValue)

        self.xValue.valueChanged.connect(lambda value: self.x_spin.setValue(value))
        self.yValue.valueChanged.connect(lambda value: self.y_spin.setValue(value))
        self.rad_spin.valueChanged.connect(lambda value: self.radValue.setValue(value))
        self.radValue.valueChanged.connect(lambda value: self.rad_spin.setValue(value))
        self.x_spin.valueChanged.connect(lambda value: self.xValue.setValue(value))
        self.y_spin.valueChanged.connect(lambda value: self.yValue.setValue(value))
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))


        self.openImage.clicked.connect(self.manual_load_image)
        # self.clearCropped_2.clicked.connect(self.clearCrop)
        self.saveResult.clicked.connect(self.saveImage)
        # self.addToolBar(NavigationToolbar(any, self))
        

        

        self.clearCrop()
        self.clearSerial()

        self.image_original = None
        self.image_cropped = None
        




        # self.crop_image()
        # Connect radio button signals
        # self.radioButton0.clicked.connect(lambda: self.changeCameraIndex(0))
        # self.radioButton1.clicked.connect(lambda: self.changeCameraIndex(1))
        # self.radioButton2.clicked.connect(lambda: self.changeCameraIndex(2))

        
    def updateXValue(self, value):
        self.value_x.setText(f'X-Axis: {value}')

    def updateYValue(self, value):
        self.value_y.setText(f'Y-Axis: {value}')
      
    
    def updateradValue(self, value):
        self.value_rad.setText(f'Radius: {value}')
    

    def update_sliders(self):

        if not self.image_active:
            self.imageNotDetectedDialog()
            return

        x = self.xValue.value() 
        y = self.yValue.value()
        radius = self.radValue.value()


        if self.image_original is not None:
            self.image_circle=self.image_original.copy()
            self.image_cropped = self.crop_trackbar(x, y, radius)

            self.display_images()
        self.getHist(self.image_cropped, self.MplWidget.ax)
        self.MplWidget.ax.figure.canvas.draw()

    def crop_trackbar(self, px, py, radius):
        canvas = np.zeros_like(self.image_original)
        cv.circle(canvas, (px, py), radius, [255, 255, 255], cv.FILLED)
        cv.circle(self.image_circle, (px, py), radius, [125, 255, 125], 2)

        cropped = cv.bitwise_and(self.image_original, canvas, mask=None)
        return cropped

    def getHist(self, image, ax):
        ax.clear()
        non_black_mask = np.any(image != [0, 0, 0], axis=2).astype(np.uint8)

        color = ['blue', 'green', 'red']
        for channel, col in enumerate(color):
            histogram = cv.calcHist([image], [channel], mask=non_black_mask, histSize=[256], ranges=[0, 256])
            # ax.plot(histogram, color=col)
            # ax.plot(histogram, color=col, label=f"Channel {channel + 1}")
            ax.plot(histogram, color=col, label=f"{col.lower()} channel")


            ax.set_xlim(0, 256)

        ax.set_xlabel("RGB values")
        ax.set_ylabel("Pixel Frequency")
        ax.set_title("RGB values")
        ax.legend()


    
    def auto_load_image(self):
        if self.image_source:
            self.image_original = cv.imread(self.image_source)
            self.image_cropped = self.image_original.copy()

            self.image_cropped = cv.cvtColor(self.image_cropped, cv.COLOR_BGR2RGB)
            self.image_original = cv.cvtColor(self.image_original, cv.COLOR_BGR2RGB)
            self.image_active = True
            
            self.update_sliders()
            self.display_images()

    def manual_load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)            

        if file_name:
            self.image_original = cv.imread(file_name)
            self.image_cropped = self.image_original.copy()

            self.image_cropped = cv.cvtColor(self.image_cropped, cv.COLOR_BGR2RGB)
            self.image_original = cv.cvtColor(self.image_original, cv.COLOR_BGR2RGB)
            self.image_active = True
            #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            
            self.update_sliders()
            self.display_images()
    
    def display_images(self):
        if self.image_cropped is not None:
            # height, width, channel = self.image_cropped.shape
            # bytes_per_line = 3 * width
            # # q_image_cropped = QPixmap.fromImage(QImage(self.image_cropped.data, width, height, bytes_per_line, QImage.Format_RGB888))
            # q_image_cropped = QImage(self.image_cropped.data, width, height, bytes_per_line, QImage.Format_RGB888)
            # # self.q_image_cropped = q_image_cropped
            # self.q_image_cropped = QPixmap.fromImage(q_image_cropped)
            # # self.cropShow_2.setPixmap(q_image_cropped)
            # processed_pixmap = self.alphaImage(self.q_image_cropped)
            # self.cropShow_2.setPixmap(processed_pixmap)
            # self.alphaImage=processed_pixmap

            height, width, channel = self.image_cropped.shape
            bytes_per_line = 3 * width
            q_image_cropped = QImage(self.image_cropped.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.q_image_cropped = QPixmap.fromImage(q_image_cropped)
            processed_pixmap = self.alphaImage(self.q_image_cropped)
            self.cropShow_2.setPixmap(processed_pixmap)
            self.processedImage = processed_pixmap  # Store the processed image

        
        if self.image_circle is not None:
            height, width, channel = self.image_circle.shape
            bytes_per_line = 3 * width
            q_img = QImage(self.image_circle.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.cropResult.setPixmap(pixmap)

    def alphaImage(self, q_image_cropped):
        q_image_alpha = QImage(q_image_cropped.size(), QImage.Format_ARGB32)
        q_image_alpha.fill(QColor(0, 0, 0, 0))

        q_img_cropped = q_image_cropped.toImage()

        for i in range(q_img_cropped.height()):
            for j in range(q_img_cropped.width()):
                color = QColor(q_img_cropped.pixel(j, i))
                if color.black() == 0:
                    q_image_alpha.setPixelColor(j, i, QColor(0, 0, 0, 0))
                else:
                    q_image_alpha.setPixelColor(j, i, color)

        q_pixmap_alpha = QPixmap.fromImage(q_image_alpha)
        return q_pixmap_alpha
    
    def saveImage(self):
        self.default_folder = os.path.expanduser("~\\Documents\\Project_INSTEAD\\") 
        default_save_location = os.path.join(self.default_folder, self.getDefaultSaveName())
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", default_save_location, "Images (*.png *.jpg *.bmp *.jpeg)")

        if file_path:
            pixmap = self.processedImage  
            pixmap.save(file_path)

    def getDefaultSaveName(self):
        timestamp = QDateTime.currentDateTime().toString("yyyyMMddhhmmss")
        return f"{timestamp}_image_altered"

    def update_gui(self,data):
        self.text_edit.append(data)

    def start_sampling(self):
            self.log_display.clear()

            delay_text = self.delay_input.text()
            amount_text = self.amount_input.text()
            repetition_text = self.repetition_input.text()

            if not delay_text or not amount_text:
                QMessageBox.warning(self, 'Warning', 'Please enter delay and amount values.')
                return

            delay = int(delay_text)
            amount = int(amount_text)
            repetition = int(repetition_text)


            remainingTime = (((delay* amount)/60000)*repetition)
            self.estimatedTime.display(remainingTime)

            self.sensor_name = f"{self.fileName_csv.text()}"
            csv_name = f"{self.sensor_name}"
            
            if not csv_name:
                return

            aroma_plot = AromaPlot()
            self.thread = DataSamplingThread(delay, amount,repetition,csv_name)

            # aroma_plot.moveToThread(self.thread)
            # self.thread.data_signal.connect(aroma_plot.update_realtime(self,data=np.array(self)))
            # self.thread.data_signal.connect(aroma_plot.update_realtime)
            # self.thread.data_signal.connect(self.update_plot_with_data)
            self.thread.data_signal.connect(aroma_plot.update_realtime_slot)


            self.thread.repetition_signal.connect(self.update_repetition_lcd)
            self.thread.update_signal.connect(self.update_text_edit)
            self.thread.finished.connect(self.thread_finished)
        
            self.thread.start()

    def update_plot_with_data(self, data):
        self.aroma_plot.update_realtime(data)
  
    def update_repetition_lcd(self, repetition_number):
        # Slot to update the LCD number display with the repetition number
        self.repetition_times.display(repetition_number)

    def update_text_edit(self, text):
        self.log_display.append(text)

    def thread_finished(self):
        
        QMessageBox.information(self, "Data collection","complete")
        self.log_display.append("Data collection completed.")
        # self.DataThread.filename_signal.connect(self.aroma_widget.auto_load_csv)
        self.aroma_widget.auto_load_csv()
        # self.file_name_signal.connect()    

    def openFolder(self):
        default_folder = os.path.expanduser("~\\Documents\\Project_INSTEAD\\") 

        if os.path.exists(default_folder):
            subprocess.Popen(['explorer', default_folder])
        else:
            QMessageBox(self, "Folder not found", "the folder doesn't exit, check again")

    def update():
        pass

    def clearSerial(self):
        self.log_display.clear()

    # def clearCrop(self):
    #     self.cropShow.clear()

    def clearCrop(self):
        # self.cropShow.clear()
        self.cropShow_2.clear()
        self.cropResult.clear()


    def handle_data_collected(self):
        # self.log_display.append(f"Collected data: {int_values}")
        self.log_display.append("stopping data collection")

    def showNotDetectedDialog(self):
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('Warning!')
        warning_box.setText('Device is not detected!')
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.exec_()

    def imageNotDetectedDialog(self):
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle('Warning!')
        warning_box.setText('You have no image selected! Please select the image first!') 
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

            # Ui_MainWindow.file_name = file_name
            self.file_name=file_name
            self.file_name_signal.emit(file_name)

            # self.image_processor = ImageProcessor(file_name)
            # self.image_processor.image_processed.connect(self.update_image)
            # self.image_processor.start()
            directory_path = os.path.dirname(file_name)
        
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

        existing_files = [file for file in os.listdir() if re.match(rf"{base_name}_(\d+)\.jpg", file)]
        existing_numbers = [int(re.search(rf"{base_name}_(\d+)\.jpg", file).group(1)) for file in existing_files if re.search(rf"{base_name}_(\d+)\.jpg", file)]

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
            self.image_source=file_name_with_extension
        
            self.auto_load_image()

        message = f"Saved as {file_name}\nDirectory: {os.path.dirname(file_name)}"
        QMessageBox.information(self, "File Saved", message)
        path= {os.path.dirname(file_name)}

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

    def changeCameraIndex(self, index):
        # if self.changeCameraIndex(index) == 0:
        #     self.changeCameraIndex(1)
        
        self.video_capture.release()
        self.deviceSelected.setText(f'Device: {index+1}')
        if index == 0:
            index =1
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