from RealtimeSTT import AudioToTextRecorder
import elevenLabs
import gemini
import time

latest_text = ""

def process_text(text):
    global latest_text
    latest_text = text
    print(text)

def on_wakeword_detected():
    print("Wake word detected!")




if __name__ == '__main__': # needed for multiprecessing
# recorder = AudioToTextRecorder(model="medium.en", silero_sensitivity=1.0, device="cuda")
    recorder = AudioToTextRecorder(
        # wake_words="blueberry",
        # wakeword_backend="pvporcupine",
        # on_wakeword_detected=on_wakeword_detected,
        # wake_words_sensitivity = 0.7,
        model="medium.en",
        device="cuda",
        silero_sensitivity = 0.7,
        # enable_realtime_transcription=True
    )
    while True:
        start = time.process_time()
        # infil = input("input: ")
        # elevenLabs.prompt_elevenlabs(gemini.prompt_gemini(infil))

        recorder.text(process_text)
        elevenLabs.prompt_elevenlabs(gemini.prompt_gemini(latest_text))
        print("\nTime Taken: "+ str(time.process_time() - start))
