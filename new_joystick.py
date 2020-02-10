
import sys
import signal
import time

from threading import Thread

from ds4drv.actions import ActionRegistry
from ds4drv.backends import BluetoothBackend, HidrawBackend
from ds4drv.config import load_options
from ds4drv.daemon import Daemon
from ds4drv.eventloop import EventLoop
from ds4drv.exceptions import BackendError
from ds4drv.action import ReportAction

from ds4drv.__main__ import create_controller_thread
# from ds4drv.__main__ import SigintHandler


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
       new_out = {}
       for key in report.__slots__:
           value = getattr(report, key)
           new_out[key] = value

       self.values = new_out
       return True


def main():
    threads = []

    # sigint_handler = SigintHandler(threads)
    # signal.signal(signal.SIGINT, sigint_handler)

    try:
        options = load_options()
    except ValueError as err:
        Daemon.exit("Failed to parse options: {0}", err)

    if options.hidraw:
        raise ValueError("HID mode not supported")
        backend = HidrawBackend(Daemon.logger)
    else:
        backend = BluetoothBackend(Daemon.logger)

    try:
        backend.setup()
    except BackendError as err:
        print("backend error")
        Daemon.exit(err)

    thread = create_controller_thread(1, options.controllers[0])
    threads.append(thread)


    print("thread created")
    # time.sleep(1)
    thread.controller.setup_device(next(backend.devices))
    print("devices conencted")
    # time.sleep(1)

    shim = ActionShim(thread.controller)
    thread.controller.actions.append(shim)
    shim.enable()
    # time.sleep(1)

    while 1:
        if thread.controller.error:
            print("encountered error")
            exit(1)

        for key, value in shim.values.items():
            print(key,value)
        print()

        time.sleep(0.1)




if __name__ == "__main__":
    main()
