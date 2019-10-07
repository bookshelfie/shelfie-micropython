"""shelfie core library"""

import time
import ujson as json
from umqtt.simple import MQTTClient

import light
import config

__version__ = "0.2"


def _type(topic):
    """Returns the topic type"""
    for topic_type, topic_string in config.mqtt["topics"].items():
        if type(topic_string) == list:
            if topic in topic_string:
                return topic_type
        elif topic == topic_string:
            return topic_type
    return False


def alert(color, blink=True, times=config.lights["blink_times"]):
    """general alert"""
    np = light.get_neopixel()
    np.clear()
    counter = 1
    while counter <= times:
        for i in range(np.n):
            np[i] = color
        np.write()
        time.sleep(
            config.lights["blink_gap"]
            )
        counter += 1
        if not blink:
            break


def locate(positions):
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
    topic_type = _type(topic)
    if topic_type == "shelf":
        locate(**message)
    elif topic_type == "alert":
        alert(**message)
    elif topic_type == "highlight":
        n = message.get("n", 10)
        light.show_nth_leds(n)
    elif topic_type == "clear":
        light.clear()
        light.clear()


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
