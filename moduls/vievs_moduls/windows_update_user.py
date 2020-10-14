'''
Диологовое окно для изменения информации о пользователе
функционал:
1) on_click_update - при нажатии обновить данные возвращает данные из формы и в сигнал signal_update_info_user
2) set_text - Выставляет данные в форму
3) close_diolog - при нажатии на кнопку закрыть окно
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import sys

class Windows_update_user(QtWidgets.QDialog):
    signal_update_info_user = pyqtSignal(dict)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Обновления информации")
        self.resize(492, 177)
        Dialog = self
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.on_click_update)
        self.pushButton_2.clicked.connect(self.close_diolog)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "Фамилия:"))
        self.label_2.setText(_translate("Dialog", "Имя:"))
        self.label_3.setText(_translate("Dialog", "Отчество:"))
        self.label_4.setText(_translate("Dialog", "Права доступа:"))
        self.pushButton.setText(_translate("Dialog", "Изменить"))
        self.pushButton_2.setText(_translate("Dialog", "Закрыть"))

    def on_click_update(self):
        '''
        При нажатии на кнопку обновить данные
        :return:
        '''
        last_name = self.lineEdit.text()
        first_name = self.lineEdit_2.text()
        middle_name = self.lineEdit_3.text()
        mode_skip = self.lineEdit_4.text()

        self.hide()

        update_info_user = {"last_name": last_name, "first_name": first_name, "middle_name": middle_name, "mode_skip": mode_skip, 'person_id': self.PERSON_ID}
        self.signal_update_info_user.emit(update_info_user)

        return update_info_user

    def set_text(self, last_name, first_name, middle_name, mode_skip, PERSON_ID):
        '''
        Заполняет значения формы
        :param last_name:
        :param first_name:
        :param middle_name:
        :param mode_skip:
        :return:
        '''
        self.PERSON_ID = PERSON_ID

        self.lineEdit.setText(last_name)
        self.lineEdit_2.setText(first_name)
        self.lineEdit_3.setText(middle_name)
        self.lineEdit_4.setText(mode_skip)

    def close_diolog(self):
        self.close()


def on_clicked():
    if not dialog.isVisible():
        dialog.lineEdit.setText("")
        dialog.open()
        dialog.raise_()
        dialog.activateWindow()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setWindowTitle("diolog")
    window.resize(300, 70)

    button = QtWidgets.QPushButton("widget")
    button.clicked.connect(on_clicked)

    box = QtWidgets.QVBoxLayout()
    box.addWidget(button)
    window.setLayout(box)
    window.show()

    dialog = Windows_update_user(window)
    dialog.pushButton.clicked.connect(dialog.on_accept)
    # dialog.hide()

    sys.exit(app.exec_())