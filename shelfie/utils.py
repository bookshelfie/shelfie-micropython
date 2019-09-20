"""Common utilities for the ESP8266
TODO: move this to a package."""


def setup_network():
    """Sets up the network based on a config."""
    import network
    import config
    # turn on wifi connectivity.
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)

    available_networks = sta_if.scan()

    # Enable access point.
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(True)

    network_data = config.networks

    for network in available_networks:
        network_name = network[0].decode()
        for network in network_data:
            if network_name == network["ssid"]:
                print("Connecting to {}".format(network_name))
                sta_if.connect(network_name, network["password"])
                break
