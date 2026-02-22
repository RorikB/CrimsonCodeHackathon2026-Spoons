import re
import elevenLabs
import clock_gui
import lamma
import timer
# import google_calendar_api
import spotify_player

def hello(name):
    print(f"Hello, {name}!")
    return f"greeted {name}"

def add(a, b):
    result = int(a) + int(b)
    print(f"{a} + {b} = {result}")
    elevenLabs.prompt_elevenlabs(f"The result of adding {a} and {b} is {result}")
    return result

FUNCTION_MAP = {
    "hello": hello,
    "add": add,
    "clock": lambda: elevenLabs.prompt_elevenlabs(f"The time is {clock_gui.ClockGUI().get_time_string()}"),
    "timer": lambda duration=None: elevenLabs.prompt_elevenlabs(timer.get_status_string() if duration is None else timer.start(int(duration))),
    # "calendar": lambda: elevenLabs.prompt_elevenlabs(google_calendar_api.GoogleCalendarAPI().run()),
    # "calendar": lambda: elevenLabs.prompt_elevenlabs(llama.chat("What is on my calendar today?")),
    "pause": lambda: spotify_player.SpotifyPlayer().play_pause(),
    "play": lambda: spotify_player.SpotifyPlayer().play_pause(),



    # spotify_player.SpotifyPlayer.play_pause() = lamma.chat("play")
}

# output = lamma.chat(latest_text)
#     if not stringParser.check_for_command(output):
#         elevenLabs.prompt_elevenlabs(output)

# elevenLabs.prompt_elevenlabs(gemini.prompt_gemini(latest_text))

def check_for_command(input_string):
    global FUNCTION_MAP
    if input_string is None:
        return False 
    # detect if the string contains a function call in the format >functionName(arg1, arg2)
    pattern = r'>(\w+)\(([^)]*)\)'
    match = re.search(pattern, input_string)
    if match:
        function_name = match.group(1)
        raw_args = match.group(2)

        # Parse args: split by comma, strip whitespace, filter empty
        args = [arg.strip() for arg in raw_args.split(',')] if raw_args.strip() else []

        if function_name in FUNCTION_MAP:
            return FUNCTION_MAP[function_name](*args)
        else:
            print(f"Unknown command: {function_name}")
            return None
    return False



def call(input):
    check_for_command(input)

# call(">clock()")
# call(">timer(10)")
# call(">calendar()")
# call(">play()")