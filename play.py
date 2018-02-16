import argparse
import logging
import os
import sys

from game_handler import GameHandler

log = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

parser = argparse.ArgumentParser(description='Gather user anonymous feedback.')
parser.add_argument('--debug', '-d', dest='debug',
                    action='store_true',
                    help='Debug mode')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        if not os.path.exists("./debug"):
            os.makedirs("./debug")
        logging.getLogger().setLevel(logging.DEBUG)

    GameHandler(debug=args.debug).play()
