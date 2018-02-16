import logging

import numpy as np

from skimage import io, color
from skimage.feature import match_template

log = logging.getLogger(__name__)


class ObjectDetection():

    player_data = "player.png"

    def __init__(self, image_path, level=0, debug=False):
        self.debug = debug
        self.level = level
        self.screen = self.load_image(image_path)
        self.player = self.load_image(self.player_data)
        log.debug("screen size: %s %s" % (len(self.screen), len(self.screen[0])))
        log.debug("player size: %s %s" % (len(self.player), len(self.player[0])))
        if self.debug:
            io.imsave("./debug/level_%s.png" % self.level, self.screen)

    def load_image(self, image_path):
        return io.imread(image_path)

    def get_best_match(self, result):
        pos = (0, 0)
        best = 0
        for i in range(len(result)):
            for j in range(len(result[i])):
                score = sum(result[i][j])
                if score > best:
                    best = score
                    pos = (i, j)
        return pos

    def find_player(self):
        player_area = self.screen[int(len(self.screen)/3): int(len(self.screen)*2/3), 0:-1]
        result = match_template(player_area, self.player, pad_input=True)

        ij = np.unravel_index(np.argmax(result), result.shape)
        _, y, x = ij[::-1]
        x = x + int(len(self.screen)/3)
        log.info("player position: %d,%d" % (x, y))
        return (x, y)

    def get_extreme_color(self, area):
        for i in range(len(area)):
            if max(area[i]) != min(area[i]):
                break
        max_val = area[i][0]
        max_index = 0
        min_val = area[i][0]
        min_index = 0
        for j in range(len(area[i])):
            if area[i][j] < min_val:
                min_index = j
                min_val = area[i][j]
            if area[i][j] > max_val:
                max_index = j
                max_val = area[i][j]
        if abs(max_val - area[0][0]) > abs(area[0][0] - min_val):
            return i, max_index
        else:
            return i, min_index

    def get_highest_platform(self, area):
        top_x, top_y = self.get_extreme_color(area)
        length = 0
        while area[top_x][top_y + length] == area[top_x][top_y]:
            length += 1
        top_y = int(top_y + length/2)
        log.info("platform top found: %s,%s" % (top_x, top_y))

        max_x = len(area)-1
        while area[max_x][top_y] != area[top_x][top_y]:
            max_x -= 1

        center = int((top_x + max_x) / 2), top_y
        log.info("platform center found: %s,%s" % center)
        return center

    def next_block_pos(self, player_x, player_y):
        area = self.screen
        ui_padding = int(len(area) / 4)
        max_x = player_x or len(area)
        area = area[ui_padding:max_x]
        # We remove player
        pdheight = int(len(self.player[0])/2)
        print(player_y-pdheight)
        area = np.concatenate((area[:, 0:player_y-pdheight], area[:, player_y+pdheight:-1]), axis=1)
        area = color.rgb2gray(area)
        if self.debug:
            io.imsave("./debug/level_%s_gray.png" % self.level, area)
        plat_x, plat_y = self.get_highest_platform(area)
        plat_x += ui_padding
        if plat_y >= player_y-pdheight:
            plat_y += 2*pdheight
        log.info("level platform position: %s,%s" % (plat_x, plat_y))
        return (plat_x, plat_y)
