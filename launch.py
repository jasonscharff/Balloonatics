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
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Camera")


from camera import *
from temperature import *


#arduino links
BAUD_RATE = 9600
#genericArduinoSerial = serial.Serial('/dev/ttyACM0', BAUD_RATE)
#pressureSerial = serial.Serial('/dev/ttyACM1', BAUD_RATE)
#radioSerial = serial.Serial('/dev/ttyACM2', BAUD_RATE)
#gpsSerial = serial.Serial('/dev/ttyACM3', BAUD_RATE)



#filenames
GENERIC_ARDUINO_FILENAME = ''
GENERIC_ARDUINO_KEYS = ['time', 'geiger_count']

GPS_ARDUINO_FILENAME = ''
GPS_ARDUINO_KEYS = ['time', 'gps_timestamp', 'lat', 'lat_direction', 
'lng', 'lng_direction', 'fix_quality', 'num_satelites','hdop', 'altitude', 'height_geoid_ellipsoid']

PRESSURE_ARDUINO_FILENAME = ''
PRESSURE_ARDUINO_KEYS = ['time', 'raw_exterior_pressure']

GPIO_FILENAME = ''
GPIO_KEYS = getTemperatureKeys()

#radio
#radio dictionary will be formatted with the name of the csv and then contain an array of dictionaries with of the last data
#the dictionaries will contain timestamps.
RADIO_DICTIONARY = {}


def operateCamera():
    while True:
        takeVideo();

def handleSerialInput(serial, responseFunction):
    while True:
        serialInput = serial.readline()
        if serialInput is not None and len(serialInput) > 0:
            responseFunction(serialInput)

def handleGenericArduinoSensor():
    def genericArduinioFunction(serialInput):
        dictionaryRepresentaion = json.loads(serialInput)
        geiger_value = dictionaryRepresentaion['geiger_cpm']
        addValueToCSV(GENERIC_ARDUINO_FILENAME, GENERIC_ARDUINO_KEYS, {'geiger_cpm' : geiger_value})

    handleSerialInput(genericArduinoSerial, genericArduinioFunction)

def handleGPSData():
    def gpsHandler(string):
        if string.startswith('$GPGGA'):
            components = string.split(',')
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
                        'lng_direction' : lng_direction, 
                        'fix_quality' : fix_quality, 
                        'num_satelites' : num_satelites, 
                        'hdop' : hdop, 
                        'altitude' : altitude, 
                        'height_geoid_ellipsoid' : height_geoid_ellipsoid}
            addValueToCSV(GPS_ARDUINO_FILENAME, GPS_ARDUINO_KEYS, dictionary)

        handleSerialInput(gpsArduinoSerial, gpsHandler)



def handleRaspberryPiGPIO():
    while True:
        tempDictionary = getTemperatureReadingJSON()
        addValueToCSV(GPIO_FILENAME, GPIO_KEYS, tempDictionary)
        time.sleep(1)

def sendToRadio():
    #convert to json
    jsonified = json.dumps(RADIO_DICTIONARY)
    #send to radio which will beam down
    radioSerial.write(jsonified)

def handlePressureSensor():
    def pressureFunction(serialInput):
        dictionaryRepresentaion = json.loads(serialInput)
        pressure = dictionaryRepresentaion['raw_exterior_pressure']
        addValueToCSV(GENERIC_ARDUINO_FILENAME, GENERIC_ARDUINO_KEYS, {'raw_exterior_pressure' : pressure})

    handleSerialInput(pressureSerial, pressureFunction)
        

def addValueToCSV(filename, keys, dictionary):
    dictionary = filteredDictionary(dictionary)
    
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

def main():
    createCSVs()
   # thread.start_new_thread(operateCamera, ())
#   thread.start_new_thread(handleGenericArduinoSensor, ())
#   thread.start_new_thread(handlePressureSensor, ())
	handleRaspberryPiGPIO()
   # thread.start_new_thread(handleRaspberryPiGPIO, ())
#   thread.start_new_thread(handleGPSData, ())
#   threading.Timer(60, sendToRadio).start()


if __name__ == "__main__":
    main();
