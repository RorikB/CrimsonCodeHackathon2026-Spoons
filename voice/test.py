import threading
import lamma as lamma
import voice.vision as vision
import voice.whisper as whisper
import time


face_detected = False

def run_vision():
    while True:
        result = vision.check_for_face()
        global face_detected
        face_detected = result

def run_whisper():
    while True:
        whisper.speech_to_text()


if __name__ == "__main__":
    # lamma.chat("Hello, how are you?")

    # vision_thread = threading.Thread(target=run_vision, daemon=True)
    whisper_thread = threading.Thread(target=run_whisper, daemon=True)

    # vision_thread.start()
    whisper_thread.start()


    while True:
        # print("Face Detected:", face_detected)
        time.sleep(1)