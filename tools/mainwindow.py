# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Wed Aug  8 09:44:45 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.bitmapView = QtGui.QGraphicsView(self.centralwidget)
        self.bitmapView.setObjectName(_fromUtf8("bitmapView"))
        self.verticalLayout_2.addWidget(self.bitmapView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.bitDepthComboBox = QtGui.QComboBox(self.centralwidget)
        self.bitDepthComboBox.setObjectName(_fromUtf8("bitDepthComboBox"))
        self.bitDepthComboBox.addItem(_fromUtf8(""))
        self.bitDepthComboBox.addItem(_fromUtf8(""))
        self.bitDepthComboBox.addItem(_fromUtf8(""))
        self.bitDepthComboBox.addItem(_fromUtf8(""))
        self.bitDepthComboBox.addItem(_fromUtf8(""))
        self.bitDepthComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.bitDepthComboBox)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.rowStrideBox = QtGui.QSpinBox(self.centralwidget)
        self.rowStrideBox.setMinimum(1)
        self.rowStrideBox.setMaximum(2096)
        self.rowStrideBox.setObjectName(_fromUtf8("rowStrideBox"))
        self.horizontalLayout.addWidget(self.rowStrideBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "ROM Bitmap Explorer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Bit Depth", None, QtGui.QApplication.UnicodeUTF8))
        self.bitDepthComboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.bitDepthComboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.bitDepthComboBox.setItemText(2, QtGui.QApplication.translate("MainWindow", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.bitDepthComboBox.setItemText(3, QtGui.QApplication.translate("MainWindow", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.bitDepthComboBox.setItemText(4, QtGui.QApplication.translate("MainWindow", "16", None, QtGui.QApplication.UnicodeUTF8))
        self.bitDepthComboBox.setItemText(5, QtGui.QApplication.translate("MainWindow", "24", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Row Stride (bytes)", None, QtGui.QApplication.UnicodeUTF8))

