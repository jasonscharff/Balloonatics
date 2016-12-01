'''
    File name: temperature.py
    Author: Jason Scharff
    Python Version: 2.7
    Description: Provides a wrapper around the Adafruit_BME280 combined temperature/humidity/pressure sensor.
    Provides conviennce function to take a reading of each datapoint from the attached BME280 sensor
    and return it as a Python Dictionary object.
'''


#import ADAFruit BME280 python library.
from Adafruit_BME280 import *
#import time module to add timestamp to reading
import time

#create sensor object.
sensor = BME280(mode=BME280_OSAMPLE_8)

#function to return a reading from the interior temperature sensor as a dictionary
def get_temperature_reading():
	#read the temperature in degrees celsius
	degrees = sensor.read_temperature()
	#read the pressure in pascals
	pascals = sensor.read_pressure()
	#read the humidity in percentage form
	humidity = sensor.read_humidity()

	#create a dictioanry object from the data and add the current timestamp
	dictionary = {"temperature" : degrees,
				  "pressure" : pascals,
				  "humidity" : humidity,
				  "time" : time.time()}

	#return a dictionary of the data.
	return dictionary

#function to return keys used in the reading dictionary to allow data to be saved as a CSV.
def get_temperature_keys():
	#returns a python list of the keys used in the dictionary returned by get_temperature_reading_json
	return ['temperature', 'pressure', 'humidity', 'time']
