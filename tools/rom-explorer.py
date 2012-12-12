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
		self.maxDim = 600
		self.setAcceptHoverEvents(True)
		self.rebuildImage()
		# Create a wrapped object for emitting events
		self.qobject = QtCore.QObject()

	def rebuildImage(self):
		width = self.stride * (8 / self.depth)
		height = int(math.ceil(self.size / float(self.stride)))
		self.img = QtGui.QImage(width,height,QtGui.QImage.Format_Mono)
		byteidx = 0
		for y in range(height):
			line = self.img.scanLine(y)
			line.setsize(self.stride)
			try:
				line[0:self.stride] = self.data[byteidx:byteidx+self.stride]
				byteidx = byteidx + self.stride
			except ValueError:
				# zero out the rest of the scan line
				remainder = len(self.data)-byteidx
				line[0:remainder] = self.data[byteidx:]
				buf = "\x00"
				for x in range(remainder,self.stride):
					line[x] = buf[0]
		self.width = width
		self.height = height
		self.xstrips = 1
		if self.height > self.maxDim:
			self.xstrips = (self.height + self.maxDim - 1)/self.maxDim

	def paint(self, qpainter, qoptions, widget=None):
		vh = min(self.height,self.maxDim)
		for strip in range(self.xstrips):
			qpainter.drawImage(strip*self.width,0,self.img,0,vh*strip,self.width,vh)

	def hoverMoveEvent(self,event):
		strip = int(event.pos().x() / self.width)
		actualh = min(self.height, self.maxDim)
		stripoff = strip*self.width*actualh*self.depth
		yoff = self.width*int(event.pos().y())*self.depth
		xoff = int(event.pos().x() - strip*self.width)*self.depth
		totalbitoff = int(xoff+yoff+stripoff)
		offset = totalbitoff / 8
		bit = totalbitoff % 8
		self.qobject.emit(QtCore.SIGNAL("mouseOverLocation"),offset,bit)

	def boundingRect(self):
		return QtCore.QRectF(0,0, self.width * self.xstrips, min(self.height,self.maxDim))


class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = mainwindow.Ui_MainWindow()
		self.ui.setupUi(self)

	def updateWithLocation(self,offset,bit):
		self.ui.statusbar.showMessage('Binary {0} loaded; total size {1} [Offset 0x{2:X} bit {3}]'.format(self.bin.name, self.bin.size, offset, bit))

	def setBinary(self,bin):
		self.bin = bin
		self.bin.depth = int(self.ui.bitDepthComboBox.currentText())
		self.bin.stride = self.ui.rowStrideBox.value()
		self.ui.statusbar.showMessage('Binary {0} loaded; total size {1}.'.format(bin.name, bin.size))
		self.scene = QtGui.QGraphicsScene()
		self.scene.addItem(bin)
		self.ui.bitmapView.setScene(self.scene)
		self.ui.bitmapView.mapToScene(0,0)
		QtCore.QObject.connect(self.bin.qobject,QtCore.SIGNAL("mouseOverLocation"),self.updateWithLocation)

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
