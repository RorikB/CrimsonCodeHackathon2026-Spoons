import re
import elevenLabs
import clock_gui
import timer
import google_calendar_api

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
    "clock": lambda:clock_gui.ClockGUI().get_time_string(),
    # "timer": lambda duration: timer_gui.TimerGUI().run(int(duration)) if duration else print("Timer command requires a duration argument"),
    "timer": lambda duration: timer.get_status_string() if duration is None else timer.start(int(duration)),
    "calendar": lambda: google_calendar_api.GoogleCalendarAPI().run(),
}

def check_for_command(input_string):
    global FUNCTION_MAP
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

call(">clock()")
# call(">timer(10)")
call(">calendar()")
