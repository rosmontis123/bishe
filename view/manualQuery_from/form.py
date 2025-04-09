# -*- coding: utf-8 -*-
from functools import partial

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QLineEdit

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")

        Form.resize(1190, 822)

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.comboBox = QtWidgets.QComboBox(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily("Arial")
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.currentTextChanged.connect(self.comboBoxChanged)
        self.horizontalLayout.addWidget(self.comboBox)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaximumSize(QtCore.QSize(100, 26))
        self.horizontalLayout.addWidget(self.lineEdit)

        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setObjectName("label2")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label2.setFont(font)
        self.horizontalLayout.addWidget(self.label2)

        self.lineEditDate1 = QtWidgets.QLineEdit(Form)
        self.lineEditDate1.setEnabled(True)
        self.lineEditDate1.setObjectName("lineEditDate1")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.lineEditDate1.setFont(font)
        self.lineEditDate1.setMaximumSize(QtCore.QSize(120, 26))
        self.horizontalLayout.addWidget(self.lineEditDate1)

        self.date_lineEdit = QtWidgets.QDateTimeEdit(Form)
        self.date_lineEdit.setEnabled(True)

        self.date_lineEdit.setDisplayFormat("yyyy-MM-dd")
        self.date_lineEdit.setObjectName("date_lineEdit")
        self.date_lineEdit.setCalendarPopup(True)
        self.date_lineEdit.setMaximumSize(QtCore.QSize(18, 26))
        self.date_lineEdit.dateChanged.connect(partial(self.dateChanged, 1))

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily("Arial")
        self.date_lineEdit.setFont(font)
        self.horizontalLayout.addWidget(self.date_lineEdit)

        self.label3 = QtWidgets.QLabel(Form)
        self.label3.setObjectName("label2")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily("Arial")
        self.label3.setFont(font)
        self.horizontalLayout.addWidget(self.label3)

        self.lineEditDate2 = QtWidgets.QLineEdit(Form)
        self.lineEditDate2.setEnabled(True)
        self.lineEditDate2.setObjectName("lineEditDate1")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.lineEditDate2.setFont(font)
        self.lineEditDate2.setMaximumSize(QtCore.QSize(120, 26))
        self.horizontalLayout.addWidget(self.lineEditDate2)

        self.date_lineEdit2 = QtWidgets.QDateTimeEdit(Form)
        self.date_lineEdit2.setEnabled(True)

        self.date_lineEdit2.setDisplayFormat("yyyy-MM-dd")
        self.date_lineEdit2.setObjectName("date_lineEdit")
        self.date_lineEdit2.setCalendarPopup(True)
        self.date_lineEdit2.setMaximumSize(QtCore.QSize(18, 26))
        self.date_lineEdit2.dateChanged.connect(partial(self.dateChanged, 2))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.date_lineEdit2.setFont(font)
        self.horizontalLayout.addWidget(self.date_lineEdit2)

        self.pushButton = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        #self.pushButton.setStyleSheet("background-color: rgb(192, 192, 192);color: rgb(0, 0, 255);")
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setStyleSheet("font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setGeometry(QRect(5, 40, 1300, 760))
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)

        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tableWidget)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)

        self.horizontalLayout_paging = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_paging.setObjectName("horizontalLayout_paging")

        self.horizontalLayout_paging.setSpacing(0)
        self.horizontalLayout_paging.setAlignment(Qt.AlignRight)

        self.homePage = QtWidgets.QPushButton(Form)
        self.homePage.setObjectName("homePage")
        self.homePage.setFont(font)

        self.homePage.setMaximumSize(QtCore.QSize(56, 32))
        self.horizontalLayout_paging.addWidget(self.homePage)

        self.prePage = QtWidgets.QPushButton(Form)
        self.prePage.setObjectName("prePage")
        self.prePage.setFont(font)
        self.prePage.setMaximumSize(QtCore.QSize(90, 32))
        self.horizontalLayout_paging.addWidget(self.prePage)

        self.curPage = QLineEdit(Form)
        self.curPage.setObjectName("curPage")
        self.curPage.setFont(font)
        self.curPage.setMaximumSize(QtCore.QSize(100, 32))
        self.curPage.setReadOnly(True)
        self.curPage.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_paging.addWidget(self.curPage)

        self.nextPage = QtWidgets.QPushButton(Form)
        self.nextPage.setObjectName("nextPage")
        self.nextPage.setFont(font)
        self.nextPage.setMaximumSize(QtCore.QSize(90, 32))
        self.horizontalLayout_paging.addWidget(self.nextPage)

        self.finalPage = QtWidgets.QPushButton(Form)
        self.finalPage.setObjectName("finalPage")
        self.finalPage.setFont(font)
        self.finalPage.setMaximumSize(QtCore.QSize(56, 32))
        self.horizontalLayout_paging.addWidget(self.finalPage)

        self.totalPage = QLabel(Form)
        self.totalPage.setObjectName("totalPage")
        self.totalPage.setFont(font)
        self.totalPage.setMaximumSize(QtCore.QSize(100, 26))
        self.horizontalLayout_paging.addWidget(self.totalPage)

        self.skipLable_0 = QLabel(Form)
        self.skipLable_0.setObjectName("totalPage")
        self.skipLable_0.setFont(font)
        self.skipLable_0.setMaximumSize(QtCore.QSize(80, 26))
        self.horizontalLayout_paging.addWidget(self.skipLable_0)

        self.skipPage = QLineEdit(Form)
        self.skipPage.setObjectName("skipPage")
        self.skipPage.setFont(font)
        self.skipPage.setMaximumSize(QtCore.QSize(56, 32))
        self.skipPage.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_paging.addWidget(self.skipPage)

        self.skipLabel_1 = QLabel(Form)
        self.skipLabel_1.setObjectName("skipLabel_1")
        self.skipLabel_1.setFont(font)
        self.skipLabel_1.setMaximumSize(QtCore.QSize(20, 26))
        self.horizontalLayout_paging.addWidget(self.skipLabel_1)

        self.confirmSkip = QtWidgets.QPushButton(Form)
        self.confirmSkip.setObjectName("confirmSkip")
        self.confirmSkip.setFont(font)
        self.confirmSkip.setMaximumSize(QtCore.QSize(56, 32))
        self.horizontalLayout_paging.addWidget(self.confirmSkip)

        self.verticalLayout.addLayout(self.horizontalLayout_paging)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate

        self.pushButton.setText(_translate("Form", "查询"))

        dt = QtCore.QDateTime.currentDateTime()
        self.date_lineEdit.setDateTime(dt)
        self.date_lineEdit2.setDateTime(dt)

        self.homePage.setText(_translate("Form", "首页"))
        self.prePage.setText(_translate("Form", "<上一页"))
        self.curPage.setText(_translate("Form", "1"))
        self.nextPage.setText(_translate("Form", "下一页>"))
        self.finalPage.setText(_translate("Form", "末页"))
        self.totalPage.setText(_translate("Form", "共1页"))
        self.skipLable_0.setText(_translate("Form", "跳到第:"))
        self.skipPage.setText(_translate("Form", "1"))
        self.skipLabel_1.setText(_translate("Form", "页"))
        self.confirmSkip.setText(_translate("Form", "确定"))

        self.comboBox.setItemText(0, _translate("Form", "[全部]"))
        self.comboBox.setItemText(1, _translate("Form", "检查单号"))
        self.comboBox.setItemText(2, _translate("Form", "病人姓名"))
        self.comboBox.setItemText(3, _translate("Form", "测量日期"))
        self.comboBox.setItemText(4, _translate("Form", "医生名称"))

        self.label2.setText(_translate("Form", "诊断时间≥"))
        self.label3.setText(_translate("Form", "诊断时间≤"))
        self.lineEditDate2.setText("")
        self.lineEditDate1.setText("")
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "检查单号"))
        self.tableWidget.setColumnWidth(0, 160)

        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "病人"))
        self.tableWidget.setColumnWidth(1, 180)

        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "测量日期"))
        self.tableWidget.setColumnWidth(2, 160)

        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "医生"))
        self.tableWidget.setColumnWidth(3, 180)

        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "状态"))
        self.tableWidget.setColumnWidth(4, 160)

        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "诊断时间"))
        self.tableWidget.setColumnWidth(5, 240)

        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "操作"))
        self.tableWidget.setColumnWidth(6, 240)
    def dateChanged(self,gData):
        if gData==2:
            mdate =  self.date_lineEdit2.date().toString('yyyy-MM-dd')
            self.lineEditDate2.setText(mdate)
        else:
            mdate = self.date_lineEdit.date().toString('yyyy-MM-dd')
            self.lineEditDate1.setText(mdate)

    def comboBoxChanged(self):
       self.lineEdit.setText("")
