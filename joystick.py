from UDPComms import Publisher
from new_joystick import Joystick

from enum import Enum

drive_pub = Publisher(8830)
arm_pub = Publisher(8410)

j=Joystick()

MODES = Enum('MODES', 'SAFE DRIVE ARM')
mode = MODES.SAFE

while True:

    values = j.get_input()

    if( values['button_ps'] ):
        if values['dpad_up']:
            mode = MODES.DRIVE
            j.led_color(red=255)
        elif values['dpad_right']:
            mode = MODES.ARM
            j.led_color(blue=255)
        elif values['dpad_down']:
            mode = MODES.SAFE
            j.led_color(green=255)
        continue


    if mode == MODE.DRIVE:
        forward_left  = - values['left_analog_y']
        forward_right = - values['right_analog_y']
        twist = values['right_analog_x')

        on_right = values['button_r1']
        on_left = values['button_l1']
        l_trigger = (pygame.joystick.Joystick(0).get_axis(3))

        if on_left or on_right:
            if on_right:
                forward = forward_right
            else:
                forward = forward_left

            slow = 150
            fast = 500
                       # this was -1 to 1. currently - to 1
            max_speed = (fast+slow)/2 + l_trigger*(fast-slow)/2
            print(max_speed)

            drive_pub.send({'f':(max_speed*forward),'t':-150*twist})
        else:
            drive_pub.send({'f':0,'t':0})

    if mode == MODE.ARM:
        r_forward  = -(pygame.joystick.Joystick(0).get_axis(5))
        r_side = (pygame.joystick.Joystick(0).get_axis(2))

        l_forward  = -(pygame.joystick.Joystick(0).get_axis(1))
        l_side = (pygame.joystick.Joystick(0).get_axis(0))

        r_shoulder  = (pygame.joystick.Joystick(0).get_button(5))
        l_shoulder  = (pygame.joystick.Joystick(0).get_button(4))

        r_trigger  = (pygame.joystick.Joystick(0).get_axis(4))
        l_trigger = (pygame.joystick.Joystick(0).get_axis(3))

        square  = (pygame.joystick.Joystick(0).get_button(0))
        cross  = (pygame.joystick.Joystick(0).get_button(1))
        circle  = (pygame.joystick.Joystick(0).get_button(2))
        triangle  = (pygame.joystick.Joystick(0).get_button(3))

        PS  = (pygame.joystick.Joystick(0).get_button(12)) 

        hat = pygame.joystick.Joystick(0).get_hat(0)

        reset = (PS == 1) and (triangle == 1)
        reset_dock = (PS==1) and (square ==1)
        
        target_vel = {"x": l_side,
                  "y": l_forward,
                  "z": (r_trigger - l_trigger)/2,
                  "yaw": r_side,
                  "pitch": r_forward,
                  "roll": (r_shoulder - l_shoulder),
                  "grip": cross - square,
                  "hat": hat,
                  "reset": reset,
                  "resetdock":reset_dock,
                  "trueXYZ": circle,
                  "dock": triangle}

        print(target_vel)
        arm_pub.send(target_vel)
    else:
        pass

    pygame.time.wait(100)
