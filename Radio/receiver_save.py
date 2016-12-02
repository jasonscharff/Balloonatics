#
import os
BASE_DIRECTORY = os.path.expanduser('~/Documents/ASR_Balloonatics/')
BAUD_RATE = 4800
import serial
import uuid
import time

FILENAME = ''


def readSerial(port):
    ser = serial.Serial(port, BAUD_RATE)
    while True:
        serialInput = ser.readline();
        if serialInput is not None and len(serialInput) > 0:
            print (serialInput)
            appendToFile(serialInput)

def appendToFile(string):
    with open(FILENAME, "a") as file:
        file.write(string)

def createFile():
    global FILENAME
    FILENAME =  BASE_DIRECTORY + 'radio_response' + str(uuid.uuid4()) + '.txt'
    with open(FILENAME, 'w') as file:
        file.write('BEGIN AT ' + str(time.time()))

createFile()




