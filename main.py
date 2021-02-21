import threading
import nfc_player
import web_interface

def start():
    thread_nfc = threading.Thread(target=nfc_player.init, name='nfc_thread')
    thread_nfc.start()

    web_interface.init()

if __name__ == '__main__':
    start()