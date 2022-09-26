import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import socket
import time
import struct
import numpy as np

HOST_CAM = '192.168.137.42'
PORT = 80

running = False
def run():
	global running
	
	client_cam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_cam.connect((HOST_CAM, PORT))

	t_now = time.time()
	t_prev = time.time()
	cnt_frame = 0

	width = 320
	height = 240
	label.resize(width, height)
	while running:	

		# 영상 받기
		data_len_bytes = client_cam.recv(4)
		data_len = struct.unpack('I', data_len_bytes)
		data = client_cam.recv(data_len[0], socket.MSG_WAITALL)

		# 영상 출력
		np_data = np.frombuffer(data, dtype='uint8')
		frame = cv2.imdecode(np_data,1)
		frame = cv2.rotate(frame,cv2.ROTATE_180)
		frame2 = cv2.resize(frame, (320, 240))

		img = frame2

		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
		h,w,c = img.shape
		qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
		pixmap = QtGui.QPixmap.fromImage(qImg)
		label.setPixmap(pixmap)

		cnt_frame += 1
		t_now = time.time()
		if t_now - t_prev >= 1.0 :
			t_prev = t_now
			print("frame count : %f" %cnt_frame)
			cnt_frame = 0

	client_cam.close()
	print("Thread end.")
	

def stop():
	global running
	running = False
	print("stoped..")

def start():
	global running
	running = True
	th = threading.Thread(target=run)
	th.start()
	print("started..")

def onExit():
	print("exit")
	stop()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel()
btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
vbox.addWidget(label)
vbox.addWidget(btn_start)
vbox.addWidget(btn_stop)
win.setLayout(vbox)
win.show()

btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
app.aboutToQuit.connect(onExit)

sys.exit(app.exec_())