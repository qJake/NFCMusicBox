# PN532 code from: https://www.waveshare.com/wiki/PN532_NFC_HAT#Resources

import state
import traceback
import threading
from time import sleep
from pn532 import PN532_SPI
DEVENV = False
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import Mock.GPIO as GPIO
    DEVENV = True

def start_nfc_thread():
    if not state.get_nfc_status():
        thread_nfc = threading.Thread(target=init, name='nfc_thread')
        thread_nfc.start()

def init():
    print('[NFC] Initializing NFC player...')

    try:
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
        print('[NFC] Waiting for RFID/NFC card...')
        while True:
            # Check if a card is available to read
            if not DEVENV:
                uid = pn532.read_passive_target(timeout=0.5)
            else:
                uid = None
                sleep(1)

            # Try again if no card is available.
            if uid is None:
                continue
            print('[NFC] Found card with UID:', [hex(i) for i in uid])
    except Exception as e:
        print('[NFC] Error doing NFC stuff!')
        print(e)
        traceback.print_tb(e.__traceback__)
    finally:
        GPIO.cleanup()
        state.set_nfc_status(False)
    
    # TODO: Maybe try to re-initialize GPIO here...? On a loop? Let the web UI do it?