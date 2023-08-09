import tkinter as tk
from tkinter import messagebox
import time
import threading
import pygame
from PIL import Image, ImageTk

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("600x400")

        self.alarm_time = None
        self.remaining_time = tk.StringVar()
        self.is_alarm_set = False
        self.is_music_playing = False

        self.init_ui()

    def init_ui(self):
        self.label = tk.Label(self.root, text="Alarm Clock Created by Sumit Gupta", font=("Arial", 24))
        self.label.pack(pady=20)

        self.set_alarm_button = tk.Button(self.root, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_button.pack()

        self.stop_alarm_button = tk.Button(self.root, text="Stop Alarm", command=self.stop_alarm, state=tk.DISABLED)
        self.stop_alarm_button.pack()

        self.user_input_label = tk.Label(self.root, text="Enter alarm time (HH:MM):")
        self.user_input_label.pack()

        self.user_input = tk.Entry(self.root)
        self.user_input.pack()

        image = Image.open("alarm.jpg")
        self.image = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(self.root, image=self.image)
        self.image_label.pack()

        self.remaining_time_label = tk.Label(self.root, textvariable=self.remaining_time, font=("Arial", 16))
        self.remaining_time_label.pack(pady=20)
    def update_remaining_time(self):

        while self.is_alarm_set:

            current_time = time.strftime("%H:%M")
            if current_time >= self.alarm_time:

                self.is_alarm_set = False
                self.remaining_time.set("Alarm!")
            else:

                alarm_time_struct = time.strptime(self.alarm_time, "%H:%M")
                current_time_struct = time.strptime(current_time, "%H:%M")
                remaining_seconds = (alarm_time_struct.tm_hour - current_time_struct.tm_hour) * 3600 + \
                                (alarm_time_struct.tm_min - current_time_struct.tm_min) * 60
            if remaining_seconds < 0:

                remaining_seconds += 86400  # Add 24 hours in seconds to handle alarm set for next day
                remaining_minutes = remaining_seconds // 60
                self.remaining_time.set(f"Alarm in {remaining_minutes} minutes")
    time.sleep(1)

    def set_alarm(self):
        if self.is_alarm_set:
            messagebox.showinfo("Alarm", "Alarm is already set.")
            return

        alarm_time = self.user_input.get()
        if not self.validate_time_format(alarm_time):
            messagebox.showerror("Error", "Invalid time format. Use HH:MM")
            return

        self.alarm_time = alarm_time
        self.is_alarm_set = True
        self.update_remaining_time()

        self.set_alarm_button.config(state=tk.DISABLED)
        self.stop_alarm_button.config(state=tk.NORMAL)

        self.start_alarm_thread()

        messagebox.showinfo("Alarm", f"Alarm is set for {alarm_time}")

    def start_alarm_thread(self):
        self.is_music_playing = True
        threading.Thread(target=self.play_music_thread).start()

    def play_music_thread(self):
        pygame.mixer.init()

        music_files = ['Ram Siya Ram In Flute.mp3','tujhe sab hai pata hai na maa.mp3','Papa Kehte Hain Bada Naam Karega.mp3']

        current_track_index = 0

        while self.is_music_playing:
            pygame.mixer.music.load(music_files[current_track_index])
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(1)

            current_track_index = (current_track_index + 1) % len(music_files)
            time.sleep(10)  # Pause between tracks

    def stop_alarm(self):
        self.is_music_playing = False
        pygame.mixer.music.stop()
        self.is_alarm_set = False
        self.remaining_time.set("")
        self.set_alarm_button.config(state=tk.NORMAL)
        self.stop_alarm_button.config(state=tk.DISABLED)

   
    def validate_time_format(self, time_str):
        try:
            time.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
