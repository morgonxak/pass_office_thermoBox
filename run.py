# -*- coding: utf-8 -*-
## -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
В классе воспроизведения попробывать исправить if status поставить перед цыклом
'''

import os
import sys
import paramiko
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidgetSelectionRange
from moduls.main_form import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from moduls.database import DataBase
import qimage2ndarray
import gc
import cv2
import pickle
from moduls.settings import Settings
from moduls.display_camera import Display
from moduls.vievs_moduls.windows_update_user import Windows_update_user


class controller():

    def __init__(self, settings:Settings):
        
        self.settings = settings 
        self.settings.load() # чтение словаря

        self._app = QtWidgets.QApplication(sys.argv)
        self._view = mainForm() # окно
        self._view.mainForm = self
        

        self.dataBase = DataBase(self.settings.settings['PATH_DATA_BASE']) # подключение бд по путир
        
        self.display = None

        self.last_photo = []  #Хранит сделанные фотографии пользователей

        self._view.pull_data_table(self.get_data_of_dataBase()) # из бд в табл

        self.init_button() # присвоение действий к кнопам

    def display_on(self, on = True):
        if on:
            if self.display == None:

                self.display = Display(self.settings) # изображение с камеры
                self.display.signal_frame_RGB.connect(self._view.showGraphicsViewRGB)
                self.display.start()
                #self.dialog = Windows_update_user(self._view)
        else:
            if self.display != None:
                if not self.display.isFinished():
                    self.display.__del__()
                self.display.quit()
                self.display = None

    def init_button(self):
        '''
        Инициализация привязок кнопок
        :return:
        '''
        self._view.dialog.signal_update_info_user.connect(self.update_info_user)
        self._view.dialog.signal_delete_PERSON_ID.connect(self.delete_PERSON_ID)
        # поиск
        self._view.ui.pushButton.clicked.connect(self.add_User) #Добавить пользователя
        self._view.ui.pushButton_5.clicked.connect(self._view.search_table) #Найти пользователя
        self._view.ui.pushButton_2.clicked.connect(self._view.onClick_photography_process) #Приступить к фотографированию
        self._view.ui.pushButton_11.clicked.connect(self.onClick_save_to_treneng) #сохранить и обучить
        # фото
        self._view.ui.pushButton_3.clicked.connect(self.onClick_to_make_photo) #Сфотографировать
        self._view.ui.pushButton_4.clicked.connect(self._view.onClick_next) #Далее
        self._view.ui.pushButton_12.clicked.connect(self._view.onClick_cancel) #отмена
        #Сохранение данных
        self._view.ui.pushButton_10.clicked.connect(self._view.onClick_cancel) #Отмена
        self._view.ui.pushButton_9.clicked.connect(self.onCkick_save) #Сохранить
        
        
        

        


    def update_info_user(self, info):
        '''
        Обновляем информацию в базе данных
        :param info:
        :return:
        '''
        print("info['person_id']", info['person_id'])
        if self.dataBase.update_user_by_personId(info['person_id'], info['last_name'], info['first_name'], info['middle_name'], info['mode_skip']) != -1:
            self._view.showMessage("Информация о пользователе изменена")
            self._view.pull_data_table(self.get_data_of_dataBase())
            return 0
        self._view.showMessage("Что то пошло не так")
        return -1
    
    def delete_PERSON_ID(self, info):
        '''
        удаляем пользователя
        :return:
        '''
        print("delete_PERSON_ID ", info['person_id'])
        if self.dataBase.del_user(info['person_id']) != -1:
            self._view.showMessage("Пользователь удалён")
            self._view.pull_data_table(self.get_data_of_dataBase())
            return 0
        self._view.showMessage("Что то пошло не так")
        return -1

    def get_data_of_dataBase(self, count=20):
        '''
        Получаем данные из базы с поьзователями и переформировываем их
        :param count:
        :return:
        '''
        #{'FIRST_NAME': 'Дмитрий', 'LAST_NAME': 'Шумелев', 'MIDDLE_NAME': 'Игоревич',
        # 'ORG_ID': 'd186ffeb-3499-4eb3-844e-cb3f2f7f97fb', 'cardID': '004EF89D'}}

        data = self.dataBase.get_users(count)  # ('038dfb1f-fc43-4ac7-bf4d-55f9d732b59c', 'Шумелев', 'Дмитрий', 'Игореви', 1, None, 0)

        if data == -1:
            self._view.showMessage("Ошибка с базой данных")
            return -1
        data_dict = {}
        for user in data:
            if user[6] == 0:
                status_photo = "Нет"
            else:
                status_photo = "Да"

            temp = {'FIRST_NAME': user[1], 'LAST_NAME': user[2], 'MIDDLE_NAME': user[3], 'MODE_SKIP': user[4], 'STATUS_PHOTO': status_photo}
            data_dict[user[0]] = temp

        return data_dict

    def add_User(self):
        '''
        кнопка добовления пользователй
        :return:
        '''
        LAST_NAME = self._view.ui.lineEdit.text()
        FIRST_NAME = self._view.ui.lineEdit_2.text()
        MIDDLE_NAME = self._view.ui.lineEdit_3.text()
        
        
        if LAST_NAME != '' and FIRST_NAME != '':
            if self.dataBase.add_user(LAST_NAME, FIRST_NAME, MIDDLE_NAME) != -1:
                self._view.showMessage("Пользователь успешно добавлен")
                self._view.pull_data_table(self.get_data_of_dataBase())
        else:
            self._view.showMessage("Введите данные")
    def onClick_to_make_photo(self):
        '''
        Пр нажатии на кнопку сделать фото
        :return:
        '''
        
        self.display_on(True)

        photo = self.display.get_frame()

        self._view.current_info_user['photo'].append(photo)
        self._view.ui.pushButton_3.setText("Сфотографировать №{}".format(len(self._view.current_info_user['photo'])))
        self._view.ui.pushButton_4.setEnabled(True)

    def onCkick_save(self):
        '''
        Сохраняем данные пользователя
        :return:
        '''
        try:
            path_user = os.path.join(self.settings.settings['PATH_DATASET'], self._view.current_info_user['personId'])
            
            if not os.path.isdir(path_user):
                os.mkdir(path_user)
                if not os.path.isdir(os.path.join(path_user, 'RGB')):
                    os.mkdir(os.path.join(path_user, 'RGB'))

            with open(os.path.join(path_user, 'RGB', 'photo.pickl'), 'wb') as f:
                pickle.dump(self._view.current_info_user['photo'], f)

            self.dataBase.update_status_photo_by_personId(self._view.current_info_user['personId'], 1)

        except BaseException as e:
            print("Error save {}".format(e))
            self._view.showMessage("Что то пошло не так")

        self._view.showMessage("Данные успешно сохранены")
        self._view.pull_data_table(self.get_data_of_dataBase())
        self._view.onClick_cancel()

    def onClick_save_to_treneng(self):
        '''
        При нажатии сохранить и обучить
        :return:
        '''
        from sys import platform
        ifplatform = (platform == "linux" or platform == "linux2")
        set_PATH_DATASET = os.path.abspath(self.settings.settings['PATH_DATASET'])
        set_PATH_SAVE_MODEL= os.path.abspath(self.settings.settings['PATH_SAVE_MODEL'])
        #?????????????????
        
        """
        if ifplatform and set_PATH_DATASET.find("\\") !=-1:
            set_PATH_DATASET = set_PATH_DATASET.replace("\\", "/")
            set_PATH_SAVE_MODEL = set_PATH_SAVE_MODEL.replace("\\", "/")
            
        elif not ifplatform and set_PATH_DATASET.find("/") !=-1:
            set_PATH_DATASET = set_PATH_DATASET.replace("/", "\\")
            set_PATH_SAVE_MODEL = set_PATH_SAVE_MODEL.replace("/", "\\")
            
        """
        from expiriments.trening_models_cvm_knn import branch_3

        #from sys import platform
        branch_3(set_PATH_DATASET, set_PATH_SAVE_MODEL)

        #if platform == "linux" or platform == "linux2":
        if ifplatform:
            os.system('nautilus {}'.format(set_PATH_SAVE_MODEL))
        else:
            os.system('explorer.exe {}'.format(set_PATH_SAVE_MODEL))

        self._view.showMessage("Данные успешно сохранены")





        if self._view.diolog_yes_no():
            if self.cp() == -1:
                self._view.showMessage("Что то пошло не так, проверьте IP")
            else:
                self._view.showMessage("Данные были успешно переданны")
                
        self._view.pull_data_table(self.get_data_of_dataBase())
        self._view.onClick_cancel()

    def cp(self):
        try:
            transport = paramiko.Transport((self.settings.settings['IP_RASPBERRY'], 22))
            transport.connect(username='pi', password='asm123')
        except paramiko.ssh_exception.SSHException as e:
            print("error connect: {}".format(e))
            return -1

        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.put(os.path.join(self.settings.settings['PATH_SAVE_MODEL'], 'dataBase_1.pk'), '/home/pi/project/recognition_service_client_simplified/rc/dataBase_1.pk')
        # sftp.put(os.path.join(self.settings.settings['PATH_SAVE_MODEL'], 'svm_model_1.pk'), '/home/pi/project/recognition_service_client_simplified/rc/svm_model_1.pk')

        sftp.put(self.settings.settings['PATH_DATA_BASE'], '/home/pi/project/recognition_service_client_simplified/rc/database')

        sftp.close()
        transport.close()
        return 0

    def run(self):
        '''
        Запускает приложение
        :return:
        '''
        self._view.show()
        return self._app.exec_()

    def __del__(self):
        gc.collect()

class mainForm(QtWidgets.QMainWindow, Ui_MainWindow):
    '''
    Функционал для отображения и для взаимодействия с пользователем
    '''
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow() # гл форма
        self.ui.setupUi(self)
        self.__init_table()
        self.dialog = Windows_update_user(self) # форма редактирования
        self.mainForm = None
        self.current_info_user = {'personId': None, 'last_name': None, 'first_name': None, 'middle_name': None, 'mode_skip': None, 'photo': []}

        self.list_lablel_photo = [self.ui.label_photo_1, self.ui.label_photo_2, self.ui.label_photo_3,
                                  self.ui.label_photo_4, self.ui.label_photo_5,
                                  self.ui.label_photo_6, self.ui.label_photo_7, self.ui.label_photo_8,
                                  self.ui.label_photo_9, self.ui.label_photo_10]

    def diolog_yes_no(self):
        '''
        предложения отправить анные на дверь
        :return:
        '''
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setStatusTip('Отправить на каробку')
        messageBox.setText("Отправить данные на систему распознование?")
        messageBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

        messageBox.setStyleSheet("QMessageBox{\n"
                                 "background: #3E454B;\n"
                                 "}\n"
                                 "\n"
                                 "QLabel{\n"
                                 "color: #fff;\n"
                                 "}\n"
                                 "\n"
                                 "\n"
                                 "QPushButton:hover {\n"
                                 " background: #2EE59D;\n"
                                 "  box-shadow: 0 15px 20px rgba(46,229,157,.4);\n"
                                 "  color: white;\n"
                                 "  transform: translateY(-7px); \n"
                                 "\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton {\n"
                                 "\n"
                                 "  text-decoration: none;\n"
                                 "  outline: none;\n"
                                 "  display: inline-block;\n"
                                 "  width: 140px;\n"
                                 "  height: 45px;\n"
                                 "  line-height: 45px;\n"
                                 "  border-radius: 45px;\n"
                                 "  margin: 10px 20px;\n"
                                 "  font-family: \'Montserrat\', sans-serif;\n"
                                 "  font-size: 11px;\n"
                                 "  text-transform: uppercase;\n"
                                 "  text-align: center;\n"
                                 "  letter-spacing: 3px;\n"
                                 "  font-weight: 600;\n"
                                 "  color: #524f4e;\n"
                                 "  background: white;\n"
                                 "  box-shadow: 0 8px 15px rgba(0,0,0,.1);\n"
                                 "  transition: .3s;\n"
                                 "border-radius: 20px;\n"
                                 " }\n"
                                 "\n"
                                 "QPushButton:pressed {\n"
                                 "    color: #111;\n"
                                 "    border: 1px solid #3873d9;\n"
                                 "    background: #fff;\n"
                                 " }")

        if messageBox.exec_() == QMessageBox.Yes:
            print('Yes clicked.')
            state = True
        else:
            print('No clicked.')
            state = False
        return state


    def showGraphicsViewRGB(self, pixMap):
        '''
        Позывать изображения на форме RGB
        :param pixMap:
        :param dic_info:
        :return:
        '''
        #print("RGB", pixMap)
        self.ui.graphicsView.setPhoto(pixMap)
        self.ui.graphicsView.fitInView(False)
        
    def search_table(self):
        """
        поиск в тб фио полностью
        """
        FIRST_NAME = self.ui.lineEdit.text()
        LAST_NAME = self.ui.lineEdit_2.text()
        MIDDLE_NAME = self.ui.lineEdit_3.text()
        rows = self.ui.tableWidget.rowCount()
        first = -1
        first_i = -1
        i_for = 0
        for i in range(rows):
            i_for = 0
            if FIRST_NAME == self.ui.tableWidget.item(i,0).text():
                i_for = 1 
                if LAST_NAME == self.ui.tableWidget.item(i,1).text(): i_for += 1 
                if MIDDLE_NAME == self.ui.tableWidget.item(i,2).text(): i_for += 1 
                if first < i_for:
                    first = i_for
                    first_i = i
                    if first == 3:
                        break
            """
            if FIRST_NAME == self.ui.tableWidget.item(i,0).text() and LAST_NAME == self.ui.tableWidget.item(i,1).text() and MIDDLE_NAME == self.ui.tableWidget.item(i,2).text():
                if not first: 
                    self.ui.tableWidget.selectRow(i)
                    break
            """
        #print(first_i)
        if first_i != -1:
            if first == 3:
                self.showMessage("Пользователь найден")
            elif first == 1:
                self.showMessage("Пользователь найден по фамилии")
            else:
                self.showMessage("Найден ближайший пользователь")
            self.ui.tableWidget.selectRow(first_i)
        else:
            self.showMessage("Пользователь не найден")
            self.ui.tableWidget.clearSelection()
            
    def __init_table(self):
        self.ui.tableWidget.setColumnCount(6)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.ui.tableWidget.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Права пользователя", "Сфотографирован", "Уникльный ключ"])

        # Устанавливаем выравнивание на заголовки
        self.ui.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.ui.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.ui.tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.ui.tableWidget.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.ui.tableWidget.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        self.ui.tableWidget.horizontalHeaderItem(5).setTextAlignment(Qt.AlignHCenter)


        self.ui.tableWidget.doubleClicked.connect(self.onDoubleClicked)
        self.ui.tableWidget.cellClicked.connect(self.onClicked)

    def onClicked(self):
        '''
        Выделения всей строки
        :return:
        '''
        currentQTableWidgetItem = self.ui.tableWidget.selectedItems()[0]
        x0 = currentQTableWidgetItem.row()
        y1 = 5
        self.ui.tableWidget.setRangeSelected(QTableWidgetSelectionRange(x0, 0, x0, y1), True)
    
    def ontab_CurrentIndex(self, i):# доступность вкладок
        
        self.ui.tabWidget.setTabEnabled(0,False);
        self.ui.tabWidget.setTabEnabled(1,False);
        self.ui.tabWidget.setTabEnabled(2,False);
        
        #self.tab_setTabEnabled(i)
        
        try:
            self.ui.tabWidget.setTabEnabled(i,True);
            self.ui.tabWidget.setCurrentIndex(i)
        except:
            self.showMessage("ontab_CurrentIndex err")
            
    def onClick_cancel(self):
        '''
        при нажатии кнопки отмена
        :return:
        '''
        self.current_info_user = {'personId': None, 'last_name': None, 'first_name': None, 'middle_name': None,
                                  'mode_skip': None, 'photo': []}

        for count, label in enumerate(self.list_lablel_photo):
            self.list_lablel_photo[count].setText('Фото')

        self.ui.pushButton_3.setText("Сфотографировать")
        """
        self.ui.tab_4.setEnabled(False)
        self.ui.tab_2.setEnabled(False)
        self.ui.tab.setEnabled(True)
        
        """
        self.ontab_CurrentIndex(0) # доступность вкладок
        self.ui.tabWidget.setCurrentIndex(0) # перход на  вкладку
        
        
        self.mainForm.display_on(False)# вкыл \ выкл поток
        
    def onDoubleClicked(self):
        '''

        :return:
        '''
        try:
            currentQTableWidgetItem = self.ui.tableWidget.selectedItems()[0]
        except IndexError:
            self.showMessage("Данные не выбраны")
        else:
            row = currentQTableWidgetItem.row()
            PERSON_ID = self.ui.tableWidget.item(row, 5).text()  # 342bdfdf-e798-4300-a843-a85c80289d5d

            FIRST_NAME = self.ui.tableWidget.item(row, 0).text()
            LAST_NAME = self.ui.tableWidget.item(row, 1).text()
            MIDDLE_NAME = self.ui.tableWidget.item(row, 2).text()
            MODE_SKIP = self.ui.tableWidget.item(row, 3).text()
            self.show_windows_update_user(self.dialog, FIRST_NAME, LAST_NAME, MIDDLE_NAME, MODE_SKIP, PERSON_ID)

    def onClick_photography_process(self):
        '''
        Переход на вкладку фотографирования пользователя
        :return:
        '''
        print("onClick_photography_process")
        try:
            currentQTableWidgetItem = self.ui.tableWidget.selectedItems()[0]
        except IndexError:
            self.showMessage("Данные не выбраны")
        else:
            
            self.ui.pushButton_4.setEnabled(False)
            self.mainForm.display_on(True)
            
            row = currentQTableWidgetItem.row()
            PERSON_ID = self.ui.tableWidget.item(row, 5).text()  # 342bdfdf-e798-4300-a843-a85c80289d5d

            FIRST_NAME = self.ui.tableWidget.item(row, 0).text()
            LAST_NAME = self.ui.tableWidget.item(row, 1).text()
            MIDDLE_NAME = self.ui.tableWidget.item(row, 2).text()
            MODE_SKIP = self.ui.tableWidget.item(row, 3).text()
            

            self.current_info_user = {'personId': None, 'last_name': None, 'first_name': None, 'middle_name': None, 'mode_skip': None,
                                      'photo': []}

            self.current_info_user['personId'] = PERSON_ID
            self.current_info_user['last_name'] = LAST_NAME
            self.current_info_user['first_name'] = FIRST_NAME
            self.current_info_user['middle_name'] = MIDDLE_NAME
            self.current_info_user['mode_skip'] = MODE_SKIP
            """
            self.ui.tab.setEnabled(False)

            self.ui.tab_2.setEnabled(True)
            """
            self.ontab_CurrentIndex(1)
            self.ui.tabWidget.setCurrentIndex(1)

            print(PERSON_ID, FIRST_NAME, LAST_NAME, MIDDLE_NAME, MODE_SKIP)

    def onClick_next(self):
        '''
        при нажатии кнопки далее на вкладке фото
        :return:
        '''

        self.ui.lineEdit_5.setText(self.current_info_user['last_name'])
        self.ui.lineEdit_6.setText(self.current_info_user['first_name'])
        self.ui.lineEdit_7.setText(self.current_info_user['middle_name'])

        for count, photo in enumerate(self.current_info_user['photo']):
            if self.mainForm.display != None:
                photo = cv2.resize(photo, (0, 0), fx=0.25, fy=0.25)
                protoPixMap = self.__converterNumpyAraayToPixMap(photo)
                self.list_lablel_photo[count].setPixmap(protoPixMap)

            if count >= 9:
                break
        """
        self.ui.tab_4.setEnabled(True)
        """
        self.ontab_CurrentIndex(2)
        self.ui.tabWidget.setCurrentIndex(2)

    def pull_data_table(self, dict_data):
        '''
        Функция размещения данных на форму в виджет таблици
        :param dict_data: {'b9e1d2bc-ac4f-4b5b-bec3-fd586c8c3e49':
        {'FIRST_NAME': 'Дмитрий', 'LAST_NAME': 'Шумелев', 'MIDDLE_NAME': 'Игоревич', 'ORG_ID': 'd186ffeb-3499-4eb3-844e-cb3f2f7f97fb', 'cardID': '004EF89D'}}
        :return:
        '''

        def createItem(text, flags):
            tableWidgetItem = QTableWidgetItem(text)
            tableWidgetItem.setFlags(flags)
            return tableWidgetItem

        self.ui.tableWidget.setRowCount(len(dict_data))  # и одну строку в таблице
        for count, key_people in enumerate(dict_data):

            self.ui.tableWidget.setItem(count, 0, createItem(dict_data[key_people]['FIRST_NAME'], Qt.ItemIsSelectable | Qt.ItemIsEnabled))
            self.ui.tableWidget.setItem(count, 1, createItem(dict_data[key_people]['LAST_NAME'], Qt.ItemIsSelectable | Qt.ItemIsEnabled))
            self.ui.tableWidget.setItem(count, 2, createItem(dict_data[key_people]['MIDDLE_NAME'], Qt.ItemIsSelectable | Qt.ItemIsEnabled))
            self.ui.tableWidget.setItem(count, 3, createItem(str(dict_data[key_people]['MODE_SKIP']), Qt.ItemIsSelectable | Qt.ItemIsEnabled))
            self.ui.tableWidget.setItem(count, 4, createItem(str(dict_data[key_people]['STATUS_PHOTO']), Qt.ItemIsSelectable | Qt.ItemIsEnabled))
            self.ui.tableWidget.setItem(count, 5, createItem(str(key_people), Qt.ItemIsSelectable | Qt.ItemIsEnabled))



        # изменить размер столбца по содержимому
        self.ui.tableWidget.resizeColumnsToContents()

    def showMessage(self, message):
        '''
        Вывод обычного сообщения
        :param messtage:
        :return:
        '''
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setStyleSheet("QMessageBox{\n"
                                 "background: #3E454B;\n"
                                 "}\n"
                                 "\n"
                                 "QLabel{\n"
                                 "color: #fff;\n"
                                 "}\n"
                                 "\n"
                                 "\n"
                                 "QPushButton:hover {\n"
                                 " background: #2EE59D;\n"
                                 "  box-shadow: 0 15px 20px rgba(46,229,157,.4);\n"
                                 "  color: white;\n"
                                 "  transform: translateY(-7px); \n"
                                 "\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton {\n"
                                 "\n"
                                 "  text-decoration: none;\n"
                                 "  outline: none;\n"
                                 "  display: inline-block;\n"
                                 "  width: 140px;\n"
                                 "  height: 45px;\n"
                                 "  line-height: 45px;\n"
                                 "  border-radius: 45px;\n"
                                 "  margin: 10px 20px;\n"
                                 "  font-family: \'Montserrat\', sans-serif;\n"
                                 "  font-size: 11px;\n"
                                 "  text-transform: uppercase;\n"
                                 "  text-align: center;\n"
                                 "  letter-spacing: 3px;\n"
                                 "  font-weight: 600;\n"
                                 "  color: #524f4e;\n"
                                 "  background: white;\n"
                                 "  box-shadow: 0 8px 15px rgba(0,0,0,.1);\n"
                                 "  transition: .3s;\n"
                                 "border-radius: 20px;\n"
                                 " }\n"
                                 "\n"
                                 "QPushButton:pressed {\n"
                                 "    color: #111;\n"
                                 "    border: 1px solid #3873d9;\n"
                                 "    background: #fff;\n"
                                 " }")
        messageBox.setText(str(message))
        messageBox.exec_()

    def show_windows_update_user(self, dialog, last_name, first_name, middle_name, mode_skip, PERSON_ID):
        '''
        Показать окно для изменения данных пользователя
        :param window:
        :param last_name:
        :param first_name:
        :param middle_name:
        :param mode_skip:
        :return:
        '''
        dialog.set_text(last_name, first_name, middle_name, mode_skip, PERSON_ID)
        if not dialog.isVisible():
            dialog.open()
            dialog.raise_()
            dialog.activateWindow()

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

def main():
    pathSettings =os.path.join(os.getcwd(),'rc','settings')
    settings = Settings(pathSettings)
    controll = controller(settings)
    controll.run()

if __name__ == '__main__':
    sys.exit(main())