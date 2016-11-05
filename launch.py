#python packages
import thread
import threading
import time

import sys
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Sensors/Temperature")
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Sensors/magnetometer")
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Sensors/Geiger_Counter")
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Camera")


from camera import *
from temperature import *
from magnetometer import *
from Geiger_Counter import *


def operateCamera():
	while True:
		takeVideo();

def handleArduinoSensor(thread_name):
	while True:
		pass


def handleRaspberryPiGPIO():
	while True:
		pass

def sendToRadio():
	pass

def readPressureSensor():
	pass



def main():
	thread.start_new_thread(operateCamera, ())
	thread.start_new_thread(external_arduino, ())
	thread.start_new_thread(handleRaspberryPiGPIO, ())
	thread.start_new_thread(handleRaspberryPiGPIO, ())
	threading.Timer(60, sendToRadio).start()



if __name__ == "__main__":
	main();
