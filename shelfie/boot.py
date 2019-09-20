"""Boot file. Runs at boot (including wake-boot from deepsleep)"""

import gc
import webrepl
webrepl.start()
import ujson as json
import utils
import light
import shelfie

if __name__ == __main__():
    with open("config.json", "r") as f:
        config = json.load(f)
    utils.setup_network(config=config)
    light.clear(config=config)
    gc.collect()
    shelfie.listen(config=config)
