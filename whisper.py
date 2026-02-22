from RealtimeSTT import AudioToTextRecorder
import elevenLabs
import gemini
import time
import lamma
import stringParser
import pygame
latest_text = ""
recorder = None 

def get_recorder():
    global recorder
    if recorder is None:
        recorder = AudioToTextRecorder(
            wake_words="computer",
            wakeword_backend="pvporcupine",
            on_wakeword_detected=on_wakeword_detected,
            wake_words_sensitivity=0.7,
            model="medium.en",
            device="cuda",
            silero_sensitivity=0.7,
            # enable_realtime_transcription=True
        )
    return recorder
def process_text(text):
    global latest_text
    latest_text = text
    print(text)

def on_wakeword_detected():
    print("Wake word detected!")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('universfield-notification-beep-229154.mp3')
    pygame.mixer.music.play()

def speech_to_text():
    get_recorder().text(process_text)
    # recorder.text(process_text)
    # start = time.process_time()
    # elevenLabs.prompt_elevenlabs(gemini.prompt_gemini(latest_text))
    output = lamma.chat(latest_text)
    if not stringParser.check_for_command(output):
        elevenLabs.prompt_elevenlabs(output)


    # print("\nTime Taken: "+ str(time.process_time() - start))
def talk(input_text):
    
    output = lamma.chat(input_text)
    if not stringParser.check_for_command(output):
        elevenLabs.prompt_elevenlabs(output)


if __name__ == '__main__': # needed for multiprecessing
# recorder = AudioToTextRecorder(model="medium.en", silero_sensitivity=1.0, device="cuda")
    # recorder = AudioToTextRecorder(
    #     # wake_words="blueberry",
    #     # wakeword_backend="pvporcupine",
    #     # on_wakeword_detected=on_wakeword_detected,
    #     # wake_words_sensitivity = 0.7,
    #     model="medium.en",
    #     device="cuda",
    #     silero_sensitivity = 0.7,
    #     # enable_realtime_transcription=True
    # )
    while True:
        # infil = input("input: ")
        # elevenLabs.prompt_elevenlabs(gemini.prompt_gemini(infil))
        speech_to_text()

        # recorder.text(process_text)
        # start = time.process_time()
        # elevenLabs.prompt_elevenlabs(gemini.prompt_gemini(latest_text))
        # print("\nTime Taken: "+ str(time.process_time() - start))
        
