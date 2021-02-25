import os
import gc
import state
import pygame
from time import sleep

class MediaPlayer:

    STATE_INIT = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    STATE_STOPPED = 3

    state = STATE_INIT
    ding = None

    songCache = []

    def __init__(self):
        pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=1024, allowedchanges=0)
        self.channel1 = pygame.mixer.Channel(1)
        self.channel2 = pygame.mixer.Channel(2)
        self.state = self.STATE_STOPPED
        self.s_ding = pygame.mixer.Sound(file='sound/ding.wav')
        self.s_loading = pygame.mixer.Sound(file='sound/loading.wav')
        self.s_ready = pygame.mixer.Sound(file='sound/ready.wav')
        self.activeSong = None
        self.channel1.play(self.s_loading)
        sleep(2)
        self.reload_songs()
        sleep(0.3)
        self.channel1.play(self.s_ready)

    def reload_songs(self):
        print('[Media] Reloading songs...')

        if self.state == self.STATE_PLAYING:
            print('[Media] Stopping playback for song reload...')
            self.stop()

        storage = state.get_storage()
        tags = storage.get_tags()

        self.songCache = []
        gc.collect() # clean up the old songs first - this can affect audio playback

        if len(tags) > 0:
            for t in tags:
                path = storage.to_full_path(t['name'])
                self.songCache.append({
                    'tag': t['uid'],
                    'songFile': path,
                    'song': pygame.mixer.Sound(path)
                })
                print('Loaded song: %s' % path)

    def set_vol(self, vol=1.0):
        self.channel1.set_volume(min(1, max(0, vol)))
        self.channel2.set_volume(min(1, max(0, vol)))
        state.set_vol(vol)

    def play_ding(self):
        vol = state.get_vol()
        if self.s_ding is not None:
            self.s_ding.set_volume(vol)
            self.channel2.play(self.s_ding)

    def load(self, name=None, tag=None):
        if name is None and tag is None:
            raise 'Must pass name or tag to load().'

        if name is not None:
            foundSong = next((s for s in self.songCache if s['songFile'] == name), None)
            if foundSong is not None:
                tag = foundSong['song']
                song = foundSong['song']
        elif tag is not None:
            foundSong = next((s for s in self.songCache if s['tag'] == tag), None)
            if foundSong is not None:
                name = foundSong['songFile']
                song = foundSong['song']

        if song is None:
            return
        
        _, tail = os.path.split(name)
        state.set_song_name(tail)

        # There's an audio blip... so stop first if we're playing.
        if self.state == self.STATE_PLAYING:
            self.channel1.stop()

        self.activeSong = song
        self.channel1.set_volume(state.get_vol())
        self.state = self.STATE_STOPPED
    
    def play(self):
        if self.activeSong is None:
            return

        try:
            if self.state == self.STATE_PAUSED:
                self.channel1.unpause()
            else:
                self.channel1.play(self.activeSong)
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
