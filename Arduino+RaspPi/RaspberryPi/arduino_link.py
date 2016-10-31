import serial
import time

BAUD_RATE = 9600

ser = serial.Serial('/dev/ttyACM0', BAUD_RATE)

def readArduino():
	while True:
		text = ser.readline()
		print text

def sendArduino(string):
	ser.write('Hello, Arduino!')


while True:
	sendArduino()
	time.sleep(5)





