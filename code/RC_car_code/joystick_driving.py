from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import sys
import math
import threading
import socket
import time
import struct
import numpy as np
import cv2

HOST_CAM = '192.168.137.229'
HOST_MOT = '192.168.137.200'
PORT = 80

client_cam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_mot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_cam.connect((HOST_CAM, PORT))
client_mot.connect((HOST_MOT, PORT))

t_now = time.time()
t_prev = time.time()
cnt_frame = 0

running = False
def run():
	global running
	global t_now, t_prev, cnt_frame

	width = 320
	height = 240
	label.resize(width, height)

	while True:	

		# 영상 읽어
		cmd = 12
		cmd = struct.pack('B', cmd)
		client_cam.sendall(cmd)	

		# 영상 받기
		data_len_bytes = client_cam.recv(4)
		data_len = struct.unpack('I', data_len_bytes)

		data = client_cam.recv(data_len[0], socket.MSG_WAITALL)

		# 영상 출력
		np_data = np.frombuffer(data, dtype='uint8')
		frame = cv2.imdecode(np_data,1)
		frame = cv2.rotate(frame,cv2.ROTATE_180)
		frame2 = cv2.resize(frame, (320, 240))
		 
		h,w,c = frame2.shape
		qImg = QtGui.QImage(frame2.data, w, h, w*c, QtGui.QImage.Format_RGB888)
		pixmap = QtGui.QPixmap.fromImage(qImg)
		label.setPixmap(pixmap)
		# cv2.imshow('frame', frame2)

		cnt_frame += 1
		t_now = time.time()
		if t_now - t_prev >= 1.0 :
			t_prev = t_now
			print("frame count : %f" %cnt_frame)
			cnt_frame = 0

# def driving(posX, posY):

class Joystick(QWidget):
    def __init__(self, parent=None):
        super(Joystick, self).__init__(parent)
        self.setMinimumSize(200, 200)
        self.movingOffset = QPointF(0, 0)
        self.grabCenter = False
        self.__maxDistance = 50

        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.__maxDistance, -self.__maxDistance, self.__maxDistance * 2, self.__maxDistance * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(Qt.black)
        painter.drawEllipse(self._centerEllipse())

    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-20, -20, 40, 40).translated(self.movingOffset)
        return QRectF(-20, -20, 40, 40).translated(self._center())

    def _center(self):
        return QPointF(self.width()/2, self.height()/2)

    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)
        if (limitLine.length() > self.__maxDistance):
            limitLine.setLength(self.__maxDistance)
        return limitLine.p2()

    def joystickPosition(self):
        if not self.grabCenter:
            return (0, 0)
        normVector = QLineF(self._center(), self.movingOffset)
        currentDistance = normVector.length()
        angle = normVector.angle()

        distance = min(currentDistance / self.__maxDistance, 1.0)

        posX = math.cos(angle*math.pi/180)*distance
        posY = math.sin(angle*math.pi/180)*distance

        return (posX, posY)

    def mousePressEvent(self, ev):
        self.grabCenter = self._centerEllipse().contains(ev.pos())
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, event):
        self.grabCenter = False
        self.movingOffset = QPointF(0, 0)
        self.update()

    def mouseMoveEvent(self, event):
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()
        # print(self.joystickPosition())
		
        posX, posY = self.joystickPosition()
        # print(posX, posY)
		
        # 자동차 주행
        right, left = 1, 1
        if posY <= 0:
            right, left = 1, 1
        else : # posY > 0
            if -0.1 < posX < 0.1 :
                right, left = 0, 0
            elif posX < -0.1 : 
                right, left = 1, 0
            elif posX > 0.1 :
                right, left = 0, 1
		
        # print(right, left)
				
        rl = right << 1 | left
        rl_byte = struct.pack('B', rl)
        client_mot.sendall(rl_byte)

    def timeout(self):
        sender = self.sender()
        if id(sender) == id(self.timer):
            # print(self.joystickPosition())
		
            posX, posY = self.joystickPosition()
            # print(posX, posY)
            
            # 자동차 주행
            right, left = 1, 1
            if posY <= 0:
                right, left = 1, 1
            else : # posY > 0
                if -0.1 < posX < 0.1 :
                    right, left = 0, 0
                elif posX < -0.1 : 
                    right, left = 1, 0
                elif posX > 0.1 :
                    right, left = 0, 1
			
            # print(right, left)
            		
            rl = right << 1 | left
            rl_byte = struct.pack('B', rl)
            client_mot.sendall(rl_byte)			

# Create main application window
app = QApplication([])
app.setStyle(QStyleFactory.create("Cleanlooks"))
mw = QMainWindow()
mw.setWindowTitle('Joystick example')
mw.setGeometry(100, 100, 300, 200)

# Create and set widget layout
# Main widget container
cw = QWidget()
ml = QGridLayout()
cw.setLayout(ml)
mw.setCentralWidget(cw)

# Create Screen
label = QtWidgets.QLabel()
ml.addWidget(label,0,0)

# Create joystick
joystick = Joystick()
ml.addWidget(joystick,1,0)

mw.show()

th = threading.Thread(target=run)
th.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
	QApplication.instance().exec_()
		
