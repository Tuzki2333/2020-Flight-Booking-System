# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'passenger.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 10, 101, 31))
        font = QtGui.QFont()
        font.setFamily(".Al Bayan PUA")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(29, 49, 271, 111))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 269, 109))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar.setGeometry(QtCore.QRect(250, 0, 16, 111))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.listView = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.listView.setGeometry(QtCore.QRect(0, 0, 251, 111))
        self.listView.setObjectName("listView")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btn_add = QtWidgets.QPushButton(Dialog)
        self.btn_add.setGeometry(QtCore.QRect(30, 170, 112, 32))
        self.btn_add.setObjectName("btn_add")
        self.btn_delete = QtWidgets.QPushButton(Dialog)
        self.btn_delete.setGeometry(QtCore.QRect(170, 170, 112, 32))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_return = QtWidgets.QPushButton(Dialog)
        self.btn_return.setGeometry(QtCore.QRect(100, 200, 112, 32))
        self.btn_return.setObjectName("btn_return")

        self.retranslateUi(Dialog)
        self.btn_return.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.qList = ["item"]

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "乘机人管理"))
        self.label.setText(_translate("Dialog", "乘机人管理"))
        self.btn_add.setText(_translate("Dialog", "新增乘机人"))
        self.btn_delete.setText(_translate("Dialog", "删除乘机人"))
        self.btn_return.setText(_translate("Dialog", "返回"))
