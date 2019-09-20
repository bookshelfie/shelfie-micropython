"""Boot file. Runs at boot (including wake-boot from deepsleep)"""

import gc
import webrepl
# Remember to set the password initially.
# this uses webrepl_cfg.py
# and reads the PASS variable.
webrepl.start()
import ujson as json
import utils
import light

if __name__ == __main__():
    with open("config.json", "r") as f:
        config = json.load(f)
    utils.setup_network(config=config)
    light.clear(config=config)
    gc.collect()
