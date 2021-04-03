# Copyright (C) 2021 Vasco Costa (gluon) <vascomacosta at gmail dot com>
#
# This file is part of glueather.
#
# glueather is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# glueather is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.gridLayout.addWidget(self.label_2, 0, 6, 1, 1)
        self.radioButton = QRadioButton(self.centralwidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)
        self.gridLayout.addWidget(self.radioButton, 0, 7, 1, 1)
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)
        self.gridLayout.addWidget(self.checkBox_2, 0, 4, 1, 1)
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 9)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setChecked(True)
        self.gridLayout.addWidget(self.checkBox_3, 0, 5, 1, 1)
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)
        self.gridLayout.addWidget(self.checkBox, 0, 3, 1, 1)
        self.radioButton_2 = QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 0, 8, 1, 1)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Units:", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Hourly", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Enter a location (ex: London or London,GB)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Display:", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Daily", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Current", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"F", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
