from flask import Flask, render_template, Response, request
from picamera2 import Picamera2
import cv2
import serial
import time
import os

app = Flask(__name__)

# === Initialize camera ===
cam = Picamera2()
config = cam.create_preview_configuration(main={"size": (640, 480)})
cam.configure(config)
cam.start()
frame_size = (640, 480)

# === Initialize serial connection ===
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)
ser.write(b'Serial Connection Established\n')

# === State Variables ===
is_recording = False
video_writer = None

# === Video Feed Generator ===
def gen_frames():
    global is_recording, video_writer
    while True:
        frame = cam.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if is_recording and video_writer:
            video_writer.write(frame)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# === Routes ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    axis = request.form.get('axis')
    value = int(request.form.get('value'))

    if abs(value - 1500) < 50:
        value = 1500

    if axis in ['m1', 'm2', 'm3']:
        command = f"{axis}{value}\n"
        ser.write(command.encode())
        print(f"Sent: {command.strip()}")
    return ('', 204)

@app.route('/photo', methods=['POST'])
def photo():
    filename = f"photo_{int(time.time())}.jpg"
    cam.capture_file(filename)
    print(f"Photo saved as {filename}")
    return ('', 204)

@app.route('/record', methods=['POST'])
def record():
    global is_recording, video_writer
    if not is_recording:
        filename = f"recording_{int(time.time())}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(filename, fourcc, 20.0, frame_size)
        is_recording = True
        print(f"Recording started: {filename}")
    else:
        is_recording = False
        if video_writer:
            video_writer.release()
            video_writer = None
        print("Recording stopped.")
    return ('', 204)

# === Run the Server ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
