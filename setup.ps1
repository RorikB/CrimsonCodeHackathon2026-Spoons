$projectRoot = "c:\Users\rorik\1Keepers\GitHub\CrimsonCodeHackathon2026-Spoons"
Set-Location $projectRoot

Write-Host "=== Desktop Assistant Setup ===" -ForegroundColor Cyan

$folders = @("core", "ui", "utils", "config", "src")
foreach ($folder in $folders) {
    $path = Join-Path $projectRoot $folder
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "Created: $folder"
    }
}

$geminiContent = @'
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def prompt_gemini(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return "Error: " + str(e)
'@
Set-Content -Path "$projectRoot\core\gemini.py" -Value $geminiContent
Write-Host "Created: core/gemini.py"

$mainContent = @'
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from core.gemini import prompt_gemini
from utils.stringParser import check_for_command

class DesktopAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Desktop Assistant")
        self.geometry("900x600")
        self.configure(bg="#1E1E1E")
        self.build_ui()
        
    def build_ui(self):
        header = tk.Frame(self, bg="#2D2D30")
        header.pack(fill="x", padx=10, pady=10)
        tk.Label(header, text="Desktop Assistant", font=("Helvetica", 20, "bold"), fg="white", bg="#2D2D30").pack(anchor="w", padx=10)
        
        content = tk.Frame(self, bg="#1E1E1E")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(content, text="Response:", font=("Helvetica", 12, "bold"), fg="#AAAAAA", bg="#1E1E1E").pack(anchor="w", pady=(0,5))
        
        self.output = scrolledtext.ScrolledText(content, height=12, bg="#252526", fg="#CCCCCC", font=("Consolas", 10), state="disabled")
        self.output.pack(fill="both", expand=True, pady=(0,15))
        
        tk.Label(content, text="Input:", font=("Helvetica", 12, "bold"), fg="#AAAAAA", bg="#1E1E1E").pack(anchor="w", pady=(0,5))
        
        self.input_text = tk.Text(content, height=3, bg="#252526", fg="#CCCCCC", font=("Consolas", 10))
        self.input_text.pack(fill="x")
        self.input_text.bind("<Control-Return>", lambda e: self.send())
        
        btn_frame = tk.Frame(content, bg="#1E1E1E")
        btn_frame.pack(fill="x", pady=(10,0))
        tk.Button(btn_frame, text="Send", command=self.send, bg="#0E639C", fg="white").pack(side="left", padx=(0,5))
        tk.Button(btn_frame, text="Clear", command=self.clear, bg="#6A6A6A", fg="white").pack(side="left")
    
    def send(self):
        msg = self.input_text.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Error", "Enter a message")
            return
        self.append("[You]: " + msg + "\n")
        self.input_text.delete("1.0", tk.END)
        threading.Thread(target=self.process, args=(msg,), daemon=True).start()
    
    def process(self, msg):
        try:
            result = check_for_command(msg)
            if result:
                self.append("[Command]: " + str(result) + "\n")
            else:
                response = prompt_gemini(msg)
                self.append("[Assistant]: " + response + "\n")
        except Exception as e:
            self.append("[Error]: " + str(e) + "\n")
    
    def append(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state="disabled")
    
    def clear(self):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")

if __name__ == "__main__":
    app = DesktopAssistant()
    app.mainloop()
'@
Set-Content -Path "$projectRoot\main.py" -Value $mainContent
Write-Host "Created: main.py"

$reqs = @'
google-generativeai>=0.3.0
spotipy>=2.22.0
requests>=2.31.0
python-dotenv>=1.0.0
icalendar>=5.0.0
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.100.0
'@
Set-Content -Path "$projectRoot\requirements.txt" -Value $reqs
Write-Host "Created: requirements.txt"

$env = @'
GEMINI_API_KEY=your_key_here
SPOTIFY_CLIENT_ID=your_id
SPOTIFY_CLIENT_SECRET=your_secret
'@
Set-Content -Path "$projectRoot\config\.env" -Value $env
Write-Host "Created: config/.env"

$parser = @'
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
'@
Set-Content -Path "$projectRoot\utils\stringParser.py" -Value $parser
Write-Host "Created: stringParser.py"

$venv_path = Join-Path $projectRoot "venv"
if (Test-Path $venv_path) {
    Remove-Item -Path $venv_path -Recurse -Force
    Write-Host "Removed: venv"
}

$voice_path = Join-Path $projectRoot "voice"
if (Test-Path $voice_path) {
    Remove-Item -Path $voice_path -Recurse -Force
    Write-Host "Removed: voice"
}

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. python -m venv venv"
Write-Host "2. venv\Scripts\activate"
Write-Host "3. pip install -r requirements.txt"
Write-Host "4. python main.py"