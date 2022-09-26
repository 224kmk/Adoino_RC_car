from PyQt5.QtWidgets import *
import sys
				
from myjoystick import MyJoystick
			
def cbJoyPos(joystickPosition) :
	posX, posY = joystickPosition
		
	# 자동차 방향
	right, left = -1, -1
	if posY < -0.5:
		right, left = 1, 1
		print('brake')
	elif posY > 0.15 :
		if -0.15 <= posX <= 0.15 :
			right, left = 0, 0
			print('forward')
		elif posX < -0.15 : 
			right, left = 1, 0
			print('left')
		elif posX > 0.15 :
			right, left = 0, 1
			print('right')
	else : # -0.5 <= posY <= 0.15
		print('stop driving')

# Create main application window
app = QApplication([])
app.setStyle(QStyleFactory.create("Cleanlooks"))
mw = QMainWindow()
mw.setWindowTitle('RC Car Joystick')
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