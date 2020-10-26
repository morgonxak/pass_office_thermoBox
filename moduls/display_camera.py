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
import face_recognition

from moduls.camera import Camera


class Display(QThread):
    #signal_frame_RGB = pyqtSignal([QPixmap,bool])
    signal_frame_RGB = pyqtSignal(QPixmap)
    if_signal_frame_RGB = pyqtSignal(bool)

    def __init__(self, settings: Settings):
        QThread.__init__(self)
        self.settings = settings
        self.cam = Camera(self.settings.settings['ID_CARARA'])
        self.frame_acquisition_mode = True
        self.current_frame = None
        #self.if_current_frame = False
        
    def get_frame(self):
        '''
        Отдает текущий кадр
        :return:
        '''
        return self.current_frame

    def run(self):
        while self.frame_acquisition_mode:
            frame = self.cam.get_frame()
            

            
            frame1 = numpy.copy(frame)
            
            gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            faces1 = face_recognition.face_locations(gray)
            i_if = 0 
            x= y= w= h=0
            for (x1 , y1 , w1 , h1) in faces1:
                i_if +=1
                x , y , w , h = x1 , y1 , w1 , h1
            #self.if_current_frame = (i_if == 1)   
            cv2.rectangle(frame1, (y, x), (h,  w), (255, 0, 0), 2)#вывод квадр
            
            self.current_frame = numpy.copy(frame)
            frame1 = cv2.flip(frame1,1) # ореентация камеры
            frame_pixMap = self.__converterNumpyAraayToPixMap(frame1)  #вывод на экран
            
            
            #self.signal_frame_RGB.emit([frame_pixMap, i_if == 1])
            self.signal_frame_RGB.emit(frame_pixMap)
            self.if_signal_frame_RGB.emit(i_if == 1)


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