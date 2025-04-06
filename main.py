import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import threading
import time
from picamera2 import Picamera2
import serial

# Initialize camera
cam = Picamera2()
config = cam.create_preview_configuration(main={"size": (640, 480)})
cam.configure(config)
cam.start()

ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)
ser.write(b'Serial Connection Established\n')

# GUI Application
class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Submarine Control Panel")
        self.is_recording = False
        self.video_writer = None

        # Video feed display
        self.label = tk.Label(root)
        self.label.pack()

        # Scrollbars (you can bind these to commands)
        self.scroll_x = tk.Scale(root, from_=1000, to=2000, orient="horizontal", label="X Axis", resolution=1)
        self.scroll_x.set(1500)
        self.scroll_x.pack(fill="x")
        self.scroll_x.bind("<ButtonRelease-1>", lambda e: self.on_slider_release(self.scroll_x, 'm1'))

        self.scroll_y = tk.Scale(root, from_=1000, to=2000, orient="horizontal", label="Y Axis", resolution=1)
        self.scroll_y.set(1500)
        self.scroll_y.pack(fill="x")
        self.scroll_y.bind("<ButtonRelease-1>", lambda e: self.on_slider_release(self.scroll_y, 'm2'))

        self.scroll_z = tk.Scale(root, from_=1000, to=2000, orient="horizontal", label="Z Axis", resolution=1)
        self.scroll_z.set(1500)
        self.scroll_z.pack(fill="x")
        self.scroll_z.bind("<ButtonRelease-1>", lambda e: self.on_slider_release(self.scroll_z, 'm3'))

        # Control buttons
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack()

        self.record_btn = ttk.Button(self.btn_frame, text="Start Recording", command=self.toggle_recording)
        self.record_btn.grid(row=0, column=0, padx=5)

        self.photo_btn = ttk.Button(self.btn_frame, text="Take Photo", command=self.take_photo)
        self.photo_btn.grid(row=0, column=1, padx=5)

        self.update_frame()

    def on_slider_release(self, slider, prefix):
        value = slider.get()
        if abs(value - 1500) < 50:  # threshold for snapping
            slider.set(1500)
        value = slider.get()
        print(f"Slider released: {prefix}{value}")
        ser.write(f"{prefix}{value}\n".encode()) 


    def update_frame(self):
        frame = cam.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if self.is_recording and self.video_writer:
            self.video_writer.write(frame)

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        filename = f"recording_{int(time.time())}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
        self.is_recording = True
        self.record_btn.config(text="Stop Recording")
        print("Recording started...")

    def stop_recording(self):
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        self.is_recording = False
        self.record_btn.config(text="Start Recording")
        print("Recording stopped.")

    def take_photo(self):
        filename = f"photo_{int(time.time())}.jpg"
        cam.capture_file(filename)
        print(f"Photo saved as {filename}")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
