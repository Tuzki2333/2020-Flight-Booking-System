# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flight_info.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(392, 176)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 60, 331, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.output_FID = QtWidgets.QLabel(self.layoutWidget)
        self.output_FID.setObjectName("output_FID")
        self.gridLayout.addWidget(self.output_FID, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)
        self.output_Airline = QtWidgets.QLabel(self.layoutWidget)
        self.output_Airline.setText("")
        self.output_Airline.setObjectName("output_Airline")
        self.gridLayout.addWidget(self.output_Airline, 0, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.output_Depart = QtWidgets.QLabel(self.layoutWidget)
        self.output_Depart.setText("")
        self.output_Depart.setObjectName("output_Depart")
        self.gridLayout.addWidget(self.output_Depart, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)
        self.output_Arrive = QtWidgets.QLabel(self.layoutWidget)
        self.output_Arrive.setText("")
        self.output_Arrive.setObjectName("output_Arrive")
        self.gridLayout.addWidget(self.output_Arrive, 1, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.output_Dtime = QtWidgets.QLabel(self.layoutWidget)
        self.output_Dtime.setText("")
        self.output_Dtime.setObjectName("output_Dtime")
        self.gridLayout.addWidget(self.output_Dtime, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 2, 2, 1, 1)
        self.output_Atime = QtWidgets.QLabel(self.layoutWidget)
        self.output_Atime.setText("")
        self.output_Atime.setObjectName("output_Atime")
        self.gridLayout.addWidget(self.output_Atime, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(157, 20, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_6.setText(_translate("Dialog", "航班号："))
        self.output_FID.setText(_translate("Dialog", "未选择"))
        self.label_7.setText(_translate("Dialog", "航空公司："))
        self.label_8.setText(_translate("Dialog", "出发机场："))
        self.label_9.setText(_translate("Dialog", "到达机场："))
        self.label_10.setText(_translate("Dialog", "出发时间："))
        self.label_11.setText(_translate("Dialog", "到达时间："))
        self.label.setText(_translate("Dialog", "航班信息"))
