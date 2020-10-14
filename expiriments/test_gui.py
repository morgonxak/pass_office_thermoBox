# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import sys


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Äèàëîãîâîå îêíî")
        self.resize(200, 70)

        self.mainBox = QtWidgets.QVBoxLayout()

        self.lineEdit = QtWidgets.QLineEdit()
        self.mainBox.addWidget(self.lineEdit)

        self.hbox = QtWidgets.QHBoxLayout()
        self.btnOK = QtWidgets.QPushButton("&OK")
        self.btnCancel = QtWidgets.QPushButton("&Cancel")
        self.btnCancel.setDefault(True)
        self.btnCancel.clicked.connect(self.hide)
        self.hbox.addWidget(self.btnOK)
        self.hbox.addWidget(self.btnCancel)
        self.mainBox.addLayout(self.hbox)

        self.setLayout(self.mainBox)


def on_clicked():
    if not dialog.isVisible():
        dialog.lineEdit.setText("")
        dialog.open()
        dialog.raise_()
        dialog.activateWindow()


def on_accept():
    dialog.hide()
    print(dialog.lineEdit.text())


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Êëàññ QDialog")
window.resize(300, 70)

button = QtWidgets.QPushButton("Îòîáðàçèòü äèàëîãîâîå îêíî...")
button.clicked.connect(on_clicked)

box = QtWidgets.QVBoxLayout()
box.addWidget(button)
window.setLayout(box)
window.show()

window2 = QtWidgets.QWidget()
window2.setWindowTitle("Ýòî îêíî íå áóäåò áëîêèðîâàíî ïðè open()")
window2.resize(500, 100)
window2.show()

dialog = MyDialog(window)
dialog.btnOK.clicked.connect(on_accept)
dialog.hide()

sys.exit(app.exec_())