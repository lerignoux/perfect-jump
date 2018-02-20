import logging
from math import sqrt
from time import sleep

from adb_com import AdbCom
from object_detection import ObjectDetection

log = logging.getLogger(__name__)


class GameHandler():

    turn_delay = 2
    pressure_unit = 1.667
    pressure_padding = 105

    def __init__(self, debug=False, simple=False):
        self.level = 0
        self.debug = debug
        self.simple = simple

    def play(self):
        while 1:
            self.play_turn()
            sleep(self.turn_delay)

    def play_turn(self):
        turn_detection = ObjectDetection(AdbCom().get_screenshot(), self.level, self.debug)
        player_pos = turn_detection.find_player()
        if self.simple:
            # y value should be enough since the jump angle is either 45 or 135 degrees.
            obj_y = turn_detection.next_block_y(*player_pos)
            y_diff = (obj_y - player_pos[1])
            log.info("Platform y distance: %s" % y_diff)
            press_time = int(sqrt(2*y_diff*y_diff) * self.pressure_unit) + self.pressure_padding
        else:
            # Computation using next platform full position
            objective_pos = turn_detection.next_block_pos(*player_pos)
            x_diff = (objective_pos[0] - player_pos[0])
            y_diff = (objective_pos[1] - player_pos[1])
            distance = sqrt(x_diff*x_diff + y_diff*y_diff)
            log.info("Platform distance: %s" % distance)
            press_time = int(distance * self.pressure_unit) + self.pressure_padding
        log.info("Asking move: press time %s " % press_time)
        AdbCom().send_keypress(press_time)
        self.level += 1
