from Adafruit_BME280 import *
import json
import time

sensor = BME280(mode=BME280_OSAMPLE_8)

def getTemperatureReadingJSON():
	degrees = sensor.read_temperature()
	pascals = sensor.read_pressure()
	humidity = sensor.read_humidity()
	dictionary = {"temperature" : degrees,
				  "pressure" : pascals,
				  "humidity" : humidity,
				  "time" : time.time()}

	return json.dumps(dictionary)
