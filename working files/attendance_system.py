import tkinter as tk
from tkinter import messagebox
import pyaudio
import wave
import threading
import time
import os
import shutil

class AttendanceSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Attendance System")

        self.label = tk.Label(master, text="Enter your name:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.record_button = tk.Button(master, text="Record Voice", command=self.record_voice)
        self.record_button.pack()

    def record_voice(self):
        voice_recorder = VoiceRecorder()

        name = self.entry.get()
        if name:
            messagebox.showinfo("Attendance Marked", f"Attendance marked for {name}")
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter your name.")

class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button = tk.Button(self.root, text="rec🔴rd", font=("Arial", 120, "bold"), command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(self.root, text="00:00:00")
        self.label.pack()
        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        frames = []

        start = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1
        while exists:
            if os.path.exists(f"data/Recordings/recording{i}.wav"):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f"recording{i}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(16000)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()

        shutil.move(f"recording{i}.wav", f"data/Recordings/recording{i}.wav")

def main():
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
