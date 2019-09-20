"""Boot file. Runs at boot (including wake-boot from deepsleep)"""

import gc
import webrepl
webrepl.start()
import utils
import shelfie

if __name__ == __main__():
    utils.setup_network(config="config.json")
    shelfie.clear_lights()
    gc.collect()
    shelfie.listen(config="config.json")
