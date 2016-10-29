import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

def readArduino():
	while True:
		text = ser.readline()
		print text
		