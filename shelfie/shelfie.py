"""shelfie core library"""

import light
from umqtt.simple as MQTTClient
import ujson as json
import config


def _type(topic):
    """Returns the topic type"""
    for topic_type, topic_name in config.mqtt["topics"]:
        if topic == topic_name:
            return topic_type
    return False


def alert(message):
    """general alert"""
    pass


def locate(message):
    """locates an item on the shelf"""
    pass


def process_message(topic, message):
    """Processes message"""
    if _type(topic) == "shelf":
        locate(message)
    elif _type(topic) == "alert":
        alert(message)


def listen():
    """Function that initiates listening to the mqtt topics."""
    client = MQTTCLient(
        "shelf_nodemcu_{label}".format(label=config.meta["label"]),
        config.mqtt["host"],
        config.mqtt["port"],
        config.mqtt["username"],
        config.mqtt["password"]
    )
    client.set_callback(process_message)
    client.connect()
    for topic in config.mqtt["topic"].values():
        client.subscribe(bytes("{}".format(topic), "utf-8"))
