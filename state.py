from main import lock

state = {}

NFC_STATUS = 'nfcstatus'

def init():
    set(NFC_STATUS, False)


def get_nfc_status():
    return get(NFC_STATUS)

def set_nfc_status(val):
    set(NFC_STATUS, val)


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