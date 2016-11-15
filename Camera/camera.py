from picamera import PiCamera
import time
import uuid
camera = PiCamera()

BASE_DIRECTORY = '/home/pi/Desktop/'

#take a picture and save it

def takePhoto():
	directory = BASE_DIRECTORY + 'photos/'
	image_name = str(time.time()) + "_" + str(uuid.uuid1()) + '.jpg'
	camera.capture(directory + image_name)

def takeVideo():
	directory = BASE_DIRECTORY + 'videos/'
	video_name = str(time.time()) + '_' + str(uuid.uuid1()) + '.h264'
	camera.start_recording(directory + video_name)
	time.sleep(300)
	camera.stop_recording()
