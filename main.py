from picamera2 import Picamera2, Preview
import time

cam = Picamera2()
camera_config = cam.create_preview_configuration()
cam.configure(camera_config)
cam.start_preview(Preview.NULL)
cam.start()
time.sleep(2)
cam.capture_file("test.jpg")
