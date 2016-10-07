import bluetooth
from control_artik import *
import logging
import socket
import string
import subprocess
import sys
import time
import threading

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class ControlLirc(object):
    def __init__(self):
        self.connected = False
        self.sock = None
        self.socket_path = "/var/run/lirc/lircd"
        self.button_delay = 0.25

    def close(self):
        self.sock.close()
        exit(self.sock)
        exit()

    def isConnected(self):
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
        for addr, name in nearby_devices:
            output, error = subprocess.Popen("echo 'info %s\nquit' | bluetoothctl" % (addr), shell=True,
                                             stdout=subprocess.PIPE).communicate()
            if output.find("Connected: yes") == -1:
                subprocess.call("echo 'connect %s\nquit' | bluetoothctl" % (addr), shell=True)

        if not self.connected:
            self.tryConnection()
            threading.Thread(target=self.monitor).start()
        return self.connected

    def connectEventLircd(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)

    def tryConnection(self):
        try:
            self.connectEventLircd()
            self.connected = True
            logging.info("connected to Lirc-Socket on %s" % self.socket_path)
            # self.monitor()
        except socket.error as msg:
            logging.error("connection error %s" % msg)
            self.connected = False

    def monitor(self):
        while self.connected:
            try:
                buf = self.sock.recv(128)
                if not buf:
                    self.sock.close()
            except:
                logging.error("monitoring error ", sys.exc_info()[0])
                self.sock.close()

            lines = string.split(buf, "\n")
            for line in lines[:-1]:
                code, count, cmd, device = string.split(line, " ")[:4]
                if count == "0":
                    if cmd == "KEY_UP":
                        send_up()
                        time.sleep(self.button_delay)
                    elif cmd == "KEY_DOWN":
                        send_down()
                        time.sleep(self.button_delay)
                    elif cmd == "KEY_LEFT":
                        send_left()
                        time.sleep(self.button_delay)
                    elif cmd == "KEY_RIGHT":
                        send_right()
                        time.sleep(self.button_delay)
                    elif cmd == "KEY_HOME":
                        send_home()
                        time.sleep(self.button_delay)
