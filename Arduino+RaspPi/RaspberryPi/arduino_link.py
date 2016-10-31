import serial
import time

BAUD_RATE = 9600

ser = serial.Serial('/dev/ttyACM0', BAUD_RATE)

def readArduino():
	while True:
		text = ser.readline()
		print text

def sendArduino(string):
	ser.write(string)


while True:
	sendArduino("Hello Arduino")
	time.sleep(30)





