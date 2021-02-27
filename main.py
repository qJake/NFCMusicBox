import os
import utils
import state
import platform
import subprocess
import nfc_reader
import web_interface
from media_player import MediaPlayer
from storage import TagStorage
from time import sleep

DEVENV = False
try:
    # pylint: disable=import-error
    import RPi.GPIO as GPIO
except:
    DEVENV = True

STORE_WIN = '%localappdata%\\NFCMusicBox\\'
STORE_LINUX = '/var/lib/nfcmusicbox/'

UPDATE_COMMAND = "/bin/bash -c 'cd /home/pi/nfc-music-box && sudo ./update.sh' &"

# Special UID to "stop"
STOP_NFC_UID = '1732584193'

def start():
    state.init()

    storage = TagStorage(get_store_path())
    state.set_storage(storage)

    def nfcLoaded():
        nfc_reader.onTagRead += on_tag_read
    nfc_reader.onLoad += nfcLoaded
    nfc_reader.start_nfc_thread()

    web_interface.init()

    player = MediaPlayer()
    state.set_player(player)

    # TODO: Startup Sound
    #player.play_ding()

    # Blocks, keep last.
    web_interface.run_wait()
        
def on_tag_read(tag):
    print_nfc_tag(tag)
    store_last_tag(tag)
    play_requested_song(tag)

def print_nfc_tag(tag):
    print('[NFC] Read new card with UID: %s' % tag)

def store_last_tag(tag):
    state.set_last_tag(tag)

def play_requested_song(tag):

    if tag == STOP_NFC_UID:
        player = state.get_player()
        player.play_ding()
        player.stop()

    else:
        storage = state.get_storage()
        tags = storage.get_tags()
        
        if len(tags) == 0:
            return
        
        tagDef = utils.select_tag(storage.get_tags(), tag)

        if tagDef is not None:
            player = state.get_player()
            player.play_ding()
            sleep(0.5)
            player.load(tag=tag)
            player.play()

def get_store_path():
    if platform.system() == 'Windows':
        return os.path.expandvars(STORE_WIN)
    else:
        return STORE_LINUX

def update():
    if platform.system() == 'Windows':
        return # Don't self-upate on Windows, this is only for Pis.
    
    os.system(UPDATE_COMMAND)

if __name__ == '__main__':
    start()