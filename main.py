import spotipy
import keyboard
import dotenv


class Spotify:
    delta = 5
    volume_down_hotkey = 'f21'
    volume_up_hotkey = 'f22'

    def __init__(self):
        scope = "user-modify-playback-state,user-read-playback-state"
        self._sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(scope=scope))
        keyboard.add_hotkey(self.volume_down_hotkey, self.down)
        keyboard.add_hotkey(self.volume_up_hotkey, self.up)

    def get_volume(self):
        pb = self._sp.current_playback()
        if pb is None:
            return 0
        return pb['device']['volume_percent']

    def set_volume(self, value):
        pb = self._sp.current_playback()
        if pb is None:
            return
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        self._sp.volume(value)
        print(self.get_volume())

    def up(self):
        self.set_volume(self.get_volume() + self.delta)

    def down(self):
        self.set_volume(self.get_volume() - self.delta)

    def basically_run(self):
        keyboard.wait()


if __name__ == '__main__':
    dotenv.load_dotenv()
    s = Spotify()
    s.basically_run()
