import os
import platform
import nfc_player
import web_interface
from media_player import MediaPlayer
from storage import TagStorage
import state

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

    nfc_player.start_nfc_thread()

    web_interface.init()

    player = MediaPlayer()
    state.set_player(player)

    # Blocks, keep last.
    web_interface.run_wait()
        
def get_store_path():
    if platform.system() == 'Windows':
        return os.path.expandvars(STORE_WIN)
    else:
        return STORE_LINUX

if __name__ == '__main__':
    start()