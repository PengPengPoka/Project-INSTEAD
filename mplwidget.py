# from PyQt5.QtCore import Qt, pyqtSignal, QObject

# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
# import sys
# import configparser
# import cv2 as cv
# import datetime
# import csv, re
# import os
# import serial
# import numpy as np
# import subprocess
# import serial.tools.list_ports
# from PyQt5.QtCore import QTimer, QTime,QThread, pyqtSignal,QMutex, QMutexLocker
# from PyQt5.QtCore import QThreadPool, pyqtSignal as Signal, pyqtSlot as Slot
# from PyQt5.QtGui import QImage, QPixmap,QTextCursor
# from PyQt5.QtWidgets import QLabel, QVBoxLayout, QTabWidget, QFileDialog, QInputDialog,QFrame, QSizePolicy
# from PyQt5.QtWidgets import QDialog, QPushButton, QMessageBox, QSlider,QFrame
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
# from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel
# from PyQt5 import QtCore,QtWidgets,uic
# from matplotlib import pyplot as plt
# from io import StringIO
# from tqdm import tqdm
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure


# from Camera import Camera
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
# import matplotlib.pyplot as plt

class MplWidget(QWidget):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self.figure)
        self.canvas.axes = self.ax
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

class Aroma(QWidget):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self.figure)
        self.canvas.axes = self.ax
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)