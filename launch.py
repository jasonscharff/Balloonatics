#python packages

#avoid integer division issues globally by using Python3 Divison
from __future__ import division

#used to run background threads
import thread
#used to keep central time for data
import time
#information sent from arduinos are in JSON format
import json
#communication with arduino is done over serial
import serial
#all data is stored as a csv
import csv
#filenames contain random uuids to ensure nothing is ever overwritten.
import uuid
#used for the altitude calculation function.
import math

#insert files into the directory
import sys
#code for interior temperature sensor
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Sensors/Temperature")
#code for camera
sys.path.insert(0, "/home/pi/Desktop/Balloonatics/Camera")

#import functions to operate camera
from camera import *
#import code to handle interior temperature
from temperature import *

#standard baud rate for communication with arduinos
BAUD_RATE = 9600

#initialize serial communication with geiger arduino to None to declare as global variable
geiger_serial = None

#initialize serial communication with gps arduino to None to declare as global variable
gps_serial = None

#initialize serial communication with pressure arduino to None to declare as global variable
pressure_serial = None

#Base directory to store data
BASE_DIRECTORY = '/home/pi/Desktop/data/'

#filename of csv used to store geiger counter data
GEIGER_ARDUINO_FILENAME = ''

#keys/column names for the csv used to store information from the geiger counter arduino
GEIGER_ARDUINO_KEYS = ['time', 'geiger_cpm', 'anemometer_rpm']

#filename of csv used to store gps data
GPS_ARDUINO_FILENAME = ''

#keys/column names for the csv used to store information from the gps arduino
GPS_ARDUINO_KEYS = ['time', 'gps_timestamp', 'lat', 'lat_direction', 
'lng', 'lng_direction', 'fix_quality', 'num_satelites','hdop', 'altitude', 'height_geoid_ellipsoid']

#filename of csv used to store data from pressure arduino
PRESSURE_ARDUINO_FILENAME = ''

#keys/column names for the csv used to store information from the pressure arduino
PRESSURE_ARDUINO_KEYS = ['time', 'exterior_pressure', 'exterior_humidity', 'exterior_temperature', 'estimated_altitude', 'sound_time','blue_voltage', 'red_voltage', 'white_voltage']

#filename of csv used to store data from gpio pin connected sensors
GPIO_FILENAME = ''

#keys/column names for the csv used to store information from sensors connected to the gpio pins.
#only thing connected to the gpio pins if the interior temperature sensor. Get keys from function in the temperature.py file.
GPIO_KEYS = get_temperature_keys()


#pressure/cutdown

#intiialize array containing last pressure samples which will be used to determine when to cutdown
last_pressure_samples = []

#number of previous pressure samples to keep track of in order to determine when to cut down.
NUM_PRESSURE_SAMPLES = 60

#minimum pressure to trigger cutdown. Approximate pressure at 28,000 meters
PRESSURE_THRESHOLD = 1560 #in Pa

#boolean to indicate whether or not the cutdown has triggered to avoid cutting it down multiple times.
#initially set to false.
has_cut_down = False

#initialize a global variable of when the data collection started. Intialized to the correct
#value once all arduinos are plugged in
start_time = None

#minimum time needed before cutdown
TIME_THRESHOLD = 3600 #1 hour

#signal to send to arduino when to cutoff.
CUTOFF_SIGNAL = 'c'

#function to continuously take a video and then a photo
#length of each video set by the camera.py module.
#should be called on separate thread to avoid blocking main thread.
def operate_camera():
    while True: #do forever
        take_video() #take a single video
        take_photo() #take a single photo

#function to handle serial input from the arduinos
#arg, serial: the serial object to read from
#arg, response_function: the function to call to handle the serial input.
#this function generally makes the code more concise by avoiding repeat serial reading code.
def handle_serial_input(serial, response_function):
    while True: #continuously read input from the serial
        serial_input = str(serial.readline()) #read up until the line from the serial. Line break
        if serial_input is not None and len(serial_input) > 0:
            response_function(serial_input)

#function to handle input from the geiger sensor arduino
def handle_geiger_sensor():
    #declare the function to handle the serial input which takes the input string as a parameter.
    def geiger_function(serial_input):
        #wrap in a try/catch in case the data is corrupted in transit
        try:
            #convert json input into a python dictionary object
            dictionary_representaion = json.loads(serial_input)
            #add the json serialzied dictionary onto the appropriate csv.
            add_value_to_csv(GEIGER_ARDUINO_FILENAME, GEIGER_ARDUINO_KEYS, dictionary_representaion)
        #exception thrown, likely from converting to json.
        except:
            #just ignore this data point. Not much we can do.
            pass

    #continuously get information from the geiger serial.
    handle_serial_input(geiger_serial, geiger_function)


#function to handle gps data
def handle_gps_data():
    #create a function to handle the serial input which takes the input string as a parameter.
    def gps_handler(string):
        #the gps will feed us a lot of data. We only need the GPGGA prefixed lines.
        if string.startswith('$GPGGA'):
            #the line is contains values separated by a comma. Split the lines into an array of components
            #using the comma as a delimetter.
            components = string.split(',')
            #if the line is too short because something got corrupted in transmission ignore it.
            if len(components) >= 12:
                #the timestamp given by the gps module is the first component
                gps_timestamp = components[1]
                #the latitude given by the gps is the second component
                lat = components[2]
                #the direction of lat (for example North) is the third component
                direction_lat = components[3]
                #the longitude given by the gps is the fourth component.
                lng = components[4]
                #the direction given by the gps is the fifth component
                direction_lng = components[5]
                #the fix quality is the sixth component.
                fix_quality = components[6]
                #the number of satelites found by the GPS is the seventh component
                num_satelites = components[7]
                #the horizontal dilution of precision (hdop) which gives the relative accuracy 
                #of the horizontal position is the eigth component
                hdop = components[8]
                #the estimated altitude from the gps module (in meters) is the 9th component
                altitude = components[9]
                #height of geoid above WGS84 ellipsoid is the eleventh component
                height_geoid_ellipsoid = components[11]

                #create a dictionary of the GPS data in order to add it to the csv
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

                #add the newly created dictionary to the appropriate csv file.
                add_value_to_csv(GPS_ARDUINO_FILENAME, GPS_ARDUINO_KEYS, dictionary)

    #continiously read from the gps serial.
    handle_serial_input(gps_serial, gps_handler)


#function to continuously read from the raspberry pi gpio pins (contains interior temperature data)
def handle_raspberry_pi_gpio():
    #read data forever
    while True:
        #call function in temperature module to get the temperature readings as a python dictionary
        dictionary = get_temperature_reading_json()
        #add the interior temperature reading to the csv
        add_value_to_csv(GPIO_FILENAME, GPIO_KEYS, dictionary)
        #wait a second before reading more data
        time.sleep(1)

#function to read data from pressure arduino
def handle_pressure_sensor():
    #declare function to handle serial input from pressure arduino
    def pressure_function(serial_input):
        #use the global variable last_pressure_samples which contains the last x number of pressure readings
        #instead of creating a new instance variable. 
        #an average of last_pressure_samples is used to trigger cutdown to avoid a singular blip
        #leading to a preliminary cutdown
        global last_pressure_samples
        try: #wrap serial reading in a try/catch to avoid corrupt data causing a crash
            #use global version of has_cut_down instead a new intance varaible. Avoids cutting down multiple times.
            global has_cut_down 
            #convert serial input into a python dictionary object.
            dictionary_representaion = json.loads(serial_input)
            #get the pressure from the json object in pascals.
            pressure = dictionary_representaion['exterior_pressure'] 
            #add arduino reading to appropriate csv
            add_value_to_csv(PRESSURE_ARDUINO_FILENAME, PRESSURE_ARDUINO_KEYS, dictionary_representaion)

            #check if pressure is a valid reading and we haven't cut down yet
            if pressure is not None and pressure > 0 and has_cut_down == False:
                #append the pressure reading into the array of last pressure readings
                last_pressure_samples.append(pressure)
                #get length of last_pressure_samples
                length = len(last_pressure_samples)
                #we only want to average the last NUM_PRESSURE_SAMPLES of pressure samples.
                #if the length is greater than the max we want to trim down the array
                if length > NUM_PRESSURE_SAMPLES:
                    #trim down last_pressure_samples to cap length at NUM_PRESSURE_SAMPLES 
                    last_pressure_samples = last_pressure_samples[NUM_PRESSURE_SAMPLES-length:]
                    #get average of last_pressure_samples
                    average = reduce(lambda x, y: x + y, last_pressure_samples) / length
                    #if the average of the last NUM_PRESSURE_SAMPLES > threshold we want to cutdown.
                    if average < PRESSURE_THRESHOLD:
                        cutdown()
        except: #something went wrong.
            #ignore this reading if an exception occurred
            pass

    #continuously read in data over serial from pressure arduino
    handle_serial_input(pressure_serial, pressure_function)

#function to trigger cutdown.
def cutdown():
    #use global version of has_cut_down to avoid creating new local variable.
    global has_cut_down
    #create local variable current time to the current time to check against a time threshold
    current_time = time.time()
    #protection to avoid cutting down multiple times.
    if has_cut_down == False:
         #if the time elapsed is greater than a time threshold.
        if current_time - start_time > TIME_THRESHOLD:
            #set has_cut_down to True to avoid cutting down multiple times.
            has_cut_down = True
            #send the signal a bunch of times to be safe
            for i in xrange(0,20):
                #write the cutoff signal over serial to the arduino containing the cutoff mechanism.
                pressure_serial.write(CUTOFF_SIGNAL)
            #create a file to log the time of the cutdown
            filename =  BASE_DIRECTORY + 'cutdown' + str(uuid.uuid4()) + '.txt'
            #open the newly created file
            with open(filename, 'w') as file:
                #log the time at which it cutdown.
                file.write('CUTDOWN AT: ' + str(time.time()))


#pressure in pascals        
def get_altitude_from_pressure(pressure):
    pressure /= 1000
    if pressure > 22.707:
        altitude = 44397.5-44388.3 * ((pressure/101.29) ** .19026)
    elif pressure < 2.483:
        altitude = 72441.47 * ((pressure/2.488) ** -.0878) - 47454.96
    else:
        altitude = 11019.12 - 6369.43 * math.log(pressure/22.65)
    return altitude

#function to add the values from a dictionary into a given csv
#arg, filename: name of the csv
#arg, keys: keys the csv contains
#arg, dictionary: dictionary to write into the csv
def add_value_to_csv(filename, keys, dictionary):
    #filter the dictionary to add empty strings for keys not present
    #and add the time if it doesn't exist
    dictionary = filter_csv_dictionary(keys, dictionary)

    #open the csv file to write to in append mode to avoid overwriting existing data.
    with open(filename, 'a') as file:
        #intitialize a python csv dictwriter from the file and keys
        writer = csv.DictWriter(file, keys)
        #write the new row into the csv
        writer.writerow(dictionary)

#function to add ensure all keys are present in dictionary that should be present
#by adding empty strings and removes unnecessary keys. Prevents issues with writing to csv.
#also adds time to the dictionary if it does not exist as all
#csv dictionaries should contain timestamp.
#arg keys, final keys that should be used in the return dictionary
#arg dictionary, original dictionary to filter
def filter_csv_Dictionary(keys, dictionary):
    #create new dictionary which will be returned
    filtered_dictionary = {}
    #iterate through each key in the expected keys dictionary
    for key in keys:
        #if the expected key is not in the dictionary, add it
        if not key in dictionary:
            #add time if not in dictionary
            if key == 'time':
                filtered_dictionary[key] = time.time()
            else:
                #add the key as to the dictionary with the value empty string
                filtered_dictionary[key] = ''
        else:
            #use the original key value pair from the input dictionary
            filtered_dictionary[key]= dictionary[key]

    #return the filtered dictionary
    return filtered_dictionary

#function to create csvs to store data
def create_csvs():
    #use global variable base directory instead of creating a new instance variable
    #base directory is where the csvs will be saved.
    global BASE_DIRECTORY

    #create csv for geiger counter data

    #use global geiger arduino filename to avoid creating a new instance variable
    #so the filename is accessible from anywhere.
    global GEIGER_ARDUINO_FILENAME

    #set the name of the geiger counter csv to the save location + geiger + a uuid to enforce uniqueness.
    GEIGER_ARDUINO_FILENAME = BASE_DIRECTORY + "geiger" + str(uuid.uuid4()) + ".csv"

    #call a function to actually create the geiger csv.
    create_csv(GEIGER_ARDUINO_FILENAME, GEIGER_ARDUINO_KEYS)

    #create csv for gps data

    #use global gps arduino filename to avoid creating a new instance variable
    #so the filename is accessible from anywhere.
    global GPS_ARDUINO_FILENAME

    #set the name of the gps csv to the save location + gps + a uuid to enforce uniqueness.
    GPS_ARDUINO_FILENAME = BASE_DIRECTORY + "gps" + str(uuid.uuid4()) + ".csv"

    #call a function to actually create the gps csv.
    createCSV(GPS_ARDUINO_FILENAME, GPS_ARDUINO_KEYS)


    #use global pressure arduino filename to avoid creating a new instance variable
    #so the filename is accessible from anywhere.
    global PRESSURE_ARDUINO_FILENAME

    #set the name of the pressure csv to the save location + pressure + a uuid to enforce uniqueness.
    PRESSURE_ARDUINO_FILENAME = BASE_DIRECTORY + "pressure" + str(uuid.uuid4()) + ".csv"

    #call a function to actually create the pressure csv.
    createCSV(PRESSURE_ARDUINO_FILENAME, PRESSURE_ARDUINO_KEYS)


    #use global gpio data (interior temperature only) filename to avoid creating a new instance variable
    #so the filename is accessible from anywhere.
    global GPIO_FILENAME

    #set the name of the gpio csv to the save location + gpio + a uuid to enforce uniqueness.
    GPIO_FILENAME = BASE_DIRECTORY + 'gpio' + str(uuid.uuid4()) + '.csv'

    #call a function to actually create the gpio csv.
    createCSV(GPIO_FILENAME, GPIO_KEYS)


#function to create a csv with a given filename and keys
#arg, filename: the filename for the csv
#arg, keys: the keys for the csv. Used in the header
def create_csv(filename, keys):
    #create a file at the given location
    with open(filename, 'wb') as file:
        #create a dictionary csv written at the location of the newly created file with the given keys
        dict_writer = csv.DictWriter(file, keys)
        #write the header (the keys) of the csv.
        dict_writer.writeheader()

#function to create serial links with the arduinos connected to the USB ports.
#linux defines ports in the order devices are plugged in so the arduinos must be plugged 
#in a certain order. 
#this function will not return until all serial devices are found and will continue trying to find serials forever
#by not failing and continuously trying to find the serials it allows us to turn on the raspberry pi (which casues the script to run)
#even though the arduinos aren't plugged in. If the arduinos were already plugged in, the order would be random
#and we wouldn't know which arduino is which.
def open_serial():
    #use global geiger_serial so the serial can be accessible from everywhere.
    global geiger_serial

    #use global gps_serial so the serial can be accessible from everywhere.
    global gps_serial

    #use global pressure_serial so the serial can be accessible from everywhere.
    global pressure_serial
    
    #wait until the geiger_serial is created so that if the script is run at boot it doesn't find nothing and crash
    while geiger_serial == None:
        #if nothing is found an exception will be thrown. Protect against that crash
        try:
            #attempt to create the geiger serial at port 0 (assigned by Linux in the order devices are plugged in)
            #with the BAUD_RATE of the globally defined BAUD_RATE
            geiger_serial = serial.Serial('/dev/ttyACM0', BAUD_RATE)
        except: #something went wrong
            #set the geiger_serial to None
            geiger_serial = None

    #wait until the gps_serial is created so that if the script is run at boot it doesn't find nothing and crash
    while gps_serial == None:
        #if nothing is found an exception will be thrown. Protect against that crash
        try:
            #attempt to create the geiger serial at port 1 (assigned by Linux in the order devices are plugged in)
            #with the BAUD_RATE of the globally defined BAUD_RATE
            gps_serial = serial.Serial('/dev/ttyACM1', BAUD_RATE)
        except:
            #set the gps_serial to None
            gps_serial = None

    #wait until the pressure_serial is created so that if the script is run at boot it doesn't find nothing and crash
    while pressure_serial == None:  #if nothing is found an exception will be thrown. Protect against that crash
        try:
            #attempt to create the geiger serial at port 2 (assigned by Linux in the order devices are plugged in)
            #with the BAUD_RATE of the globally defined BAUD_RATE
            pressure_serial = serial.Serial('/dev/ttyACM2', BAUD_RATE)
        except:
            #set the geiger_serial to None
            pressure_serial = None

def main():
    #open serial connections to each of the arduinos. 
    #this function will not return until all the serials are found.    
    open_serial();
    #tell python to use the global variable start_time instead of creating a new local variable.
    global start_time
    #declare the global variable start time to the current time (which is the start time as data collection is about to begin)
    start_time = time.time()

    #create csv files to store the data
    create_csvs()

    #start taking photos/video on a new thread.
    thread.start_new_thread(operate_camera, ())

    #start getting data from the geiger sensor arduino on a new thread
    thread.start_new_thread(handle_geiger_sensor, ())

    #start getting data from the gps on a new thread.
    thread.start_new_thread(handle_gps_data, ())

    #start getting data from the pressure arduino on a new thread
    thread.start_new_thread(handle_pressure_sensor, ())

    #start collecting data from sensors attached to the GPIO pins (the interior temperature sensor)
    #something needs to be occupying the main thread for the program to not return
    #so execute this on the main thread. Note that the main thread function must be last
    #to avoid the program from never executing anything below the main thread blocking function.
    handle_raspberry_pi_gpio()
    

#call the main function to begin the data collection process.
main()
