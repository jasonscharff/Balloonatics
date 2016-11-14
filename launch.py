#python packages
from __future__ import division
import thread
import threading
import time
import json
import serial
import csv
import uuid
import math

#insert modules as needed
import sys
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Sensors/Temperature")
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Camera")


from camera import *
from temperature import *


#arduino links
BAUD_RATE = 9600

genericArduinoSerial = None
gpsSerial = None
pressureSerial = None
radioSerial = None


#filenames
GENERIC_ARDUINO_FILENAME = ''
GENERIC_ARDUINO_KEYS = ['time', 'geiger_cpm']

GPS_ARDUINO_FILENAME = ''
GPS_ARDUINO_KEYS = ['time', 'gps_timestamp', 'lat', 'lat_direction', 
'lng', 'lng_direction', 'fix_quality', 'num_satelites','hdop', 'altitude', 'height_geoid_ellipsoid']

PRESSURE_ARDUINO_FILENAME = ''
PRESSURE_ARDUINO_KEYS = ['time', 'exterior_pressure', 'exterior_humidity', 'exterior_temperature', 'estimated_altitude', 'sound_time','blue_voltage', 'red_voltage', 'white_voltage']

GPIO_FILENAME = ''
GPIO_KEYS = getTemperatureKeys()

#radio
#radio dictionary will be formatted with the name of the csv and then contain an array of dictionaries with of the last data
#the dictionaries will contain timestamps.
RADIO_DICTIONARY = {}

#altitude
NUM_TIMES_ALTITUDE_REACHED = 0
ALTITUDE_THRESHOLD = 30000 #in m

#pressure
NUM_TIMES_PRESSURE_REACHED = 0
PRESSURE_THRESHOLD = 98750 #in Pa

#time
currentTime = time.time()
TIME_THRESHOLD = 3600 #1 hour

CUTOFF_SIGNAL = 'c'


def operateCamera():
    while True:
        takeVideo();
        takePhoto();

def handleSerialInput(serial, responseFunction):
    while True:
        serialInput = str(serial.readline())
        if serialInput is not None and len(serialInput) > 0:
            responseFunction(serialInput)

def handleGenericArduinoSensor():
    def genericArduinioFunction(serialInput):
        try:
            serialInput = serialInput.replace('\r', '')
            serialInput = serialInput.replace('\n', '')
            dictionaryRepresentaion = json.loads(serialInput)
            addValueToCSV(GENERIC_ARDUINO_FILENAME, GENERIC_ARDUINO_KEYS, dictionaryRepresentaion)
        except:
            pass

    handleSerialInput(genericArduinoSerial, genericArduinioFunction)

def handleGPSData():
    def gpsHandler(string):
        if string.startswith('$GPGGA'):
            components = string.split(',')
            if len(components) >= 12:
                gps_timestamp = components[1]
                lat = components[2]
                directionLat = components[3]
                lng = components[4]
                directionLng = components[5]
                fix_quality = components[6]
                num_satelites = components[7]
                hdop = components[8]
                altitude = components[9]
                height_geoid_ellipsoid = components[11]
                dictionary = {'gps_timestamp': gps_timestamp, 
                        'lat' : lat, 
                        'lat_direction' : directionLat, 
                        'lng' : lng,
                        'lng_direction' : directionLng, 
                        'fix_quality' : fix_quality, 
                        'num_satelites' : num_satelites, 
                        'hdop' : hdop, 
                        'altitude' : altitude, 
                        'height_geoid_ellipsoid' : height_geoid_ellipsoid}
                addValueToCSV(GPS_ARDUINO_FILENAME, GPS_ARDUINO_KEYS, dictionary)

    handleSerialInput(gpsSerial, gpsHandler)



def handleRaspberryPiGPIO():
    while True:
        tempDictionary = getTemperatureReadingJSON()
        addValueToCSV(GPIO_FILENAME, GPIO_KEYS, tempDictionary)
        time.sleep(1)

def sendToRadio():
    #convert to json
    jsonified = json.dumps(RADIO_DICTIONARY)
    #hope one of the 1000 times works.
    for i in xrange(0,1000):
        radioSerial.write(jsonified + '\n')
    threading.Timer(5, sendToRadio).start()

def handlePressureSensor():
    def pressureFunction(serialInput):
        try:
            dictionaryRepresentaion = json.loads(serialInput)
            addValueToCSV(PRESSURE_ARDUINO_FILENAME, PRESSURE_ARDUINO_KEYS, dictionaryRepresentaion)
            pressure = dictionaryRepresentaion['exterior_pressure']
            if pressure is not None:
                if pressure > PRESSURE_THRESHOLD:
                    NUM_TIMES_PRESSURE_REACHED += 1
                if NUM_TIMES_PRESSURE_REACHED > 30:
                    pressureSerial.write(CUTOFF_SIGNAL)
        except:
            pass

    handleSerialInput(pressureSerial, pressureFunction)

def backupTrigger():
	global currentTime
	if(currentTime - startTime > TIME_THRESHOLD):
		pressureSerial.write(CUTOFF_SIGNAL)
	currentTime = time.time()
	threading.Timer(5, backupTrigger).start()

#pressure in pascals        
def getAltitudeFromPressure(pressure):
    pressure /= 1000
    if pressure > 22.707:
        altitude = 44397.5-44388.3 * ((pressure/101.29) ** .19026)
    elif pressure < 2.483:
        altitude = 72441.47 * ((pressure/2.488) ** -.0878) - 47454.96
    else:
        altitude = 11019.12 - 6369.43 * math.log(pressure/22.65)
    return altitude

def addValueToCSV(filename, keys, dictionary):
    dictionary = filterCSVDictionary(keys, dictionary)
    
    if filename in RADIO_DICTIONARY:
        array = RADIO_DICTIONARY[filename]
    else:
        array = []

    array.append(dictionary)
    RADIO_DICTIONARY[filename] = array
    
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
    global GENERIC_ARDUINO_FILENAME
    GENERIC_ARDUINO_FILENAME = BASE_DIRECTORY + "arduino_one" + str(uuid.uuid4()) + ".csv"
    createCSV(GENERIC_ARDUINO_FILENAME, GENERIC_ARDUINO_KEYS)

    global GPS_ARDUINO_FILENAME
    GPS_ARDUINO_FILENAME = BASE_DIRECTORY + "gps" + str(uuid.uuid4()) + ".csv"
    createCSV(GPS_ARDUINO_FILENAME, GPS_ARDUINO_KEYS)

    global PRESSURE_ARDUINO_FILENAME
    PRESSURE_ARDUINO_FILENAME = BASE_DIRECTORY + "pressure" + str(uuid.uuid4()) + ".csv"
    createCSV(PRESSURE_ARDUINO_FILENAME, PRESSURE_ARDUINO_KEYS)

    global GPIO_FILENAME
    GPIO_FILENAME = BASE_DIRECTORY + 'gpio' + str(uuid.uuid4()) + '.csv'
    createCSV(GPIO_FILENAME, GPIO_KEYS)


def createCSV(filename, keys):
    with open(filename, 'wb') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()

def openSerial():
    global genericArduinoSerial
    global gpsSerial
    global pressureSerial
    global radioSerial
    
    while genericArduinoSerial == None:
        try:
            genericArduinoSerial = serial.Serial('/dev/ttyACM0', BAUD_RATE)
        except:
            genericArduinoSerial = None

    while gpsSerial == None:
        try:
            gpsSerial = serial.Serial('/dev/ttyACM1', BAUD_RATE)
        except:
            gpsSerial = None
    while pressureSerial == None:
        try:
            pressureSerial = serial.Serial('/dev/ttyACM2', BAUD_RATE)
        except:
            pressureSerial = None
    while radioSerial == None:
        try:
            radioSerial = serial.Serial('/dev/ttyACM3', 4800)
        except:
            radioSerial = None

def main():
    openSerial();
    global startTime
    startTime = time.time()
    createCSVs()
    thread.start_new_thread(operateCamera, ())
    thread.start_new_thread(handleGenericArduinoSensor, ())
    thread.start_new_thread(handleGPSData, ())
    thread.start_new_thread(handlePressureSensor, ())
    threading.Timer(300, backupTrigger).start()
    threading.Timer(60, sendToRadio).start()
#something needs to occupy the main thread it appears from prelminary testong.
    handleRaspberryPiGPIO()
    
   
    
    


main()
