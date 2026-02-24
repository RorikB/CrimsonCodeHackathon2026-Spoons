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
