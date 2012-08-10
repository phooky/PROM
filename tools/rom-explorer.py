#!/usr/bin/python

from PyQt4 import QtCore, QtGui
import sys
import math
import mainwindow
import os.path

# Depth: depth in bits
# Width: width in bytes
# Height: computed

# Strips: # of strips (auto?)
class BinMapper(QtGui.QGraphicsItem):
	def __init__(self, path):
		super(BinMapper,self).__init__()
		f = open(path)
		self.name = os.path.basename(path)
		self.data = f.read()
		self.size = len(self.data)
		self.depth = 1
		self.stride = 1
		self.bigendian = 1
		self.rebuildImage()

	def rebuildImage(self):
		width = self.stride * (8 / self.depth)
		height = int(math.ceil(self.size / float(self.stride)))
		self.img = QtGui.QImage(width,height,QtGui.QImage.Format_Mono)
		byteidx = 0
		try:
			for y in range(height):
				line = self.img.scanLine(y)
				line.setsize(self.stride)
				for x in range(self.stride):
					line[x] = self.data[byteidx]
					byteidx = byteidx + 1
		except IndexError:
			# zero out the rest of the image
			pass

	def paint(self, qpainter, qoptions, widget=None):
		qpainter.drawImage(0,0,self.img)

	def boundingRect(self):
		width = self.stride * (8 / self.depth)
		height = int(math.ceil(self.size / float(self.stride)))
		return QtCore.QRectF(0,0,width, height)


class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = mainwindow.Ui_MainWindow()
		self.ui.setupUi(self)

	def setBinary(self,bin):
		self.bin = bin
		self.bin.depth = int(self.ui.bitDepthComboBox.currentText())
		self.bin.stride = self.ui.rowStrideBox.value()
		self.ui.statusbar.showMessage('Binary {0} loaded; total size {1}.'.format(bin.name, bin.size))
		self.scene = QtGui.QGraphicsScene()
		self.scene.addItem(bin)
		self.ui.bitmapView.setScene(self.scene)
		self.ui.bitmapView.mapToScene(0,0)

	def updateScene(self):
		self.bin.rebuildImage()
		self.ui.bitmapView.scene().setSceneRect(self.bin.boundingRect())
		self.ui.bitmapView.viewport().update()

	#QtCore.pyqtSlot()
	def on_bitDepthComboBox_currentIndexChanged(self,index):
		self.bin.rebuildImage()
		self.bin.depth = int(self.ui.bitDepthComboBox.currentText())
		self.updateScene()

	#QtCore.pyqtSlot()
	def on_rowStrideBox_valueChanged(self,value):
		self.bin.stride = self.ui.rowStrideBox.value()
 		self.updateScene()

# Strategies for iterating through cut-up formats

import cProfile

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	bm = BinMapper(sys.argv[1])
	mw = MainWindow()
	mw.setVisible(1)
	mw.setBinary(bm)
	app.exec_()