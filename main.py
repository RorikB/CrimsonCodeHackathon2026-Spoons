from modules.gui.display import fullscreen_mirror

def main():
    state = {
        "Weather": "72°F Sunny",
        "Calendar": "Meeting at 2pm",
        "Timer": "5:00",
        "Music": "No song playing"
    }
    fullscreen_mirror(state)

if __name__ == "__main__":
    main()