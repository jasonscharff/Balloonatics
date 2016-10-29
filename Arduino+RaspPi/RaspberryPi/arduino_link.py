import serial

BAUD_RATE = 9600

ser = serial.Serial('/dev/ttyACM0', BAUD_RATE)

def readArduino():
	while True:
		text = ser.readline()
		print text

readArduino()
