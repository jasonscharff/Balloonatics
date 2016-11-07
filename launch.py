#python packages
import thread
import threading
import time
import json
import serial
import csv
import uuid

#insert modules as needed
import sys
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Sensors/Temperature")
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Sensors/magnetometer")\
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Camera")


from camera import *
from temperature import *
from magnetometer import *


#arduino links
BAUD_RATE = 9600
genericArduinoSerial = serial.Serial('/dev/ttyACM0', BAUD_RATE)
# radioSerial = serial.Serial('/dev/ttyACM1', BAUD_RATE)
# cutDownSerial = serial.Serial('/dev/ttyACM2', BAUD_RATE)
# pressureSerial = serial.Serial('/dev/ttyACM3', BAUD_RATE)


#filenames
GENERIC_ARDUINO_FILENAME = ''
GENERIC_ARDUINO_KEYS = ['time', 'geiger_count']


def operateCamera():
	while True:
		takeVideo();

def handleArduinoSensor():
	while True:
		serialInput = genericArduinoSerial.readline()
		if(serialInput is not None and len(serialInput) > 0):
			dictionaryRepresentaion = json.loads(serialInput)
			geiger_value = dictionaryRepresentaion['geiger_cpm']
			addValueToCSV(GENERIC_ARDUINO_FILENAME, GENERIC_ARDUINO_KEYS, {'geiger_cpm' : geiger_value})


def handleRaspberryPiGPIO():
	while True:
		pass

def sendToRadio():
	pass

def readPressureSensor():
	pass



def addValueToCSV(filename, keys, dictionary):
	dictionary = filteredDictionary(dictionary)
	with open(filename, 'a') as file:
    	writer = csv.DictWriter(file, keys)
        writer.writerow(dictionary)

def filterCSVDictionary(keys, dictionary):
	filteredDictionary = {}
	for key in keys:
		if not key in dictionary:
			#add time if not already there
			if key == 'time':
				filteredDictionary[key] = time.time()
			else:
				filteredDictionary[key] = ''
		else:
			filteredDictionary[key]= dictionary[key]
	return filteredDictionary


def createCSVs():
	BASE_DIRECTORY = '/home/pi/Desktop/data/'

	#create csv for geiger counter
	GENERIC_ARDUINO_FILENAME = BASE_DIRECTORY + "arduino_one" + str(uuid.uuid4()) + ".csv"
	GENERIC_ARDUINO_KEYS = ['time', 'geiger_count']
	createCSV(GENERIC_ARDUINO_FILENAME, GENERIC_ARDUINO_KEYS)


def createCSV(filename, keys):
	with open(filename, 'wb') as file:
		dict_writer = csv.DictWriter(file, keys)
		dict_writer.writeheader()

def main():
	createCSVs()
	thread.start_new_thread(operateCamera, ())
	thread.start_new_thread(external_arduino, ())
	thread.start_new_thread(handleArduinoSensor, ())
	thread.start_new_thread(handleRaspberryPiGPIO, ())
	threading.Timer(60, sendToRadio).start()


if __name__ == "__main__":
	main();
