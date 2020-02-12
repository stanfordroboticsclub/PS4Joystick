
import sys
import signal
import time
import subprocess

from threading import Thread
from collections import OrderedDict

from ds4drv.actions import ActionRegistry
from ds4drv.backends import BluetoothBackend, HidrawBackend
from ds4drv.config import load_options
from ds4drv.daemon import Daemon
from ds4drv.eventloop import EventLoop
from ds4drv.exceptions import BackendError
from ds4drv.action import ReportAction

from ds4drv.__main__ import create_controller_thread


class ActionShim(ReportAction):
    """ intercepts the joystick report"""

    def __init__(self, *args, **kwargs):
        super(ActionShim, self).__init__(*args, **kwargs)
        self.timer = self.create_timer(0.02, self.intercept)
        self.values = {}

    def enable(self):
        self.timer.start()

    def disable(self):
        self.timer.stop()

    def load_options(self, options):
        if options.dump_reports:
            self.enable()
        else:
            self.disable()

    def intercept(self, report):
        dump = "Report magic dump\n"
        new_out = OrderedDict()
        for key in report.__slots__:
            value = getattr(report, key)
            new_out[key] = value

        for key in ["left_analog_x", "left_analog_y", "right_analog_x", "right_analog_y"]:
            new_out[key] =  (new_out[key] - 128) /128

        for key in ["l2_analog", "r2_analog"]:
            new_out[key] =  new_out[key] /256

        self.values = new_out
        return True

class Joystick:
    def __init__(self):
        self.thread = None
        signal.signal(signal.SIGINT, self.cleanup_thread)

        try:
            options = load_options()
        except ValueError as err:
            Daemon.exit("Failed to parse options: {0}", err)

        if options.hidraw:
            raise ValueError("HID mode not supported")
            backend = HidrawBackend(Daemon.logger)
        else:
            subprocess.run(["hciconfig", "hciX", "up"])
            backend = BluetoothBackend(Daemon.logger)

        try:
            backend.setup()
        except BackendError as err:
            print("backend error")
            Daemon.exit(err)

        self.thread = create_controller_thread(1, options.controllers[0])

        self.thread.controller.setup_device(next(backend.devices))

        self.shim = ActionShim(self.thread.controller)
        self.thread.controller.actions.append(self.shim)
        self.shim.enable()

    def cleanup_thread(self, *args):
        if self.thread is None:
            return
        self.thread.controller.exit("Cleaning up...")
        self.thread.controller.loop.stop()
        self.thread.join()

    def __del__(self):
        self.cleanup_thread()

    def print_values(self):
        while 1:
            for key, value in self.get_input().items():
                print(key,value)
            print()

            time.sleep(0.1)

    def get_input(self):
        if self.thread.controller.error:
            raise IOError("Encountered error with controller")

        return self.shim.values

    def led_color(self, red=0, green=0, blue=0):
        """ set RGB color in range 0-255"""
        self.thread.controller.device.set_led(red,green,blue)

    def rumble(self, small=0, big=0):
        """ rumble in range 0-255 """
        self.thread.controller.device.rumble(small,big)

    def led_flash(self, on=0, off=0):
        """ flash led: on and off times in range 0 - 255 """
        if(on == 0 and off ==0):
            self.thread.controller.device.stop_led_flash()
        else:
            self.thread.controller.device.start_led_flash(on,off)



if __name__ == "__main__":
    j = Joystick()
    j.print_values()
