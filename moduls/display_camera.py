# -*- coding: utf-8 -*-
## -*- coding: utf-8 -*-
import os
import sys
import numpy
from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange, QSpinBox
from moduls.main_form import Ui_MainWindow
from moduls.database import DataBase
import json
import qimage2ndarray
import gc
import cv2
import queue
import pickle
from moduls.settings import Settings

from moduls.camera import Camera


class Display(QThread):
    signal_frame_RGB = pyqtSignal(QPixmap)

    def __init__(self, settings: Settings):
        QThread.__init__(self)
        self.settings = settings
        self.cam = Camera(self.settings.settings['ID_CARARA'])
        self.frame_acquisition_mode = True
        self.current_frame = None

    def get_frame(self):
        '''
        Отдает текущий кадр
        :return:
        '''
        return self.current_frame

    def run(self):
        while self.frame_acquisition_mode:
            frame = self.cam.get_frame()
            self.current_frame = numpy.copy(frame)

            frame_pixMap = self.__converterNumpyAraayToPixMap(frame)
            self.signal_frame_RGB.emit(frame_pixMap)


    def __converterNumpyAraayToPixMap(self, NumpyArray):
        '''
        Конвертирует Numpy массив в PixMap
        :param NumpyArray:
        :return:
        '''
        try:
            pixMapArray = QPixmap.fromImage(qimage2ndarray.array2qimage(NumpyArray))
            return pixMapArray
        except ValueError:
            print("error")
            return None


    def __del__(self):
        self.frame_acquisition_mode = False
        gc.collect()
        self.cam.release