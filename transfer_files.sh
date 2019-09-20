#!/bin/bash

./webrepl/webrepl_cli.py -p $1 shelfie/config.py $2:/config.py
./webrepl/webrepl_cli.py -p $1 config/config.json $2:/config.json
./webrepl/webrepl_cli.py -p $1 shelfie/light.py $2:/light.py
./webrepl/webrepl_cli.py -p $1 shelfie/utils.py $2:/utils.py
./webrepl/webrepl_cli.py -p $1 shelfie/shelfie.py $2:/shelfie.py
./webrepl/webrepl_cli.py -p $1 shelfie/main.py $2:/main.py
./webrepl/webrepl_cli.py -p $1 shelfie/boot.py $2:/boot.py
