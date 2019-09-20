"""Config reader
Example config:

{
    "meta":{
        "label": "a",
        "is_visible": true
    },
    "mqtt": {
        "host": "mosquitto",
        "port": 1883,
        "username": "shelfie",
        "password": "secure-password",
        "topics":
            {
                "shelf": "shelfie/{label}",
                "alert": "shelfie/alert"
            }
    },
    "lights": {
        "hold_time": 10,
        "blink_gap": 0.5,
        "blink_times": 3,
        "length": 100,
        "pin": 2,
        "colors": {
            "red": [255, 0, 0],
            "blue": [0, 0, 255],
            "green": [0, 255, 0],
            "yellow": [255, 255, 0],
            "orange": [255, 165, 0],
            "pink": [255, 192, 203],
            "cyan": [0, 255, 255],
            "magenta": [255, 0, 255],
            "1": [128, 0, 255],
            "2": [255,128,0],
            "3": [0,128,255],
            "4": [32,64,255]
        }
    },
    "networks": [
        {
            "ssid": "ssid1",
            "password": "password1"
        },
        {
            "ssid": "ssid2",
            "password": "password2"
        }
       ]
    }
}

"""

import ujson as json

with open("config.json", "r") as f:
    config = json.load(f)

networks = config["networks"]
meta = config["meta"]

mqtt = config["mqtt"]
mqtt["topics"]["shelf"] = mqtt["topics"]["shelf"].format(label=meta["label"])
# add the label to the shelf topic
# convert the color codes to tuples.
lights = config["lights"]
for key in lights["colors"].keys():
    lights["colors"][key] = tuple(lights["colors"][key])
