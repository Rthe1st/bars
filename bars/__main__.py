import argparse
from bars import play
import bars.play.main
from bars import generate
import bars.generate.main
import json

import signal
import sys
def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan and generate barcodes for playing music')

    with open('./config.json') as config_file:
        config = json.load(config_file)
    
    subparsers = parser.add_subparsers(help='sub-command help', dest="mode")

    play_parser = subparsers.add_parser('play', help='play tracks you scan')
    play.main.set_args(config, play_parser)

    generate_parser = subparsers.add_parser('generate', help='generate barcodes')
    generate.main.set_args(config, generate_parser)

    args = parser.parse_args()

    if args.mode == 'play':
        play.main.run(args, config)
    elif args.mode == 'generate':
        generate.main.run(args, config)