# PN532 code from: https://www.waveshare.com/wiki/PN532_NFC_HAT#Resources

import sys
import state
import traceback
import threading
from event import Event
from time import sleep
from pn532 import PN532_SPI
DEVENV = False
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import Mock.GPIO as GPIO
    DEVENV = True

onLoad = Event()
onTagRead = Event()

def start_nfc_thread():
    nfc = NFCReader()
    if not state.get_nfc_status():
        thread_nfc = threading.Thread(target=nfc.init, name='nfc_thread')
        thread_nfc.start()

class NFCReader:
    def init(self):
        print('[NFC] Initializing NFC player...')

        self.lastTag = None

        try:
            GPIO.setwarnings(False)

            pn532 = PN532_SPI(debug=False, reset=20, cs=4)
            #pn532 = PN532_I2C(debug=False, reset=20, req=16)
            #pn532 = PN532_UART(debug=False, reset=20)
            
            if not DEVENV:
                ic, ver, rev, support = pn532.get_firmware_version()
            else:
                ver = 0
                rev = 0

            print('[NFC] Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()

            state.set_nfc_status(True)
            print('[NFC] Ready!')
            onLoad.fire()
            print('[NFC] Waiting for RFID/NFC card...')
            while True:
                # Check if a card is available to read
                if not DEVENV:
                    uid = pn532.read_passive_target(timeout=0.5)
                else:
                    uid = None

                # Try again if no card is available.
                if uid is None:
                    sleep(1)
                    continue
                else:
                    tag = int.from_bytes(uid, byteorder=sys.byteorder, signed=False)
                    self.lastTag = tag
                    onTagRead.fire(str(tag).strip())
                    # [hex(i) for i in uid] <-- do we need this? probably not...?
                    sleep(3) # don't spam the reader
        except Exception as e:
            print('[NFC] Error doing NFC stuff!')
            print(e)
            traceback.print_tb(e.__traceback__)
        finally:
            GPIO.cleanup()
            state.set_nfc_status(False)
        
        # TODO: Maybe try to re-initialize GPIO here...? On a loop? Let the web UI do it?