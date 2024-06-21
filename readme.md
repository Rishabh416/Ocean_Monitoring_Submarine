# Research Project with Rochester Institute of Technology, Dubai
This project works on creating a ocean monitoring submarine. The system is equipped with a Raspberry Pi 4 Model B which is able to capture live video feed through an Arducam 5MP camera. The Raspberry Pi uses the Picamera2 library to interface with the camera. The live video feed is displayed on a webUI which also facilitates a 9-key control system to maneuver the submarine. 

### Hardware
Raspberry Pi 4 Model B
Arducam 5MP OV5647

### Software
- FastAPI: This library is used to provide API access points that can be accessed by the webUI to display a live camera feed and relay information
- Uvicorn: This library is a web server which is being used to host the API endpoints on a local host. 
- Picamera2: This library is used to interface with the camera and capture images.
- OpenCV: This library is for image processing and used to encode/decode the images so that it can be relayed over an API endpoint. 
- Time: This library is used to get access to the current time and provide a unique identifier to each image saved. 