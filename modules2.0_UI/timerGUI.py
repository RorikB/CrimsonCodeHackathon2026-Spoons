import tkinter as tk
from timer import Timer

timer = Timer()

def formatTimer(seconds):
    hours = seconds // 3600
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def updateTimer():
    if timer.is_active():
        remaining_time = timer.get_remaining_time() 
        timer_label.config(text=formatTimer(remaining_time)) 
        root.after(1000, updateTimer)
    else:
        timer_label.config(text="00:00:00")
        
def startTimer():
    duration = int(entry.get())
    timer.start(duration)
    updateTimer() 
    ValueError (timer.start(duration))
    
def stopTimer():
    timer.stop()
    timer_label.config(text="00:00:00")
    
def reset_timer():
     timer.stop()
     timer_label.config(text="00:00:00")
     entry_seconds.delete(0, tk.END)
     
    
    
    