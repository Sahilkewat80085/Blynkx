import cv2
import time
import os
import RPi.GPIO as GPIO
import threading
import statistics
from collections import Counter
from picamera2 import Picamera2

# ------------------ SPEECH ------------------
last_speech_time = 0
speech_interval = 4
last_spoken = ""

def speak(text):
    global last_speech_time, last_spoken

    if (time.time() - last_speech_time > speech_interval) or (text != last_spoken):
        print("[SPEAK]", text)
        os.system(f'espeak "{text}"')
        last_speech_time = time.time()
        last_spoken = text

# ------------------ GPIO ------------------
TRIG = 23
ECHO = 24

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

distance = None

# ------------------ ULTRASONIC THREAD ------------------
def ultrasonic_worker():
    global distance

    while True:
        try:
            GPIO.output(TRIG, False)
            time.sleep(0.002)

            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            start = time.time()
            timeout = start + 0.04

            while GPIO.input(ECHO) == 0:
                start = time.time()
                if start > timeout:
                    break

            while GPIO.input(ECHO) == 1:
                end = time.time()
                if end > timeout:
                    break

            duration = end - start
            dist = duration * 17150

            if 2 < dist < 400:
                distance = round(dist, 2)

            time.sleep(0.05)

        except:
            distance = None

# Start ultrasonic thread
threading.Thread(target=ultrasonic_worker, daemon=True).start()

# ------------------ LOAD MOBILENET ------------------
net = cv2.dnn.readNetFromCaffe(
    "MobileNetSSD_deploy.prototxt",
    "MobileNetSSD_deploy.caffemodel"
)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor"]

# ------------------ CSI CAMERA ------------------
picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (320, 240), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()

# ------------------ MAIN LOOP ------------------
frame_count = 0
SKIP_FRAMES = 6

try:
    while True:
        frame = picam2.capture_array()
        
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        
        frame_count += 1
        detected_objects = []

        # -------- DETECTION --------
        if frame_count % SKIP_FRAMES == 0:

            blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()

            h, w = frame.shape[:2]
            person_detected = False

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence < 0.5:
                    continue

                idx = int(detections[0, 0, i, 1])

                if idx >= len(CLASSES):
                    continue

                label = CLASSES[idx]

                # PRIORITY: PERSON
                if label == "person":
                    person_detected = True

                if label not in ["person", "chair", "diningtable", "tvmonitor"]:
                    continue

                # Rename for clarity
                if label == "diningtable":
                    label = "table"
                if label == "tvmonitor":
                    label = "computer"

                detected_objects.append(label)

                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                x1, y1, x2, y2 = box.astype("int")

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

            # Person priority override
            if person_detected:
                detected_objects = ["person"]

        # -------- SPEECH --------
        if detected_objects:
            counts = Counter(detected_objects)
            sentence = ", ".join([f"{v} {k}" for k, v in counts.items()])

            if distance:
                speak(f"{sentence} at {int(distance)} centimeters")
            else:
                speak(sentence)

        # -------- DISPLAY --------
        if distance:
            cv2.putText(frame, f"{distance:.1f} cm", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

        cv2.imshow("BlinkX CSI Final", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Stopped")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    GPIO.cleanup()
