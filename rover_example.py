from UDPComms import Publisher, Subscriber, timeout
from PS4Joystick import Joystick

import time
from enum import Enum

drive_pub = Publisher(8830)
telemetry = Subscriber(8810, timeout = 1)

j=Joystick()

MODES = Enum('MODES', 'SAFE DRIVE')
mode = MODES.SAFE
j.led_color(green=255, blue=180)

while True:
    values = j.get_input()

    if( values['button_ps'] ):
        if values['dpad_up']:
            mode = MODES.DRIVE
            j.led_color(red=255)
        elif values['dpad_down']:
            mode = MODES.SAFE
            j.led_color(green=255, blue=180)

    if mode == MODES.DRIVE:
        side_left  = values['left_analog_x']
        twist = values['right_analog_x']

        forward = - values['right_analog_y'] - values['left_analog_y']
        if forward < -1:
            forward = -1

        if forward > 1:
            forward = 1

        speed = 1000

        on_right = values['button_r1']
        # on_left = values['button_l1']
        # l_trigger = values['l2_analog']

        if on_right:
            out = {'y':speed* forward, 'x': speed*side_left, 't':-speed*twist}
            drive_pub.send(out)
            print(out)
        else:
            drive_pub.send({'y':0, 'x':0, 't':0})

        try:
            # {"left": [12.414477348327637, -0.9286113977432251, -0.017259109765291214], "right": [12.368555068969727, -0.501807451248169, 0.3269135355949402]}
            tele = telemetry.get()

            if len(tele) != 2:
                j.led_flash(on=10, off=10)
            else:
                voltage = min( item[0] for key,item in tele.items() )
                if voltage < 10.8:
                    j.led_flash(on=10, off=10)
                else:
                    j.led_flash(on=0, off=0)

        except timeout:
                j.led_flash(on=10, off=10)

    elif mode == MODES.SAFE:
        j.led_flash(on=0, off=0)

        # random stuff to demo color features
        triangle = values['button_triangle']
        square = values['button_square']

        j.rumble(small = 255*triangle, big = 255*square)

        # r2 = values['r2_analog']
        # r2 = j.map( r2, -1, 1, 0 ,255)
        # j.led_color( green = 255, blue = r2)

    else:
        pass

    time.sleep(0.1)
