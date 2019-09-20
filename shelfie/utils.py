"""Common utilities for the ESP8266
TODO: move this to a package."""

import network
import ujson as json


def setup_network(config):
    """Sets up the network based on a config."""
    # turn on wifi connectivity.
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)

    available_networks = sta_if.scan()

    # Disable access point.
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(True)

    with open(config, "r") as f:
        network_data = json.load(f)["networks"]

    for network in available_networks:
        network_name = network[0].decode()
        if network_name in network_data.keys():
            sta_if.connect(network_name, network_data[network_name])
            break
