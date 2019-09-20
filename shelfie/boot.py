"""Boot file. Runs at boot (including wake-boot from deepsleep)"""

import gc
import webrepl
# Remember to set the password initially.
# this uses webrepl_cfg.py
# and reads the PASS variable.j
webrepl.start()
import ujson as json
print("preparing imports")
import utils
import light

if __name__ == "__main__":
    print("Preparing to boot.")
    utils.setup_network()
    light.clear()
    gc.collect()
    print("boot complete.")
