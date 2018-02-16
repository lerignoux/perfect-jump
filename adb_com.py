import logging
import subprocess
import time

log = logging.getLogger(__name__)


class AdbCom():
    def __init__(self, device_id=None):
        self.device_id = device_id

    def get_screenshot(self):
        """
        Get the current device screenshot
        """
        args = {
            'device': ''
        }
        if self.device_id is not None:
            args['device'] = "-s %s" % self.device_id

        cmds = [
            "adb {device} shell screencap -p /sdcard/perfect_jump_screenshot.png".format(**args),
            "adb {device} pull /sdcard/perfect_jump_screenshot.png".format(**args),
            "adb {device} shell rm /sdcard/perfect_jump_screenshot.png".format(**args)
        ]

        for cmd in cmds:
            self._send_command(cmd)
        return "perfect_jump_screenshot.png"

    def send_keypress(self, duration=500, position=(0, 0)):
        """
        send a keypress event
        """
        args = {
            'device': '',
            'start_x': position[0],
            'start_y': position[1],
            'end_x': position[0],
            'end_y': position[1],
            'duration': duration
        }
        if self.device_id is not None:
            args['device'] = "-s %s" % self.device_id

        args['start_x'] = position[0]
        args['start_y'] = position[1]
        args['end_x'] = position[0]
        args['end_y'] = position[1]

        cmd = "adb shell {device} input touchscreen swipe {start_x} {start_y} {end_x} {end_y} {duration}".format(**args)
        self._send_command(cmd)

    def _send_command(self, command):
        child = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        child.communicate()[0]
        child.returncode
