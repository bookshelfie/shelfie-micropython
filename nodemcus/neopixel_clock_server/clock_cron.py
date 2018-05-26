import requests
import datetime

import time

while True:
    d = datetime.datetime.now()
    if 6 <= d.hour <18:
        lumens = 255
    elif 18 <= d.hour < 20:
        lumens = 128
    elif 20<= d.hour < 23:
        lumens = 64
    else:
        lumens = 32
    r = requests.get("http://192.168.1.101/show_time", 
                     params={
                         "hour":d.hour, 
                         "minute": d.minute, 
                         "second": d.second, 
                         "lumens": lumens
                     })
    time.sleep(10)