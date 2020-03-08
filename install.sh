#!/usr/bin/env sh

if [ "$(uname)" == "Darwin" ]; then
	echo "ds4drv doesn't work on Mac OS!"
	echo "try installing pygame (commented out in this script) and running mac_joystick.py"
	exit 0
fi

FOLDER=$(dirname $(realpath "$0"))
cd $FOLDER

yes | sudo pip3 install ds4drv
sudo python3 setup.py clean --all install