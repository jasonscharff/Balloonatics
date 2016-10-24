import serial

#constants
BAUD_RATE = 9600
SERIAL_PATH = '/dev/ttyACM0'

ser = serial.Serial(SERIAL_PATH,BAUD_RATE)
s = [0]
while True:
	read_serial=ser.readline()
	s[0] = str(int (ser.readline(),16))
	print s[0]
	print read_serial
