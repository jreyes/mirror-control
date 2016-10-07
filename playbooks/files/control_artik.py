import json
import logging
import os
import requests
import threading
import time

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def send_action(action):
    try:
        headers = {"Content-Type": "application/json", "Authorization": "Bearer %s" % os.environ['DEVICE_TOKEN']}
        data = {
            "sdid": os.environ['DEVICE_ID'],
            "ts": int(round(time.time() * 1000)),
            "type": "message",
            "data": {"action": action}
        }
        logging.debug("sending %s" % json.dumps(data))
        response = requests.post("https://api.artik.cloud/v1.1/messages", data=json.dumps(data), headers=headers)
        logging.debug("response: %s" % response.text)
    except Exception as ex:
        print("Could not send action: " + str(ex))


def send_left():
    threading.Thread(target=send_action, args=("left",)).start()


def send_right():
    threading.Thread(target=send_action, args=("right",)).start()


def send_up():
    threading.Thread(target=send_action, args=("up",)).start()


def send_down():
    threading.Thread(target=send_action, args=("down",)).start()


def send_home():
    threading.Thread(target=send_action, args=("home",)).start()
