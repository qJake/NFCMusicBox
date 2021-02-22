import os
import state
import pygame

class MediaPlayer:

    STATE_INIT = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    STATE_STOPPED = 3

    state = STATE_INIT

    def __init__(self):
        pygame.mixer.init()
        self.state = self.STATE_STOPPED

    def set_vol(self, vol=1.0):
        pygame.mixer.music.set_volume(min(1, max(0, vol)))
        state.set_vol(vol)

    def load(self, name):
        _, tail = os.path.split(name)
        state.set_song_name(tail)
        pygame.mixer.music.load(name)
        pygame.mixer.music.set_volume(state.get_vol())
        self.state = self.STATE_STOPPED
    
    def play(self):
        try:
            if self.state == self.STATE_PAUSED:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
            self.state = self.STATE_PLAYING
        # pylint: disable=no-member
        except pygame.error as e:
            if 'music not loaded' in e.args[0]:
                pass

    def stop(self):
        pygame.mixer.music.stop()
        self.state = self.STATE_STOPPED

    def pause(self):
        pygame.mixer.music.pause()
        self.state = self.STATE_PAUSED

    def is_state(self, state_check):
        return self.state == state_check
