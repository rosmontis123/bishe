import sys
import typing
import os
from functools import partial
from datetime import datetime

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

# 添加PDF生成相关库
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from view.manualQuery_from.form import Ui_Form
from view.manual_form.manual import Ui_ManualForm
from view.manual_form.setting import Ui_Setting
from view.manual_form.prentry import Ui_Prentry
from view.manual_form.setBdf import Ui_SetBdf
from view.manual_form.sign_info import Ui_diag_MainWindow
from view.manual_form.diagList import Ui_diagList
from view.manual_form.prentry import Ui_Prentry


class PrentryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.hide()


class sign_InfoView(QMainWindow, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_diag_MainWindow()
        self.ui.setupUi(self)


class ManualView(QWidget):
    page_control_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.homePage.clicked.connect(self.home_page)
        self.ui.prePage.clicked.connect(self.pre_page)
        self.ui.nextPage.clicked.connect(self.next_page)
        self.ui.finalPage.clicked.connect(self.final_page)
        self.ui.confirmSkip.clicked.connect(self.confirm_skip)
        self.ui.pushButton.clicked.connect(self.my_Query)

    def generate_pdf(self, diag_info, patient_name):
        """生成PDF文件"""
        try:
            # 创建保存目录
            save_dir = r"D:\_pdf"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{patient_name}_{timestamp}.pdf"
            filepath = os.path.join(save_dir, filename)

            # 创建PDF文档
            c = canvas.Canvas(filepath, pagesize=letter)
            width, height = letter

            # 设置字体
            c.setFont("Helvetica", 12)

            # 添加内容
            y_position = height - 40
            c.drawString(100, y_position, f"患者姓名: {patient_name}")
            y_position -= 20
            c.drawString(100, y_position, f"检查单号: {diag_info[-2]}")
            y_position -= 20
            c.drawString(100, y_position, f"测量日期: {diag_info[1]}")
            y_position -= 20
            c.drawString(100, y_position, f"诊断医生: {diag_info[2]}")
            y_position -= 20
            c.drawString(100, y_position, f"诊断时间: {diag_info[4]}")
            y_position -= 20
            c.drawString(100, y_position, f"诊断状态: {diag_info[3]}")

            c.save()

            # 显示生成成功提示
            QMessageBox.information(self, "导出成功", f"PDF文件已保存到：\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成PDF失败：{str(e)}")

    def init_table(self, diags_viewInfo, curUser, userNamesDict, paitentNamesDict, on_clicked_manual_query,
                   on_clicked_diag_query, curPageIndex, maxPages):
        try:
            self.ui.tableWidget.clear()
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["检查单号", '病人', '测量日期', '医生', '状态', '诊断时间', '操作'])
            self.ui.tableWidget.removeRow(0)
            self.ui.curPage.setText(str(curPageIndex))
            self.ui.totalPage.setText(f"共{maxPages}页")

            self.row_num = len(diags_viewInfo)
            if self.row_num <= 0:
                self.ui.tableWidget.setRowCount(1)
                self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("[无]"))
                self.ui.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(0, 0).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(0, 0).font()
                font.setPointSize(12)
                return

            col_num = 6
            if self.row_num > 12:
                self.row_num = 12

            self.ui.tableWidget.setRowCount(self.row_num)
            for i in range(self.row_num):
                self.ui.tableWidget.setRowHeight(i, 50)

            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            iFont = QFont("", 14)
            for row in range(0, self.row_num):
                i = 0
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][-2]))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                i = i + 1
                patient_name = paitentNamesDict.get(diags_viewInfo[row][0], str(diags_viewInfo[row][0]))
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(patient_name))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                i = i + 1
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][1])))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)
                i = i + 1
                doctor_name = userNamesDict.get(diags_viewInfo[row][2], str(diags_viewInfo[row][2]))
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(doctor_name))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                i = i + 1
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][3])))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                i = i + 1
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][4]).format("yyyy-MM-dd")))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                # 操作列布局
                layout = QHBoxLayout()
                self.ui.tableWidget.setCellWidget(row, col_num, QWidget())

                # 选择脑电数据文件按钮
                manualBtn = QPushButton('选择脑电数据文件...')
                manualBtn.clicked.connect(partial(on_clicked_manual_query, diags_viewInfo[row], patient_name))
                manualBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                manualBtn.setCursor(Qt.PointingHandCursor)
                layout.addWidget(manualBtn)

                # 查看诊断信息按钮
                diagBtn = QPushButton('查看诊断信息')
                diagBtn.clicked.connect(partial(on_clicked_diag_query, diags_viewInfo[row], patient_name))
                diagBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                diagBtn.setCursor(Qt.PointingHandCursor)
                layout.addWidget(diagBtn)

                # 新增打印信息按钮
                printBtn = QPushButton('打印信息')
                printBtn.clicked.connect(partial(self.generate_pdf, diags_viewInfo[row], patient_name))
                printBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                printBtn.setCursor(Qt.PointingHandCursor)
                layout.addWidget(printBtn)

                # 设置布局比例
                layout.setStretch(0, 1)
                layout.setStretch(1, 1)
                layout.setStretch(2, 1)
                self.ui.tableWidget.cellWidget(row, col_num).setLayout(layout)

        except Exception as e:
            print('initTable', e)

    def home_page(self):
        self.page_control_signal.emit(["home"])

    def pre_page(self):
        self.page_control_signal.emit(["pre"])

    def next_page(self):
        self.page_control_signal.emit(["next"])

    def final_page(self):
        self.page_control_signal.emit(["final"])

    def confirm_skip(self):
        self.page_control_signal.emit(["confirm"])

    def my_Query(self):
        self.page_control_signal.emit(["query"])

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     view = ManualView()
#     view.show()
#     sys.exit(app.exec_())