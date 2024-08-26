from picamera2 import Picamera2
import cv2
import time
from gpiozero import Button
import time

# Initialize camera and set its configuration (480p resolution)
cam = Picamera2()
config = cam.create_preview_configuration(main={"size": (640, 480)})
cam.configure(config)
cam.start()

# Use 'mp4v' codec for MP4 files
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

button = Button(26)

print("started")

# Loop until the button is released
while True:
    if button.is_pressed:
        frame = cam.capture_array()
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
    else:
        break  # Stop recording when the button is released

print("complete")
# Release everything if job is finished
time.sleep(0.5)
out.release()
