import neopixel, machine
import ujson as json
import time
import math

import config

def test(pin, number, color):
    n = neopixel.NeoPixel(machine.Pin(pin), number)
    n.fill(color)
    n.write()


def get_neopixel():
    """Returns neopixel controller"""
    pin = config.lights["pin"]
    number_of_leds = config.lights["length"]
    np = neopixel.NeoPixel(machine.Pin(pin), number_of_leds)
    return np

def das_blinken_lights():
    """Trippy blinkenlights"""
    np = get_neopixel()
    for j in range(255):
        for i in range(n):
            np[i] = (j,0,0)
            np.write()
            time.sleep(0.1)
        for i in range(n):
            np[i] = (0,j,0)
            np.write()
            time.sleep(0.1)
        for i in range(n):
            np[i] = (0,0,j)
            np.write()
            time.sleep(0.1)
        for i in reversed(list(range(n))):
            np[i] = (0,0,0)
            np.write()

def show_time(h,m,s=None, lumens=255):
    """Time function for the 16 node neopixel ring
    16x = 12h
        16y = 60ms
    """
    np = get_neopixel()
    n = np.n
    if h > 12:
        h -= 12 # for 24 hours.
    h_pos = math.ceil(n/12*h) - 1 - 8
    m_pos = math.ceil(n/60*m) - 1 - 8
    np.fill((0,0,0))
    np[h_pos] = (lumens,lumens,0)
    if s is not None:
        s_pos = math.ceil(n/60*s) - 1 - 8

    np[m_pos] = (0,lumens,lumens)
    if s is not None:
        np[s_pos] = (lumens,0,lumens)
    np.write()

def test_ring():
    """Function to test the neopixel ring"""
    for h in range(12):
        for m in range(60):
            for s in range(60):
                show_time(h+1,m+1,s+1,lumens=16)
                time.sleep(0.025)
            print("The time is {}:{}".format(h,m))

def test_strip():
    """Function to test the neopixel strip"""
    np = get_neopixel()
    for j in range(255):
        lumens = 128
        for i in range(n):
            np[i] = (lumens,lumens,0)
            np.write()
            time.sleep(0.1)
        for i in range(n):
            np[i] = (0,lumens,lumens)
            np.write()
            time.sleep(0.1)
        for i in range(n):
            np[i] = (lumens,0,lumens)
            np.write()
            time.sleep(0.1)
        for i in reversed(list(range(n))):
            np[i] = (0,0,0)
            np.write()


def show_tenth_leds():
    """Marks the 10th LEDs of strip."""
    np = get_neopixel()
    lumens = 128
    for i in range(np.n):
        if (i+1)%10 == 0 :
            np[i] = (lumens,0,int(lumens/2))
            np.write()
            time.sleep(0.1)


def light_up(leds):
    """Pass a list of pairs of led positions and colours.
    Like so:

        >>> light_up([[1, (255,0,0)]])
    """
    np = get_neopixel()
    for rgb, led in leds:
        np[led] = rgb
    np.write()

def locate(col_start, col_end, row):
    """Takes a book position and highlights it.
    Runs a trippy location algorithm too."""
    np = get_neopixel()
    number_of_neopixels = np.n
    # run a bisection animation.
    np.fill((0,0,0))
    np.write()
    i = 0
    j = number_of_neopixels - 1
    while (i<= col_start) or (j >= col_end):
        if i<= col_start:
            np[i] = config.lights["colors"]["red"]
            i += 1
        if j>= col_end:
            np[j] = config.lights["colors"]["red"]
            j -=1
        np.write()
        time.sleep(0.0125)

    for i in range(col_start,col_end+1):
        np[i] = config.lights["colors"]["cyan"]
    np.write()

    time.sleep(1)
    for i in range(col_start,col_end+1):
        np[i] = config.lights["colors"]["white"]
    np.write()
    time.sleep(1)
    np.fill(config.lights["colors"]["black"])
    if row <= 4:
        color = config.lights["colors"][str(row)]
    else:
        color = config.lights["colors"]["white"]
    for i in range(col_start,col_end+1):
        np[i] = color
    np.write()


def clear():
    np = get_neopixel()
    np.fill((0,0,0))
    np.write()
    state = "OFF"
    with open("state.json", "w") as buffer:
        buffer.write(json.dumps({"state":"OFF"}))


def show_progress(progress, color=None):
    np = get_neopixel()
    if progress == 100:
        pixels = np.n
    else:
        pixels = math.floor(progress*np.n/100)
    if color is None:
        color=(255,255,255)
    elif isinstance(color,str):
        color = eval(color)
    elif isinstance(color,tuple) or isinstance(color,list):
        color = color
    np.fill((0,0,0))
    for i in range(pixels):
        np[i] = color
    np.write()

def blink(color=None, t=0.2):
    """Blinks the strip"""
    if color is None:
        color = (255,255,255)
    elif isinstance(color,str):
        color = eval(color)
    np = get_neopixel()
    for i in range(3):
        np.fill((0,0,0) if i in [0,2] else color)
        np.write()
        time.sleep(t)


def change_state(color=None):
    """Toggles the state of the strip."""
    import os
    if color is None:
        color = (255,255,255)
    elif isinstance(color,str):
        color = eval(color)
    state_file = "state.json"
    if state_file in os.listdir():
        with open(state_file, "r") as buffer:
            state_json = json.load(buffer)
        print(state_json)
        state = state_json.get("state", "OFF")
    else:
        state = "OFF"
    if state == "OFF":
        print("Turning it on. Color: {}".format(color))
        np = get_neopixel()
        np.fill(color)
        np.write()
        with open("state.json", "w") as buffer:
            buffer.write(json.dumps({"state":"ON"}))
    else:
        print("Turning it off")
        clear()


def snake(
    stop=None, reverse=False, lumens=128,
    length=5, longpause=0.1, shortpause=0.01):
    """Snakes its way through the LEDs"""
    import urandom

    np = get_neopixel()
    if stop is None:
        if reverse:
            stop = 0
        else:
            stop = np.n-1
    if reverse:
            path = reversed(range(stop, np.n))
    else:
        path = range(0, stop)
    print(list(path))
    colors = []
    #for j in range(length):
        #colors.append((int(urandom.getrandbits(8)/(j+1)), int(urandom.getrandbits(8)/(j+1)), int(urandom.getrandbits(8)/(j+1))))
    colors = [
        (0, int(lumens/6), int(lumens/6/2)),
        (0, int(lumens/5), int(lumens/5/2)),
        (0, int(lumens/4), int(lumens/4/2)),
        (0, int(lumens/3), int(lumens/3/2)),
        (0, int(lumens/2), int(lumens/2/2))
    ]
    colors = list(reversed(colors))
    pointer_colors = [
        (0, 0, lumens),
        (0, lumens, 0),
        (lumens, 0, 0 ),
        (lumens, 0, lumens),
        (lumens, lumens, 0),
        (0, lumens, lumens),
        (lumens, lumens, lumens)
    ]
    for i in path:
        np.fill((0,0,0))
        if not reverse:
            for j in range(length):
                position = i-(j+1)
                if (0 <= position <= stop):
                    np[position] = colors[j]

            np.write()
            if 0<=i<=(stop):
                for c in pointer_colors:
                    np[i] = c
                    np.write()
                    time.sleep(shortpause)
            else:
                for c in pointer_colors:
                    np[stop] = c
                    np.write()
                    time.sleep(shortpause)
        else:
            for j in range(length):
                position = (i+(j+1))
                if (0 <= position <= stop):
                    np[position] = colors[j]
            np.write()
            if 0<=i<stop:
                for c in pointer_colors:
                    np[i] = c
                    np.write()
                    time.sleep(shortpause)
            else:
                for c in pointer_colors:
                    np[stop] = c
                    np.write()
                    time.sleep(shortpause)
        time.sleep(longpause)
    for i in path[-5:-1]:
        np[i] = (0,0,0)
        np.write()
        time.sleep(longpause)
