"""shelfie core library"""

import ujson as json
import time
from umqtt.simple as MQTTClient

import light
import config


def _type(topic):
    """Returns the topic type"""
    for topic_type, topic_name in config.mqtt["topics"]:
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
    time.sleep(config.lights.hold_time)
    light.clear()


def process_message(topic, message):
    """Processes message"""
    # TODO: convert the topic and message before using them.
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
    client = MQTTCLient(
        "shelf_nodemcu_{label}".format(
            label=config.meta["label"]),
        config.mqtt["host"],
        config.mqtt["port"],
        config.mqtt["username"],
        config.mqtt["password"]
    )
    client.set_callback(process_message)
    client.connect()
    for topic in config.mqtt["topic"].values():
        client.subscribe(bytes("{}".format(topic), "utf-8"))

    while True:
        if True:
            c.wait_msg() # blocking wait for message
        else:
            c.check_msg() # non-blocking wait for message
            time.sleep(1)
    client.disconnect()
