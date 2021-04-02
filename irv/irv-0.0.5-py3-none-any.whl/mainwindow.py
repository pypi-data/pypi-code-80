# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(973, 588)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftVerticalLayout = QVBoxLayout()
        self.leftVerticalLayout.setSpacing(12)
        self.leftVerticalLayout.setObjectName(u"leftVerticalLayout")
        self.acqHeaderTableView = QTableView(self.centralWidget)
        self.acqHeaderTableView.setObjectName(u"acqHeaderTableView")

        self.leftVerticalLayout.addWidget(self.acqHeaderTableView)

        self.linePlotsFrame = QFrame(self.centralWidget)
        self.linePlotsFrame.setObjectName(u"linePlotsFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linePlotsFrame.sizePolicy().hasHeightForWidth())
        self.linePlotsFrame.setSizePolicy(sizePolicy)
        self.linePlotsFrame.setMinimumSize(QSize(869, 10))
        self.linePlotsFrame.setMouseTracking(False)
        self.linePlotsFrame.setFrameShape(QFrame.StyledPanel)
        self.linePlotsFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.linePlotsFrame)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")

        self.leftVerticalLayout.addWidget(self.linePlotsFrame)


        self.horizontalLayout.addLayout(self.leftVerticalLayout)

        self.rightVerticalLayout = QVBoxLayout()
        self.rightVerticalLayout.setSpacing(12)
        self.rightVerticalLayout.setObjectName(u"rightVerticalLayout")
        self.rightVerticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.rightVerticalLayout.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.centralWidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.rightVerticalLayout.addWidget(self.label)

        self.activeChannelSlider = QSlider(self.centralWidget)
        self.activeChannelSlider.setObjectName(u"activeChannelSlider")
        sizePolicy1.setHeightForWidth(self.activeChannelSlider.sizePolicy().hasHeightForWidth())
        self.activeChannelSlider.setSizePolicy(sizePolicy1)
        self.activeChannelSlider.setMaximum(0)
        self.activeChannelSlider.setOrientation(Qt.Horizontal)

        self.rightVerticalLayout.addWidget(self.activeChannelSlider)

        self.currentDataListView = QListView(self.centralWidget)
        self.currentDataListView.setObjectName(u"currentDataListView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.currentDataListView.sizePolicy().hasHeightForWidth())
        self.currentDataListView.setSizePolicy(sizePolicy2)
        self.currentDataListView.setMinimumSize(QSize(164, 0))
        self.currentDataListView.setMaximumSize(QSize(96, 16777215))

        self.rightVerticalLayout.addWidget(self.currentDataListView, 0, Qt.AlignLeft)


        self.horizontalLayout.addLayout(self.rightVerticalLayout)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 973, 28))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName(u"mainToolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
        QWidget.setTabOrder(self.acqHeaderTableView, self.activeChannelSlider)
        QWidget.setTabOrder(self.activeChannelSlider, self.currentDataListView)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Channel:", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

