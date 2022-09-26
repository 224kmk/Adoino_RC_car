import socket
import time
import struct

HOST_CAM = '192.168.137.108'
PORT = 80

client_cam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_cam.connect((HOST_CAM, PORT))

while True:

	cmd = 12
	cmd = struct.pack('B', cmd)
	client_cam.sendall(cmd)

	time.sleep(1)

client_cam.close()