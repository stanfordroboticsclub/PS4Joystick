import os
import pygame
from UDPComms import Publisher
import signal

drive_pub = Publisher(8830)
arm_pub = Publisher(8410)

# prevents quiting on pi when run through systemd
def handler(signum, frame):
    print("GOT singal", signum)
signal.signal(signal.SIGHUP, handler)

# those two lines allow for running headless (hopefully)
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.putenv('DISPLAY', ':0.0')

pygame.display.init()
pygame.joystick.init()

# wait until joystick is connected
while 1:
    try:
        pygame.joystick.Joystick(0).init()
        break
    except pygame.error:
        pygame.time.wait(500)

# Prints the joystick's name
JoyName = pygame.joystick.Joystick(0).get_name()
print("Name of the joystick:")
print(JoyName)
# Gets the number of axes
JoyAx = pygame.joystick.Joystick(0).get_numaxes()
print("Number of axis:")
print(JoyAx)

mode_file = open("/tmp/robot_joystick_mode.txt","r")

# Prints the values for axis0
while True:
    print("running")
    mode_file.seek(0)
    mode = mode_file.read()
    
    pygame.event.pump()

    if mode.startswith('drive'):
        forward_left  = -(pygame.joystick.Joystick(0).get_axis(1))
        forward_right = -(pygame.joystick.Joystick(0).get_axis(5))
        twist = (pygame.joystick.Joystick(0).get_axis(2))

        on_right = (pygame.joystick.Joystick(0).get_button(5))
        on_left = (pygame.joystick.Joystick(0).get_button(4))
        l_trigger = (pygame.joystick.Joystick(0).get_axis(3))

        if on_left or on_right:
            if on_right:
                forward = forward_right
            else:
                forward = forward_left

            slow = 150
            fast = 500
            max_speed = (fast+slow)/2 + l_trigger*(fast-slow)/2
            print(max_speed)
            drive_pub.send({'f':(max_speed*forward),'t':-150*twist})
        else:
            pass
            #without button go into freewheel
            drive_pub.send({'f':0,'t':0})

    if mode.startswith('arm'):
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

        # print("button")
        # for i in range(14):
        #     print(i, pygame.joystick.Joystick(0).get_button(i))
        # print("axis")
        # for i in range(12):
        #     print(i, pygame.joystick.Joystick(0).get_axis(i))

        hat = pygame.joystick.Joystick(0).get_hat(0)

        reset = (PS == 1) and (triangle == 1)
        reset_dock = (PS==1) and (square ==1)

        if(PS == 0):
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
        else:
              target_vel = {"x": 0,
                      "y": 0,
                      "z": 0,
                      "yaw": 0,
                      "pitch": 0,
                      "roll": 0,
                      "grip": 0,
                      "hat": (0,0),
                      "reset": reset,
                      "resetdock": reset_dock,
                      "trueXYZ": 0,
                      "dock":0}
        print(target_vel)
        arm_pub.send(target_vel)
    else:
        pass

    pygame.time.wait(100)
