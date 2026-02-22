from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play, save
import os

load_dotenv()

# Load environment variables
ffmpeg_path = os.getenv("FFMPEG_PATH")
ffprobe_path = os.getenv("FFPROBE_PATH")

# Add ffmpeg to system PATH
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def prompt_elevenlabs(input_text):
    audio = elevenlabs.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    play(audio)

