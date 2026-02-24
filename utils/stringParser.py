import re
import threading
from features.timer.timer import Timer
import features.spotify.spotify_player as spotify_player
from ui.clock.clock_gui import ClockGUI

def hello(name):
    return "Hello, " + name + "!"

def add(a, b):
    return "Result: " + str(int(a) + int(b))

timer = Timer()

def start_clock():
    def run_clock():
        ClockGUI().run()

    threading.Thread(target=run_clock, daemon=True).start()
    return "Clock opened"

SIMPLE_COMMANDS = {
    "clock": start_clock,
}

FUNCTION_MAP = {
    "hello": hello,
    "add": add,
    "timer": lambda *args: timer.start(*args),
    "pause": lambda: spotify_player.SpotifyPlayer().play_pause(),
    "play": lambda: spotify_player.SpotifyPlayer().play_pause(),
    "clock": start_clock,
}

def check_for_command(input_string):
    if not input_string:
        return False
    cleaned = input_string.strip().lower()
    if cleaned in SIMPLE_COMMANDS:
        return SIMPLE_COMMANDS[cleaned]()
    pattern = r'>(\w+)\(([^)]*)\)'
    match = re.search(pattern, input_string)
    if match:
        func_name = match.group(1)
        raw_args = match.group(2)
        args = [arg.strip() for arg in raw_args.split(',')] if raw_args.strip() else []
        return FUNCTION_MAP.get(func_name, lambda: "Unknown: " + func_name)(*args)
    return False
