Hello, Jr's this is Sahil Kewat one who continued project after my senior Pranav Shanbaug, so Im presenting you: 
🚀 BlinkX – Your Third Eye 👁️‍🗨️

Welcome to BlinkX, a smart assistive system designed to help visually impaired users navigate the world using AI + sensors + audio feedback.

If you're reading this, congrats — you’ve inherited a working but slightly chaotic project. Don’t worry, I’ve got you covered.

🧠 What This Project Does

BlinkX uses:

📷 Camera → detects objects (people, chairs, etc.)
📏 Ultrasonic Sensor → measures distance
🔊 Audio (espeak) → tells the user what’s ahead

Example output:
“1 person at 60 centimeters”

TO START THE PROJECT:
cd Blynkx
python csi_mobilenet.py

⚙️ Tech Stack
Python 🐍
OpenCV (DNN)
MobileNet-SSD
Raspberry Pi
Picamera2
HC-SR04 Ultrasonic Sensor
espeak (text-to-speech)
🔧 Hardware Setup
Raspberry Pi (3/4 recommended)
CSI Camera Module
Ultrasonic Sensor (HC-SR04)
Earphones / Speaker
Breadboard + jumper wires
🔌 GPIO Connections
Component	Pin
TRIG	23
ECHO	24
🧪 How It Works (Simple Flow)
Camera → Object Detection → Filter → Distance → Audio Output
Camera captures frame
MobileNet detects objects
Only useful objects are kept
Ultrasonic gives distance
System speaks result
🏃‍♂️ How to Run
python3 rpicam.py
⚡ Auto Start on Boot

If service is enabled:

sudo systemctl start blinkx.service

Check status:

sudo systemctl status blinkx.service
🧠 Important Logic (Read This!)
🔥 Person Priority

If a person is detected:

detected_objects = ["person"]

👉 Because humans > everything

🔥 Frame Skipping
SKIP_FRAMES = 6

👉 Improves performance on Pi

🔥 Ultrasonic Thread

Runs separately → avoids lag

⚠️ Known Issues (a.k.a. Things That Might Break at 2 AM)
Camera upside down → use:
cv2.rotate(frame, cv2.ROTATE_180)
Blue tint → fix color format (BGR888)
Service not showing window → remove cv2.imshow()
👉 systemd = headless
🚀 Future Improvements (YOUR JOB 😄)
🔥 Left / Right direction detection
🔥 Better voice (Hindi / natural TTS)
🔥 Smaller hardware (ID-card design)
🔥 Mobile app integration
🔥 GPS navigation (Google Maps API)
🧠 Pro Tips
Don’t use YOLO on Pi unless you enjoy suffering
Always test with:
journalctl -u blinkx.service -f
If something crashes → it’s probably:
path issue
display issue
model missing
🎯 Goal of Project

Not just a project —
👉 A real assistive device for real people

👀 Final Advice
Keep it simple
Keep it stable
Don’t overcomplicate
💬 If You're Stuck

Ask yourself:

“Did I break something that was already working?”

👉 Answer is usually yes.

🏁 You're Now the Owner

Good luck.
