import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# custom class
from CheckDataframeIndexDialog import CheckDataframeIndexDialog
from ErrorDialog import ErrorDialog
from PandasModel import PandasModel

formClass = uic.loadUiType("ui/main2.ui")[0]


class Main(QMainWindow, formClass):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # set tabWidget index
        self.tabWidget.setCurrentIndex(0)

        self.initUI()

    def initUI(self):
        # 데이터와 상관관계 탭(tab1)
        # 메뉴바 아이템 추가1 - 파일 불러오기
        openAction = QAction("Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip("Open File")
        openAction.triggered.connect(self.openMenu)

        # 메뉴바 아이템 추가2 - 프로그램 종료
        quitAction = QAction(QIcon('study/images/exit.png'), 'Exit', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.setStatusTip('Quit Program')
        quitAction.triggered.connect(qApp.quit)

        # 상태바 추가
        self.statusBar()

        # 메뉴바 추가
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(openAction)
        filemenu.addAction(quitAction)

        # 프로그램 제목
        self.setWindowTitle('MateriaL')

        # 상관관계분석 그래프 세팅
        # self.fig = plt.Figure(figsize=(6,8))
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.relationLayout.addWidget(self.canvas)

    # 파일 불러오기 기능 - dialog (파일 불러오기 및 상관관계분석 그래프 생성)
    def openMenu(self):
        self.dataView.reset()

        # csv 파일 여는 팝업
        self.filename = QFileDialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)")
        # print(self.filename[0])
        # print(all(self.filename))

        if all(self.filename) is False:
            print("filename is null")
        else:
            chkIndex = CheckDataframeIndexDialog()
            chkIndex.exec_()

            dataframeIndex = chkIndex.dataframeIndex

            if dataframeIndex == 0:
                # csv 파일 읽기
                self.df = pd.read_csv(self.filename[0])
            elif dataframeIndex == 1:
                self.df = pd.read_csv(self.filename[0], header=None)
                tempColumns = []
                for i, value in enumerate(self.df.columns):
                    tempColumns.append("index " + str(i))
                self.df.columns = tempColumns
            print(self.df)
            model = PandasModel(self.df)
            self.dataView.setModel(model)

            # 데이터 일반 정보 List View(탭1 - dataInformationLayout - dataInformationListView)
            perc = [.20, .40, .60, .80]
            desc = self.df.describe(percentiles=perc)
            desc = pd.DataFrame(desc)
            descModel = PandasModel(desc)
            self.summaryView.setModel(descModel)

            # 상관관계분석 그래프
            self.fig.clear()
            ax = self.fig.add_subplot(111)
            ax.set_yticklabels(self.df.columns, va="center", ha="center")
            ax.set_title("Heatmap by Correlation", fontsize=15)

            try:
                sns.heatmap(data=self.df.corr(method="spearman"), annot=True,
                            fmt='.2f', linewidths=.5, cmap='Blues', ax=ax)
            except Exception as e:
                self.errorText = "Error! : " + str(e)
                errDiag = ErrorDialog(self.errorText)
                errDiag.exec_()

            self.canvas.draw()

            # # 데이터에서 컬럼 뽑아오기
            # self.columns = self.df.columns

            # for i in range(len(self.columns) - 1):
            #     self.listWidget.addItem(self.columns[i])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
