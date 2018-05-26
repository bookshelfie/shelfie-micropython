# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc, webrepl, network
import ujson as json
from light import get_neopixel

webrepl.start()

sta_if = network.WLAN(network.STA_IF)
if not sta_if.active():
    sta_if.active(True)
    
available_networks = sta_if.scan()

with open("networks.json", "r") as f:
    network_data = json.load(f)
for network in available_networks:
    network_name = network[0].decode()
    if network_name in network_data.keys():
        sta_if.connect(network_name, network_data[network_name])
        break

np = get_neopixel()
np.fill((0,0,0))
np.write()

# Disable access point.
ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
    ap_if.active(False)



gc.collect()
