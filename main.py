from fastapi import FastAPI  # API endpoint import
from fastapi.responses import StreamingResponse # live streaming import
from fastapi.middleware.cors import CORSMiddleware # Cross-origin resource sharing policy override import
import uvicorn # live server/API host library
from picamera2 import Picamera2  # camera interface library
import cv2 # image processing library
import time # current time details library

# initialize API
app = FastAPI()

# override CORS policy on browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize camera and set its configuration (480p resolution)
cam = Picamera2()
config = cam.create_preview_configuration(main={"size": (640, 480)})
cam.configure(config)  
cam.start()  

# function to get current frame, encode as jpg and convert it into bytes
def generate_frames():
    while True:  
        frame = cam.capture_array()  
        ret, buffer = cv2.imencode('.jpg', frame)  
        frame = buffer.tobytes()  
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# API endpoint for live video streaming from camera
@app.get("/videoFeed")
async def videoFeed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# API endpoint for capturing current image of camera, name of image is set to current timestamp
@app.get("/takeImage")
async def takeImage():
    cam.capture_file(f"{time.time()}.jpg")
    return("captured")

# following set of functions are for controlling the movement of a submarine
@app.get("/forward")
async def forward():
    print("forward") # replace with movement forward code
    return("forward")    

@app.get("/backward")
async def backward():
    print("backward") # replace with movement backward code
    return("backward")    

@app.get("/right")
async def right():
    print("right") # replace with movement right code
    return("right")    

@app.get("/left")
async def left():
    print("left") # replace with movement left code
    return("left")    

@app.get("/up")
async def up():
    print("up") # replace with movement up code
    return("up")    

@app.get("/down")
async def down():
    print("down") # replace with movement down code
    return("down")    

@app.get("/stop")
async def stop():
    print("stop") # replace with movement stop code
    return("stop")    

# run the API on a localhost server at port 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
