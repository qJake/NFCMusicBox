import os
import state
import pygame

class MediaPlayer:

    STATE_INIT = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    STATE_STOPPED = 3

    state = STATE_INIT
    ding = None

    def __init__(self):
        pygame.mixer.init(48000,-16,2,1024)
        self.channel1 = pygame.mixer.Channel(1)
        self.channel2 = pygame.mixer.Channel(2)
        self.state = self.STATE_STOPPED
        self.ding = pygame.mixer.Sound(file='sound/ding.wav')
        self.loadedSong = None

    def set_vol(self, vol=1.0):
        self.channel1.set_volume(min(1, max(0, vol)))
        self.channel2.set_volume(min(1, max(0, vol)))
        state.set_vol(vol)

    def play_ding(self):
        vol = state.get_vol()
        if self.ding is not None:
            self.ding.set_volume(vol)
            self.channel2.play(self.ding)

    def load(self, name):
        _, tail = os.path.split(name)
        state.set_song_name(tail)

        # There's an audio blip... so stop first if we're playing.
        if self.state == self.STATE_PLAYING:
            self.channel1.stop()

        self.loadedSong = pygame.mixer.Sound(name)
        self.channel1.set_volume(state.get_vol())
        self.state = self.STATE_STOPPED
    
    def play(self):
        if self.loadedSong is None:
            return

        try:
            if self.state == self.STATE_PAUSED:
                self.channel1.unpause()
            else:
                self.channel1.play(self.loadedSong)
            self.state = self.STATE_PLAYING
        # pylint: disable=no-member
        except pygame.error as e:
            if 'music not loaded' in e.args[0]:
                pass

    def stop(self):
        self.channel1.stop()
        self.state = self.STATE_STOPPED

    def pause(self):
        self.channel1.pause()
        self.state = self.STATE_PAUSED

    def is_state(self, state_check):
        return self.state == state_check
