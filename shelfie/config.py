"""Config reader"""
import ujson as json

with open("config.json", "r") as f:
    config = json.load(f)


networks = config["networks"]
mqtt = config["mqtt"]
lights = config["lights"]
