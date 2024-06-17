from fastapi import FastAPI  
from fastapi.responses import StreamingResponse  
import uvicorn 
from picamera2 import Picamera2, Preview  
import io  
import cv2 
import time

app = FastAPI()

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)  
picam2.start()  

def generate_frames():
    while True:  
        frame = picam2.capture_array()  
        ret, buffer = cv2.imencode('.jpg', frame)  
        frame = buffer.tobytes()  
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/videoFeed")
async def videoFeed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/takeImage")
async def takeImage():
    picam2.capture_file(f"{time.time()}.jpg")
    print("Taken image")
    return("captured")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
