import os
import utils
import state
import platform
import nfc_player
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

def start():
    state.init()

    storage = TagStorage(get_store_path())
    state.set_storage(storage)

    def nfcLoaded():
        nfc_player.onTagRead += print_nfc_tag
        nfc_player.onTagRead += store_last_tag
        nfc_player.onTagRead += play_requested_song
    nfc_player.onLoad += nfcLoaded
    nfc_player.start_nfc_thread()

    web_interface.init()

    player = MediaPlayer()
    state.set_player(player)

    # TODO: Startup Sound
    #player.play_ding()

    # Blocks, keep last.
    web_interface.run_wait()
        
def print_nfc_tag(tag):
    print('[NFC] Read new card with UID: ', tag)

def store_last_tag(tag):
    state.set_last_tag(tag)

def play_requested_song(tag):
    storage = state.get_storage()
    tags = storage.get_tags()
    
    if len(tags) == 0:
        return
    
    tagDef = utils.select_tag(storage.get_tags(), tag)

    if tagDef is not None:
        player = state.get_player()
        player.play_ding()
        sleep(1)
        player.load(storage.to_full_path(tag['name']))
        player.play()

def get_store_path():
    if platform.system() == 'Windows':
        return os.path.expandvars(STORE_WIN)
    else:
        return STORE_LINUX

if __name__ == '__main__':
    start()