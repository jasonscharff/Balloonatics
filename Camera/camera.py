from picamera import PiCamera
camera = PiCamera()
import uuid

BASE_DIRECTORY = '/home/pi/Desktop/photos/'

#take a picture and save it
image_name = uuid.uuid1() + '.jpg'
camera.capture(BASE_DIRECTORY + image_name)