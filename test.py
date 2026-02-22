import threading
import vision
import whisper
import time

face_detected = False

def run_vision():
    while True:
        result = vision.check_for_face()
        global face_detected


def run_whisper():
    while True:
        whisper.speech_to_text()


if __name__ == "__main__":
    vision_thread = threading.Thread(target=run_vision, daemon=True)
    whisper_thread = threading.Thread(target=run_whisper, daemon=True)

    vision_thread.start()
    whisper_thread.start()


    while True:
        print("Face Detected:", face_detected)
        time.sleep(1)