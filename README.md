# UDPJoystick

Code allowing to use a DualShock (PS4 Joystick) over bluetooth on linux. Over USB comming soon. `mac_joystick.py` shows how to emulate something similar on mac, but without the fancy features.

Note: we updating from the prevoous version make sure you disable ds4drv from running automatically at startup as they will conflict

This method still requires [ds4drv](https://github.com/chrippa/ds4drv) however it doesn't run it as a seperate service and then separatly pull joystick data using  pygame. Instead it imports ds4drv directly which gives us much more control over the joystick behaviour. Specifically:

- It will only pair to one joystick allowing us to run multiple robots at a time
- Allows for launching joystick code via systemd at boot using `sudo systemclt enable joystick`
- Can change joystick colors and using rumble directly from python (can also access the touchpad and IMU!)
- Is a much nicer interface then using pygame, as the axis are actully named as opposed to arbitrarly numbered! The axis directions are consistant with pygame. 
- Doesn't need $DISPLAY hacks to run on headless devices

### Usage

Checkout out `rover_example.py` as it demontrates most features. 
To copy this functionality to a new repository (say [PupperCommand](https://github.com/stanfordroboticsclub/PupperCommand)) copy the `PS4Joystick.py` file. 


### Install

``` sudo bash install.sh ```
