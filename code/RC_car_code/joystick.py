from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import math
import sys

# class MyJoystick(QWidget):
	# def __init__(self, cbJoyPos, parent=None):
		# super(MyJoystick, self).__init__(parent)
		# self.setMinimumSize(100, 100)
		# self.movingOffset = QPointF(0, 0)
		# self.grabCenter = False
		# self.__maxDistance = 50

		# self.timer = QTimer(self)
		# self.timer.setInterval(10)
		# self.timer.timeout.connect(self.timeout)
		# self.timer.start()
		
		# self.cbJoyPos = cbJoyPos

	# def paintEvent(self, event):
		# painter = QPainter(self)
		# bounds = QRectF(
		# -self.__maxDistance, 
		# -self.__maxDistance, 
		# self.__maxDistance * 2, 
		# self.__maxDistance * 2
		# ).translated(self._center())
		# painter.drawEllipse(bounds)
		# painter.setBrush(Qt.black)
		# painter.drawEllipse(self._centerEllipse())

	# def _centerEllipse(self):
		# if self.grabCenter:
			# return QRectF(-20, -20, 40, 40).\
			# translated(self.movingOffset)
		# return QRectF(-20, -20, 40, 40).translated(self._center())

	# def _center(self):
		# return QPointF(self.width()/2, self.height()/2)

	# def _boundJoystick(self, point):
		# limitLine = QLineF(self._center(), point)
		# if (limitLine.length() > self.__maxDistance):
			# limitLine.setLength(self.__maxDistance)
		# return limitLine.p2()

	# def joystickPosition(self):
		# if not self.grabCenter:
			# return (0, 0)
		# normVector = QLineF(self._center(), self.movingOffset)
		# currentDistance = normVector.length()
		# angle = normVector.angle()

		# distance = min(currentDistance / self.__maxDistance, 1.0)

		# posX = math.cos(angle*math.pi/180)*distance
		# posY = math.sin(angle*math.pi/180)*distance

		# return (posX, posY)

	# def mousePressEvent(self, ev):
		# self.grabCenter = self._centerEllipse().contains(ev.pos())
		# return super().mousePressEvent(ev)

	# def mouseReleaseEvent(self, event):
		# self.grabCenter = False
		# self.movingOffset = QPointF(0, 0)
		# self.update()

	# def mouseMoveEvent(self, event):
		# if self.grabCenter:
			# self.movingOffset = self._boundJoystick(event.pos())
			# self.update()
		# if self.cbJoyPos != None :
			# self.cbJoyPos(self.joystickPosition())

	# def timeout(self):
		# sender = self.sender()
		# if id(sender) == id(self.timer):
			# if self.cbJoyPos != None :
				# self.cbJoyPos(self.joystickPosition())
				
from myjoystick import MyJoystick
			
def cbJoyPos(joystickPosition) :
	print(joystickPosition)

# Create main application window
app = QApplication([])
app.setStyle(QStyleFactory.create("Cleanlooks"))
mw = QMainWindow()
mw.setWindowTitle('MyJoystick')
mw.setGeometry(100, 100, 300, 200)

# Create and set widget layout
# Main widget container
cw = QWidget()
ml = QGridLayout()
cw.setLayout(ml)
mw.setCentralWidget(cw)

# Create joystick
joystick = MyJoystick(cbJoyPos)
ml.addWidget(joystick,0,0)

mw.show()

# Start Qt event loop 
sys.exit(app.exec_())