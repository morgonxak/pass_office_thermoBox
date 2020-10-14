import cv2
import numpy

X_DIMENSION = 640
Y_DIMENSION = 480

class Camera:
    '''
    Клас для получения данных с камеры RGB
    '''
    def __init__(self, count_camera=0):
        self.count_camera = count_camera
        self.operating_mode = True  # РЕжим работы потока
        self.frame_acquisition_mode = False  #РЕжим получения кадра

        self.init_camera(self.count_camera)
        self.old_frame = numpy.zeros((X_DIMENSION, Y_DIMENSION))

    def init_camera(self, count):
        '''
        Создает объект камеры с какой считывать данные
        :param count:
        :return:
        '''
        try:
            self.cam = cv2.VideoCapture(count)
        except BaseException as e:
            print("error init camera {}".format(e))
            return -1
        return 0


    def get_id_camers(self):
        '''
        Получить все доступные камеры в системе
        :return:
        '''
        pass

    def getFrame_gen(self):
        while self.operating_mode:
            while self.frame_acquisition_mode:
                ret, img = self.cam.read()
                if ret:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    yield ret, img
                k = cv2.waitKey(10) & 0xff  # 'ESC' для Выхода
                if k == 27:
                    break

    def get_frame(self):
        '''
        Отдает кадр по запросу
        :return:
        '''
        ret, frame = self.cam.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.old_frame = numpy.copy(frame)
        return self.old_frame


    def get_operating_mode(self):
        '''
        Возвращает
        :return:
        '''
        return self.operating_mode

    def get_frame_acquisition_mode(self):
        '''

        :return:
        '''
        return self.frame_acquisition_mode