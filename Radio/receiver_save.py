'''
    File name: receiver_save.py
    Author: Jason Scharff
    Python Version: 2.7
    Description: Provides a way to save serial output to a text file. 

    The radio receiver Arduino prints the data it receives to the Serial console. 
    However, the Arduino IDE does not provide an easy way to save the Serial data. 
    This Python script creates a file and then saves all of the data received 
    over serial to that file.

    This is designed to be use a command line utility with a simple call to read_serial with
    the port to read from as the sole parameter.
'''

#import the os module in order to use the expanduser function to use the ~ to represent the user's home folder.
import os
#import the serial module in order to interface with Serial as the Arduino prints the received data using Serial.
import serial
#import the uuid module to append a random uuid to the filename ensuring no overwrites due to conflicting filenames.
import uuid
#import the time module to mark the time at which the file was created.
import time

#the directory in which to save the file. 
#will crash if this directory does not exist.
BASE_DIRECTORY = os.path.expanduser('~/Documents/ASR_Balloonatics/')
#baud rate in which the receiver sends data over.
BAUD_RATE = 4800

#initialize a global variable to store the name of the file the serial output is saved to.
FILENAME = ''


#function to begin the process of saving data received over serial.
#arg, port: the serial port in which to read the data from. Depends on the USB port used to plug the Arduino into.
def read_serial(port):
	#initialize a serial object at the specified port using the predefined baud rate.
    ser = serial.Serial(port, BAUD_RATE)
    #read forever (or until manually stopped by user)
    while True:
    	#read any input from the Arduino receiver over serial.
        serial_input = ser.readline();
        #check if we received anything of interest from the serial read/
        if serial_input is not None and len(serial_input) > 0:
        	#print the serial_input to provide feedback via the command utility of the received data.
            print (serial_input)
            #add the data to the file
            append_to_file(serial_input)

#function to append the received string to the file.
#arg, string: the string in which to append to the file.
def append_to_file(string):
	#open the global variable filename in append mode as variable file.
    with open(FILENAME, "a") as file:
    	#append the string to the file.
        file.write(string)

#function to create the file to save the data to.
def create_file():
	#use the global variable FILENAME instead of creating a new instance variable.
    global FILENAME
    #set the filename equal to the directory we want to save to _+ radio_response + a uuid to enforce uniqueness + '.txt'
    #as it is a text file.
    FILENAME =  BASE_DIRECTORY + 'radio_response' + str(uuid.uuid4()) + '.txt'
    #create and open the file.
    with open(FILENAME, 'w') as file:
    	#write the time in which the file was created
        file.write('BEGIN AT ' + str(time.time()))

#create the file when this script is run.
create_file()





