# PS4Joystick

Code allowing to use a DualShock (PS4 Joystick) over bluetooth on linux. Over USB comming soon. `mac_joystick.py` shows how to emulate something similar on mac, but without the fancy features.

Note: we updating from the prevoous version make sure you disable ds4drv from running automatically at startup as they will conflict

This method still requires [ds4drv](https://github.com/chrippa/ds4drv) however it doesn't run it as a seperate service and then separatly pull joystick data using  pygame. Instead it imports ds4drv directly which gives us much more control over the joystick behaviour. Specifically:

- It will only pair to one joystick allowing us to run multiple robots at a time
- Allows for launching joystick code via systemd at boot using `sudo systemclt enable joystick`
- Can change joystick colors and using rumble directly from python (can also access the touchpad and IMU!)
- Is a much nicer interface then using pygame, as the axis are actully named as opposed to arbitrarly numbered! The axis directions are consistant with pygame. 
- Doesn't need $DISPLAY hacks to run on headless devices

### Usage

Take a look at `rover_example.py` as it demontrates most features. 
To implement this functionality to a new repository (say [PupperCommand](https://github.com/stanfordroboticsclub/PupperCommand)) you can just call `from PS4Joystick import Joystick` anywhere once you've installed the module. Replicate `joystick.service` in that repository.


### Install

``` sudo bash install.sh ```


### Mac

Sadly ds4drv doesn't work on macs. But you can get some of the functionality by installing pygame with `sudo pip3 install pygame`. Take a look in `mac_joystick.py` for an example. Note this only works over USB (plug the controller in using a micro usb cable) and the mapping is different then using pygame with ds4drv