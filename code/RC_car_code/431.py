import socket
import time
import struct
import numpy as np
import cv2

HOST_CAM = '192.168.137.108'
PORT = 80

client_cam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_cam.connect((HOST_CAM, PORT))

while True:

	# 영상 보내
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
	cv2.imshow('frame', frame2)

	key = cv2.waitKey(1)
	if key == 27:
		break

client_cam.close()