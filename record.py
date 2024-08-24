from picamera2 import Picamera2  # camera interface library
import cv2 # image processing library
import time # current time details library
from gpiozero import Button

# initialize camera and set its configuration (480p resolution)
cam = Picamera2()
config = cam.create_preview_configuration(main={"size": (640, 480)})
cam.configure(config)  
cam.start()  


fourcc = cv2.VideoWriter_fourcc(*'avc1') #(*'MP42')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

button = Button(26)

print("started")

while button.is_pressed:
    frame = cam.capture_array()  
    frame = cv2.resize(frame, (640, 480))
    out.write(frame)

print("complete")
# Release everything if job is finished
out.release()