from control_artik import *
import cwiid
import logging
import time

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class ControlWii(object):
    def __init__(self):
        self.connected = False
        self.wii = None
        self.button_delay = 0.25

    def close(self):
        exit(self.wii)
        exit()

    def vibrate(self):
        self.wii.rumble = 1
        time.sleep(1)
        self.wii.rumble = 0

    def isConnected(self):
        if not self.connected:
            try:
                self.wii = cwiid.Wiimote()
                self.wii.rpt_mode = cwiid.RPT_BTN
                self.connected = True
                logging.info('Wiimote connection established!')
                self.vibrate()
                self.monitor()
            except RuntimeError:
                self.connected = False
                self.wii = None
        return self.connected

    def monitor(self):
        while self.connected:
            buttons = self.wii.state['buttons']

            # Detects whether + and - are held down and if they are it quits the program
            if buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0:
                logging.info('Closing connection ...')
                # NOTE: This is how you RUMBLE the Wiimote
                self.vibrate()
                self.wii.close()
                self.connected = False
                return

            # The following code detects whether any of the Wiimotes buttons have been pressed
            # and then prints a statement to the screen!
            if buttons & cwiid.BTN_LEFT:
                send_left()
                time.sleep(self.button_delay)

            if buttons & cwiid.BTN_RIGHT:
                send_right()
                time.sleep(self.button_delay)

            if buttons & cwiid.BTN_UP:
                send_up()
                time.sleep(self.button_delay)

            if buttons & cwiid.BTN_DOWN:
                send_down()
                time.sleep(self.button_delay)

            if buttons & cwiid.BTN_HOME:
                send_home()
                time.sleep(self.button_delay)

