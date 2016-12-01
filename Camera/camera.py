'''
    File name: camera.py
    Author: Jason Scharff
    Python Version: 2.7
    Description: Provides a wrapper around the picamera module to provide convinence
    functions to take both photos and video and save them with a standardized naming scheme
    in a standardized location.
'''


#import the picamera module to interact with the standard raspberry pi camera.
from picamera import PiCamera
#import the time module to assign timestamps to our filenames and allow sleeping.
import time
#import the uuid module to assign a uuid to each filename to enforce uniqueness to avoid file overrwrites
import uuid

#create global camera object
camera = PiCamera()

#set camera resolution to 720p
camera.resolution = (1280, 720)

#the base directory for which to save photos/videos.
BASE_DIRECTORY = '/home/pi/Desktop/'

#function to take a picture and save it
def take_photo():
	#directory of photos is BASE + folder called photos
	#if the folder doesn't exist an exception will be thrown so this should exist.
	directory = BASE_DIRECTORY + 'photos/'
	#create a name for the image equal to the timestamp_a uuid.jpg
	image_name = str(time.time()) + "_" + str(uuid.uuid1()) + '.jpg'
	#actually take the photo and save it to the appropriate directory.
	camera.capture(directory + image_name)

#function to take 5 minute video and save it
#will thus take 5 minutes to return.
def take_video():
	#directory of photos is BASE + folder called videos
	#if the folder doesn't exist an exception will be thrown so this should exist.
	directory = BASE_DIRECTORY + 'videos/'
	#create a name for the video equal to the timestamp_a uuid.jpg
	video_name = str(time.time()) + '_' + str(uuid.uuid1()) + '.h264'
	#begin recording
	camera.start_recording(directory + video_name)
	#take video for 5 minutes
	time.sleep(300)
	#stop recording.
	camera.stop_recording()
