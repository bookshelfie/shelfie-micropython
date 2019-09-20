# Shelfie

This repo contains the source for the micropython client for Shelfie. This
service just listens to a few topics on the Mosquitto MQTT and controls the
LEDs on the neopixels.

I've tested this code with ESP8266s controlling WS8212B Addressable RGB Strips.

## Demo

![Demo Gif](docs/static/image/demo.gif)

## Deployment

These instructions should work on any Linux based system. I cannot confirm whether they work on a Mac.

### Setting up MicroPython on the ESP8266

1. In a python virtualenv, install `esptool`.

    ``` bash
    python3 -m venv env
    source env/bin/activate
    pip install esptool
    ```

2. Connect the nodemcu to your computer using a microusb wire. Make sure the wire supports data transfer.

3. Run `ls /dev/ttyUSB*` to see where this is mounted. `/dev/ttyUSB0` is probably the nodemcu. If there are multiple, you need to check.

4. If your user is not in the dialout user group, you will not be able to continue, so make sure to add yourself to the group.

    ```bash
    sudo usermod -a -G dialout "$whoami"
    ```

5. Download the Micropython firmware for the ESP8266 from [here](http://micropython.org/download#esp8266).

    ```bash
    curl -O http://micropython.org/resources/firmware/esp8266-20190529-v1.11.bin
    ```

6. Delete existing firmware on the ESP8266.

    ```bash
    esptool.py --port /dev/ttyUSB0 erase_flash
    ```

7. Flash the micropython firmware.

    ```bash
    esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect 0 esp8266-20190529-v1.11.bin
    ```

### Testing MicroPython Installation

1. Install `screen` on your computer if you don't have it already.

    ```bash
    sudo apt-get install screen
    ```
    Screen is the recommended way to get into the MicroPython REPL, but there
    are alternatives such as `picocom` or `minicom`. Screen is the easiest to exit.
    Make sure you add `bind q quit` to `~/.screenrc` and use `<CTRL-a><q>` to quit.
    The default quit binding is `<CTRL-a><CTRL-c>`.
2. Test connection to ESP8266.
    ```bash
    screen /dev/ttyUSB0 115200
    ```

3. You *should* be dropped into a micropython prompt. Try to print the zen of MicroPython by using the following command.

    ```python
    >>> import this
    The Zen of MicroPython

    Code,
    Hack it,
    Less is more,
    Keep it simple,
    Small is beautiful,

    Be brave! Break things! Learn and have fun!
    Express yourself with MicroPython.

    Happy hacking! :-)
    ```

4. Enable the [WebREPL](http://micropython.org/webrepl/). This enables us to transmit the files using the CLI.

    First:
    ```bash
    screen /dev/ttyUSB0 115200
    ```
    Configure the client in the REPL.
    ```python
    >>> import webrepl_setup
    # This step will ask for a password for the network.
    # <ctrl-a><q>
    ```

5. Connect to the micropython wifi for the first time. The SSID will be of the form: `MicroPython-xxxxx`, and the password is what you set above.

6. Download the `webREPL` files.
    ```bash
    # install the webrepl
    git clone https://github.com/micropython/webrepl
    cd webrepl
    chmod u+x webrepl_cli.py
    ./webrepl_cli.py --help
    ```
7. Transfer the files to the nodemcu.
    ```bash
    # copy the config
    ./webrepl_cli.py -p password config/config.json 192.168.4.1:config.json
    # copy the shelfie.py module
    ./webrepl_cli.py -p password shelfie/boot.py 192.168.4.1:shelfie.py
    # copy the boot.py module.
    ./webrepl_cli.py -p password shelfie/boot.py 192.168.4.1/boot.py
    ```
8. Reboot the nodemcu.
    ```bash
    screen /dev/ttyUSB0 115200
    ```

    ```python
    >>> import machine
    >>> machine.reset()
    ```


## Configuration

The `config.json` file contains the main configuration. It should be populated
before deploying the application.

Here is a sample file with all *required* config values.

```json

{
    "meta":{
        "label": "a",
        "is_visible": true
    },
    "mqtt": {
        "host": "mosquitto",
        "port": 1883,
        "username": "shelfie",
        "password": "secure-password",
        "topics":
            {
                "shelf": "shelfie/{label}",
                "alert": "shelfie/alert"
            }
    },
    "lights": {
        "hold_time": 10,
        "blink_gap": 0.5,
        "blink_times": 3,
        "length": 100,
        "pin": 2,
        "colors": {
            "red": [255, 0, 0],
            "blue": [0, 0, 255],
            "green": [0, 255, 0],
            "yellow": [255, 255, 0],
            "orange": [255, 165, 0],
            "pink": [255, 192, 203],
            "cyan": [0, 255, 255],
            "magenta": [255, 0, 255],
            "white": [255, 255, 255],
            "black": [0, 0, 0],
            "1": [128, 0, 255],
            "2": [255,128,0],
            "3": [0,128,255],
            "4": [32,64,255]
        }
    },
    "networks": [
        {
            "ssid": "wifissid",
            "password": "wifipassword"
        }
    ]
}

```

## Development Notes

### Library

This client utilizes the [`umqtt`](https://github.com/micropython/micropython-lib/tree/master/umqtt.simple) library from MicroPython. Do not rely on third-party extensions. See [here](https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/example_pub.py) for a sample publisher and [here](https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/example_sub.py) for a sample subscriber.
