"""shelfie core library"""

import ujson as json
import time
from umqtt.simple import MQTTClient

import light
import config

__version__ = "0.1"

def _type(topic):
    """Returns the topic type"""
    for topic_type, topic_name in config.mqtt["topics"].items():
        if topic == topic_name:
            return topic_type
    return False


def alert(color, blink=True, times=2):
    """general alert"""



def locate(positions, color):
    """locates an item on the shelf"""
    if "." in positions:
        positions, row = positions.split(".")
    else:
        row = 1
    if ":" in positions:

        start, end = positions.split(":")
    else:
        start = end = positions
    start, end, row = int(start), int(end), int(row)
    light.locate(start, end, row)
    print("holding lights for a while.")
    time.sleep(config.lights["hold_time"])
    light.clear()
    print("clearing lights")

def process_message(topic, message):
    """Processes message"""
    # TODO: convert the topic and message before using them.
    print((topic, message))
    topic = topic.decode()
    message = json.loads(message.decode())
    if _type(topic) == "shelf":
        locate(**message)
    elif _type(topic) == "alert":
        alert(**message)
    else:
        alert(config.lights["colors"]["red"],)


def listen():
    """Function that initiates listening to the mqtt topics."""
    client_id = "shelf_nodemcu_{label}".format(
            label=config.meta["label"])
    host = config.mqtt["host"]
    port = config.mqtt["port"]
    user = config.mqtt["username"]
    password = config.mqtt["password"]
    client = MQTTClient(
        client_id,
        host,
        port,
        user,
        password
    )
    print("Configuring callbacks")
    client.set_callback(process_message)
    client.connect()
    for topic in config.mqtt["topics"].values():
        client.subscribe(bytes("{}".format(topic), "utf-8"))
    print("listening...")
    while True:
        if True:
            client.wait_msg() # blocking wait for message
        else:
            client.check_msg() # non-blocking wait for message
            time.sleep(1)
    client.disconnect()
