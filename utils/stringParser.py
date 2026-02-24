import re
from features.timer.timer import Timer
import features.spotify.spotify_player as spotify_player

def hello(name):
    return "Hello, " + name + "!"

def add(a, b):
    return "Result: " + str(int(a) + int(b))

timer = Timer()
FUNCTION_MAP = {
    "hello": hello,
    "add": add,
    "timer": lambda *args: timer.start(*args),
    "pause": lambda: spotify_player.SpotifyPlayer().play_pause(),
    "play": lambda: spotify_player.SpotifyPlayer().play_pause(),
}

def check_for_command(input_string):
    if not input_string:
        return False
    pattern = r'>(\w+)\(([^)]*)\)'
    match = re.search(pattern, input_string)
    if match:
        func_name = match.group(1)
        raw_args = match.group(2)
        args = [arg.strip() for arg in raw_args.split(',')] if raw_args.strip() else []
        return FUNCTION_MAP.get(func_name, lambda: "Unknown: " + func_name)(*args)
    return False
