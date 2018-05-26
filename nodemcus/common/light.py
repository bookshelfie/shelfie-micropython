def get_number_of_neopixels():
    import ujson as json
    with open("neopixels.json", "r") as f:
        neopixels = json.load(f)
    return neopixels["number_of_leds"]

def get_neopixel():
    import neopixel, machine
    import ujson as json
    with open("neopixels.json", "r") as f:
        neopixels = json.load(f)
    number_of_leds =  neopixels["number_of_leds"]
    np = neopixel.NeoPixel(machine.Pin(neopixels["pin"]), number_of_leds) 
    return np

def das_blinken_lights():
    import time
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
    """16x = 12h
        16y = 60ms
    """
    import math
    n = get_number_of_neopixels()
    if h > 12:
        h -= 12 # for 24 hours.
    h_pos = math.ceil(n/12*h) - 1 - 8
    m_pos = math.ceil(n/60*m) - 1 - 8
    np = get_neopixel()
    np.fill((0,0,0))
    np[h_pos] = (lumens,lumens,0)
    if s is not None:
        s_pos = math.ceil(n/60*s) - 1 - 8

    np[m_pos] = (0,lumens,lumens)
    if s is not None:
        np[s_pos] = (lumens,0,lumens)
    np.write()

def test_ring():
    import time
    for h in range(12):
        for m in range(60):
            for s in range(60):
                show_time(h+1,m+1,s+1,lumens=16)
                time.sleep(0.025)
            print("The time is {}:{}".format(h,m))

def test_strip():
    import time
    import machine, neopixel
    n = 145
    np = neopixel.NeoPixel(machine.Pin(2), n)
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
    import time
    import machine, neopixel
    n = 145
    np = neopixel.NeoPixel(machine.Pin(2), n)
    lumens = 128
    for i in range(n):
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

def locate(pos):
    """Takes a book position and highlights it. Runs a trippy location
    algorithm too."""
    import time
    import math
    if isinstance(pos, float):
        pos = str(pos)
    col,row = pos.split(".")
    row = int(row)
    if ":" in col:
        col_start, col_end = col.split(":")
        col_start = int(col_start)
        col_end = int(col_end)
    else:
        col_start = col_end = int(col)
    number_of_neopixels = get_number_of_neopixels()
    # run a bisection animation.
    np = get_neopixel()
    np.fill((0,0,0))
    np.write()
    i = 0
    j = number_of_neopixels - 1
    while (i<= col_start) or (j >= col_end):
        if i<= col_start:
            np[i] = (255,0,0)
            i += 1
        if j>= col_end:
            np[j] = (255,0,0)
            j -=1
        np.write()
        time.sleep(0.0125)
    
    for i in range(col_start,col_end+1):
        np[i] = (0,255,255)
    np.write()
    
    time.sleep(1)
    for i in range(col_start,col_end+1):
        np[i] = (255,255,255)
    np.write()
    time.sleep(1)
    
    np.fill((0,0,0))
    if row == 1:
        color = (128,0,255)
    elif row == 2:
        color = (255,128,0)
    elif row == 3:
        color = (0,128,255)
    elif row == 4:
        color = (32,64,255)
    else:
        color = (0,0,0)
    for i in range(col_start,col_end+1):
        np[i] = color
    np.write()


def clear():
    np = get_neopixel()
    np.fill((0,0,0))
    np.write()        


    
