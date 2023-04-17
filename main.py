import spotipy
import keyboard
import dotenv
import tkinter as tk
from tkinter import ttk
import random

class Spotify:
    delta = 5
    volume_down_hotkey = 'f21'
    volume_up_hotkey = 'f22'

    def __init__(self):
        scope = "user-modify-playback-state,user-read-playback-state"
        self._sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(scope=scope))
        keyboard.add_hotkey(self.volume_down_hotkey, self.down)
        keyboard.add_hotkey(self.volume_up_hotkey, self.up)
        self._window = tk.Tk()
        self._window.overrideredirect(True)
        self._window.configure(bg='black')
        self._window.geometry('70x200')
        self._window.title('Spotify volume control')
        # Make the window topmost
        self._window.attributes('-topmost', True)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", troughcolor='white', background='blue', darkcolor='white', lightcolor='white', bordercolor='white', thickness=100)
        self._progress_bar = ttk.Progressbar(self._window, orient=tk.VERTICAL, length=500, mode='determinate', style="red.Horizontal.TProgressbar")
        self._progress_bar.pack(pady=30)

    def timer(self, id):
        if id != self._last_timer_id:
            return
        self._window.withdraw()

    def get_volume(self):
        pb = self._sp.current_playback()
        if pb is None:
            return 0
        return pb['device']['volume_percent']

    def set_volume(self, value):
        self._window.deiconify()
        self._last_timer_id = random.randint(0, 1337)
        self._window.after(5000, self.timer, self._last_timer_id)
        pb = self._sp.current_playback()
        if pb is None:
            return
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        self._sp.volume(value)
        vol = self.get_volume()
        self._progress_bar['value'] = vol
        print(vol)

    def up(self):
        self.set_volume(self.get_volume() + self.delta)

    def down(self):
        self.set_volume(self.get_volume() - self.delta)

    def basically_run(self):
        self._window.mainloop()
        #keyboard.wait()


if __name__ == '__main__':
    dotenv.load_dotenv()
    s = Spotify()
    s.basically_run()
