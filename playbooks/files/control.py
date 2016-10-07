import signal
import multiprocessing
import time
from control_lirc import ControlLirc
from control_wii import ControlWii

wii_thread = None
lirc_thread = None


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    lirc_thread.terminate()
    wii_thread.terminate()
    exit()


def run_lirc():
    lirc_control = ControlLirc()
    while True:
        lirc_control.isConnected()
        time.sleep(10)


def run_wii():
    wii_control = ControlWii()
    while True:
        wii_control.isConnected()
        time.sleep(10)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

    lirc_thread = multiprocessing.Process(target=run_lirc)
    lirc_thread.start()
    wii_thread = multiprocessing.Process(target=run_wii)
    wii_thread.start()

    while True:
        time.sleep(5)
