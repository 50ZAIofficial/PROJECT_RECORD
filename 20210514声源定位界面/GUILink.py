import matplotlib
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QGraphicsScene

import Data_Process
from GUI20210502 import Ui_MainWindow

matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import sys
import pandas as pd
import Serial_Data
import Music_Doa
from matplotlib import pyplot as plt
import numpy as np
from PySide2.QtWidgets import *


class MyFigureCanvas(FigureCanvas):
    '''
    通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
    '''

    def __init__(self, parent=None, width=5, height=5, xlim=(0, 2500), ylim=(-2, 2), dpi=100):
        # 创建一个Figure
        # fig = plt.Figure(, dpi=dpi, tight_layout=True)  # tight_layout: 用于去除画图时两边的空白
        fig = plt.figure(figsize=(width, height), tight_layout=True)
        FigureCanvas.__init__(self, fig)  # 初始化父类
        self.setParent(parent)
        self.ax = fig.gca(projection='3d')

        # self.axes = fig.add_subplot(111)  # 添加子图
        self.ax.spines['top'].set_visible(False)  # 去掉绘图时上面的横线
        self.ax.spines['right'].set_visible(False)  # 去掉绘图时右面的横线
        # self.ax.set_xlim(181)
        # self.ax.set_ylim(181)


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.Signal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handleCalc)
        self.pushButton_2.clicked.connect(self.handleCalc_2)
        self.pushButton_3.clicked.connect(self.handleCalc_3)
        self.pushButton_4.clicked.connect(self.handleCalc_4)
        self.pushButton_5.clicked.connect(self.handleCalc_5)
        self.pushButton_6.clicked.connect(self.handleCalc_6)
        sys.stdout = EmittingStream()
        # self.connect(sys.stdout,QtCore.SIGNAL('textWritten(QString)'),self.normalOutputWritten)
        sys.stdout.textWritten.connect(self.normalOutputWritten)
        self.textEdit_2.setPlaceholderText("请输入8.5kHz声源下的最低SNR")
        self.textEdit.setPlaceholderText("请输入测量次数")
        self.DOAData = np.zeros(shape=(181, 181))

        self.DoaAlgorithmWay = self.comboBox.currentText()

        self.gv_visual_data_content = MyFigureCanvas(
            width=self.graphicsView.width() / 220,
            height=self.graphicsView.height() / 220)
        # xlim=(0, 2 * np.pi),
        # ylim=(-1, 1))  # 实例化一个FigureCanvas
        self.plot_doa()

    def handleCalc(self):
        self.progressBar.setValue(0)
        self.DoaAlgorithmWay = self.comboBox.currentText()
        collect_times = int(self.textEdit.toPlainText())
        SNR = int(self.textEdit_2.toPlainText())
        self.progressBar.setValue(20)

        if self.DoaAlgorithmWay == 'MUSIC算法':
            self.RawData, self.DOAData = Data_Process.DataProcess(collect_times, SNR)
            print('MUSIC算法定位成功')
        elif self.DoaAlgorithmWay == 'MVDR算法':
            self.RawData, self.DOAData = Data_Process.DataProcessMVDR(collect_times, SNR)
            print('MVDR算法定位成功')
        elif self.DoaAlgorithmWay == 'CBF算法':
            self.RawData, self.DOAData = Data_Process.DataProcessCBF(collect_times, SNR)
            print('CBF算法定位成功')
        self.progressBar.setValue(70)

        self.plot_re()
        self.progressBar.setValue(80)
        thete = np.argmax(np.amax(self.DOAData, axis=1), axis=0) - 90
        fai = np.argmax(np.amax(self.DOAData, axis=0), axis=0) - 90
        self.lineEdit_3.setText(str(fai))
        self.lineEdit_4.setText(str(thete))
        self.progressBar.setValue(100)
        # QMessageBox.about(self.window, '窗口标题', '定位完成')

    def handleCalc_2(self):
        self.writeXLSX(self.RawData)

    def handleCalc_3(self):
        self.SerialTest()
        print(self.comport)

    def handleCalc_4(self):
        self.progressBar.setValue(0)
        self.DoaAlgorithmWay = self.comboBox.currentText()
        collect_times = int(self.textEdit.toPlainText())
        SNR = int(self.textEdit_2.toPlainText())
        self.progressBar.setValue(20)
        if self.DoaAlgorithmWay == 'MUSIC算法':
            self.RawData, self.DOAData = Data_Process.DataProcess(collect_times, SNR)
            print('MUSIC算法定位成功')
        elif self.DoaAlgorithmWay == 'MVDR算法':
            self.RawData, self.DOAData = Data_Process.DataProcessMVDR(collect_times, SNR)
            print('MVDR算法定位成功')
        elif self.DoaAlgorithmWay == 'CBF算法':
            self.RawData, self.DOAData = Data_Process.DataProcessCBF(collect_times, SNR)
            print('CBF算法定位成功')
        self.progressBar.setValue(70)
        self.plot_Spherical()
        self.progressBar.setValue(80)
        thete = np.argmax(np.amax(self.DOAData, axis=1), axis=0) - 90
        fai = np.argmax(np.amax(self.DOAData, axis=0), axis=0) - 90
        self.lineEdit_3.setText(str(fai))
        self.lineEdit_4.setText(str(thete))
        self.progressBar.setValue(100)
        # QMessageBox.about(self.window, '窗口标题', '定位完成')

    def handleCalc_5(self):
        self.progressBar.setValue(0)
        self.DoaAlgorithmWay = self.comboBox.currentText()
        self.DoaPrecision = self.comboBox_2.currentText()
        self.progressBar.setValue(5)
        Pre = 0
        if self.DoaPrecision == '快速':
            Pre = 0
        elif self.DoaPrecision == '精确':
            Pre = 1
        self.progressBar.setValue(10)
        fuyang = float(self.textEdit_7.toPlainText())
        fangwei = float(self.textEdit_8.toPlainText())
        SNRdata = float(self.textEdit_9.toPlainText())
        self.progressBar.setValue(20)
        if (self.DoaAlgorithmWay == 'MUSIC算法'):
            self.DOAData = Music_Doa.SimulationMusic(fangwei, fuyang, SNRdata, Precision=Pre)
            print('MUSIC算法仿真成功')
        elif (self.DoaAlgorithmWay == 'MVDR算法'):
            self.DOAData = Music_Doa.SimulationMVDR(fangwei, fuyang, SNRdata, Precision=Pre)
            print('MVDR算法仿真成功')
        elif (self.DoaAlgorithmWay == 'CBF算法'):
            self.DOAData = Music_Doa.SimulationCBF(fangwei, fuyang, SNRdata, Precision=Pre)
            print('CBF算法仿真成功')
        self.progressBar.setValue(60)
        if Pre == 0:
            thete = np.argmax(np.amax(self.DOAData, axis=1), axis=0) - 90
            fai = np.argmax(np.amax(self.DOAData, axis=0), axis=0) - 90
            self.plot_re()
        else:
            thete = (float(np.argmax(np.amax(self.DOAData, axis=1), axis=0)))/10 - 90
            fai = (float(np.argmax(np.amax(self.DOAData, axis=0), axis=0)))/10 - 90
            self.plot_fine()
        self.progressBar.setValue(80)
        self.lineEdit_3.setText(str(fai))
        self.lineEdit_4.setText(str(thete))
        self.progressBar.setValue(100)

    def handleCalc_6(self):
        self.progressBar.setValue(0)
        self.DoaAlgorithmWay = self.comboBox.currentText()
        self.DoaPrecision = self.comboBox_2.currentText()
        self.progressBar.setValue(5)
        Pre = 0
        if self.DoaPrecision == '快速':
            Pre = 0
        elif self.DoaPrecision == '精确':
            Pre = 1
        self.progressBar.setValue(10)
        fuyang = float(self.textEdit_7.toPlainText())
        fangwei = float(self.textEdit_8.toPlainText())
        SNRdata = float(self.textEdit_9.toPlainText())
        self.progressBar.setValue(20)
        if (self.DoaAlgorithmWay == 'MUSIC算法'):
            self.DOAData = Music_Doa.SimulationMusic(fangwei, fuyang, SNRdata, Precision=Pre)
            print('MUSIC算法仿真成功')
        elif (self.DoaAlgorithmWay == 'MVDR算法'):
            self.DOAData = Music_Doa.SimulationMVDR(fangwei, fuyang, SNRdata, Precision=Pre)
            print('MVDR算法仿真成功')
        elif (self.DoaAlgorithmWay == 'CBF算法'):
            self.DOAData = Music_Doa.SimulationCBF(fangwei, fuyang, SNRdata, Precision=Pre)
            print('CBF算法仿真成功')
        self.progressBar.setValue(60)
        if Pre == 0:
            thete = np.argmax(np.amax(self.DOAData, axis=1), axis=0) - 90
            fai = np.argmax(np.amax(self.DOAData, axis=0), axis=0) - 90
            self.plot_Spherical()
        else:
            thete = (float(np.argmax(np.amax(self.DOAData, axis=1), axis=0)))/10 - 90
            fai = (float(np.argmax(np.amax(self.DOAData, axis=0), axis=0)))/10 - 90
            self.plot_Spherical_Fine()
        self.progressBar.setValue(80)
        self.lineEdit_3.setText(str(fai))
        self.lineEdit_4.setText(str(thete))
        self.progressBar.setValue(100)

    def writeXLSX(self, bufer_data):
        data = pd.DataFrame(bufer_data)
        writer = pd.ExcelWriter('DataSave.xlsx')
        data.to_excel(writer, 'SHEET1')
        writer.save()
        writer.close()
        print('保存成功', '保存在程序目录下的DataSave.xlsx文件中')

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textBrowser_3.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser_3.setTextCursor(cursor)
        self.textBrowser_3.ensureCursorVisible()

    def SerialTest(self):
        self.comport = Serial_Data.SerialTest()

    def plot_doa(self):
        fai_buf, theta_buf = Music_Doa.ax_provide()
        FAI, THE = np.meshgrid(fai_buf, fai_buf)
        self.gv_visual_data_content.ax.plot_wireframe(FAI, THE, self.DOAData, linewidth=0.5)
        self.gv_visual_data_content.ax.set_xlabel('方位角')
        self.gv_visual_data_content.ax.set_ylabel('俯仰角')
        self.gv_visual_data_content.ax.set_zlabel('P/dB')
        # 加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        self.graphic_scene = QGraphicsScene()  # 创建一个QGraphicsScene
        self.graphic_scene.addWidget(
            self.gv_visual_data_content)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.graphicsView.setScene(self.graphic_scene)  # 把QGraphicsScene放入QGraphicsView
        self.graphicsView.show()  # 调用show方法呈现图形

    def plot_re(self):
        self.gv_visual_data_content.ax.clear()  # 由于图片需要反复绘制，所以每次绘制前清空，然后绘图
        fai_buf, theta_buf = Music_Doa.ax_provide()
        FAI, THE = np.meshgrid(fai_buf, fai_buf)
        # self.DOAData = self.DOAData - np.min(self.DOAData) + 0.01
        Pmax = np.max(self.DOAData)
        self.DOAData = 10 * np.log10(self.DOAData / Pmax)
        pass
        self.gv_visual_data_content.ax.set_xlabel('方位角')
        self.gv_visual_data_content.ax.set_ylabel('俯仰角')
        self.gv_visual_data_content.ax.set_zlabel('P/dB')
        self.gv_visual_data_content.ax.plot_wireframe(FAI, THE, self.DOAData, linewidth=0.5)
        # self.gv_visual_data_content.ax.plot_surface(FAI, THE, self.DOAData, linewidth=0.5)
        self.gv_visual_data_content.draw()  # 刷新画布显示图片，否则不刷新显示

    def plot_fine(self):
        self.gv_visual_data_content.ax.clear()  # 由于图片需要反复绘制，所以每次绘制前清空，然后绘图
        fai_buf, theta_buf = Music_Doa.ax_provide_fine()
        FAI, THE = np.meshgrid(fai_buf, fai_buf)
        # self.DOAData = self.DOAData - np.min(self.DOAData) + 0.01
        Pmax = np.max(self.DOAData)
        self.DOAData = 10 * np.log10(self.DOAData / Pmax)
        self.gv_visual_data_content.ax.set_xlabel('方位角')
        self.gv_visual_data_content.ax.set_ylabel('俯仰角')
        self.gv_visual_data_content.ax.set_zlabel('P/dB')
        self.gv_visual_data_content.ax.plot_wireframe(FAI, THE, self.DOAData, linewidth=0.5)
        # self.gv_visual_data_content.ax.plot_surface(FAI, THE, self.DOAData, linewidth=0.5)
        self.gv_visual_data_content.draw()  # 刷新画布显示图片，否则不刷新显示

    def plot_Spherical(self):
        self.gv_visual_data_content.ax.clear()  # 由于图片需要反复绘制，所以每次绘制前清空，然后绘图
        fai_buf, theta_buf = Music_Doa.ax_provide()
        FAI, THE = np.meshgrid(fai_buf, fai_buf)
        fai_ang, thete_ang = 180, 180
        x, y, z = np.empty(shape=32761), np.empty(shape=32761), np.empty(shape=32761)
        while fai_ang >= 0:
            thete_ang = 180
            while thete_ang >= 0:
                z[thete_ang + fai_ang * 181] = self.DOAData[fai_ang, thete_ang] * np.cos((thete_ang - 90) * np.pi / 180)
                x[thete_ang + fai_ang * 181] = self.DOAData[fai_ang, thete_ang] * np.sin(
                    (thete_ang - 90) * np.pi / 180) * np.cos((fai_ang - 90) * np.pi / 180)
                y[thete_ang + fai_ang * 181] = self.DOAData[fai_ang, thete_ang] * np.sin(
                    (thete_ang - 90) * np.pi / 180) * np.sin((fai_ang - 90) * np.pi / 180)
                thete_ang = thete_ang - 1
            fai_ang = fai_ang - 1
        self.gv_visual_data_content.ax.set_xlabel('X')
        self.gv_visual_data_content.ax.set_ylabel('Y')
        self.gv_visual_data_content.ax.set_zlabel('Z')
        self.gv_visual_data_content.ax.set_xticks([])
        self.gv_visual_data_content.ax.set_yticks([])
        self.gv_visual_data_content.ax.set_zticks([])
        self.gv_visual_data_content.ax.scatter(x, y, z, s=0.01)
        self.gv_visual_data_content.draw()  # 刷新画布显示图片，否则不刷新显示

    def plot_Spherical_Fine(self):
        self.gv_visual_data_content.ax.clear()  # 由于图片需要反复绘制，所以每次绘制前清空，然后绘图
        fai_buf, theta_buf = Music_Doa.ax_provide_fine()
        FAI, THE = np.meshgrid(fai_buf, fai_buf)
        fai_ang, thete_ang = 180.0, 180.0
        x, y, z = np.empty(shape=327610), np.empty(shape=327610), np.empty(shape=327610)
        while fai_ang >= 0:
            thete_ang = 180.0
            while thete_ang >= 0:
                z[int(10*(thete_ang + fai_ang * 181))] = self.DOAData[int(10*fai_ang), int(10*thete_ang)] * np.cos((thete_ang - 90) * np.pi / 180)
                x[int(10*(thete_ang + fai_ang * 181))] = self.DOAData[int(10*fai_ang), int(10*thete_ang)] * np.sin(
                    (thete_ang - 90) * np.pi / 180) * np.cos((fai_ang - 90) * np.pi / 180)
                y[int(10*(thete_ang + fai_ang * 181))] = self.DOAData[int(10*fai_ang), int(10*thete_ang)] * np.sin(
                    (thete_ang - 90) * np.pi / 180) * np.sin((fai_ang - 90) * np.pi / 180)
                thete_ang = thete_ang - 1
            fai_ang = fai_ang - 1
        self.gv_visual_data_content.ax.set_xlabel('X')
        self.gv_visual_data_content.ax.set_ylabel('Y')
        self.gv_visual_data_content.ax.set_zlabel('Z')
        self.gv_visual_data_content.ax.set_xticks([])
        self.gv_visual_data_content.ax.set_yticks([])
        self.gv_visual_data_content.ax.set_zticks([])
        self.gv_visual_data_content.ax.scatter(x, y, z, s=0.01)
        self.gv_visual_data_content.draw()  # 刷新画布显示图片，否则不刷新显示



def GUI():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
