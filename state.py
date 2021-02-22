import threading

lock = threading.Lock()
state = {}

NFC_STATUS = 'nfcstatus'
MEDIA_PLAYER = 'mediaplayer'
STORAGE = 'storage'
VOL = 'vol'
SONGNAME = 'songname'

def init():
    set(NFC_STATUS, False)
    set(MEDIA_PLAYER, None)
    set(STORAGE, None)
    set(SONGNAME, None)
    set(VOL, 1.0)

def get_nfc_status():
    return get(NFC_STATUS)

def set_nfc_status(val):
    set(NFC_STATUS, val)

def get_song_name():
    return get(SONGNAME)

def set_song_name(val):
    set(SONGNAME, val)

def get_player():
    return get(MEDIA_PLAYER)

def set_player(val):
    set(MEDIA_PLAYER, val)

def get_vol():
    return get(VOL)

def set_vol(val):
    set(VOL, val)

def get_storage():
    return get(STORAGE)

def set_storage(val):
    set(STORAGE, val)

def get(key):
    global state
    
    val = None
    with lock:
        val = state[key]
    return val

def set(key, newval):
    global state

    with lock:
        state[key] = newval