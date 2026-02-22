from modules.gui.display import fullscreen_mirror
from timer import Timer

def main():
    timer = Timer()

    state = {
        "Weather": "72°F Sunny",
        "Calendar": "Meeting at 2pm",
        "Music": "No song playing",
        "Timer": "0:00"
    }

    def update_state():
        if timer.is_active():
            remaining = timer.get_remaining_time()
            minutes = remaining // 60
            seconds = remaining % 60
            state["Timer"] = f"{minutes:02d}:{seconds:02d}"
        else:
            state["Timer"] = "0:00"

    timer.start(120)

    fullscreen_mirror(state, per_frame_callback=update_state)

if __name__ == "__main__":
    main()