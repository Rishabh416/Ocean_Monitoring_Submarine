from fastapi import FastAPI, Response
from picamera2 import Picamera2
import cv2

app = FastAPI()

# Initialize the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

@app.get("/video_feed")
async def video_feed():
    # Capture a single frame as a numpy array
    frame = picam2.capture_array()
    # Encode the frame as JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    # Create a response with the JPEG image
    return Response(content=buffer.tobytes(), media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn  # Import uvicorn for running the FastAPI app
    # Run the app on all available IP addresses (0.0.0.0) at port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
