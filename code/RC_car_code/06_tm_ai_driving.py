import socket
import time
import struct
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps

HOST_CAM = '192.168.137.220'
HOST_MOT = '192.168.137.86'
PORT = 80

client_cam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_mot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_cam.connect((HOST_CAM, PORT))
client_mot.connect((HOST_MOT, PORT))

t_now = time.time()
t_prev = time.time()
cnt_frame = 0

model = load_model('keras_model.h5')

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

names = ['_0_forward', '_1_right', '_2_left', '_3_stop']

while True:

	# 영상 보내
	cmd = 12
	cmd = struct.pack('B', cmd)
	client_cam.sendall(cmd)

	# 영상 받기
	data_len_bytes = client_cam.recv(4)
	data_len = struct.unpack('I', data_len_bytes)

	_data = client_cam.recv(data_len[0], socket.MSG_WAITALL)

	# 영상 출력
	np_data = np.frombuffer(_data, dtype='uint8')
	frame = cv2.imdecode(np_data,1)
	frame = cv2.rotate(frame,cv2.ROTATE_180)
	frame2 = cv2.resize(frame, (320, 240))
	cv2.imshow('frame', frame2)

	image = Image.fromarray(frame)

	size = (224, 224)
	image = ImageOps.fit(image, size, Image.ANTIALIAS)

	#turn the image into a numpy array
	image_array = np.asarray(image)
	# Normalize the image
	normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
	# Load the image into the array
	data[0] = normalized_image_array

	# run the inference
	y_predict = model.predict(data)

	y_predict = np.argmax(y_predict,axis=1)
	print(names[y_predict[0]], y_predict[0])

	# send y_predict
	cmd = y_predict[0].item()
	cmd = struct.pack('B', cmd)
	client_mot.sendall(cmd)

	key = cv2.waitKey(1)
	if key == 27:
		break

	cnt_frame += 1
	t_now = time.time()
	if t_now - t_prev > 1.0 :
		t_prev = t_now
		print("frame count : %f" %cnt_frame)
		cnt_frame = 0

client_cam.close()
client_mot.close()