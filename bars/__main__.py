import argparse
import json
import signal
import sys
import os
import shutil

from bars import play, generate,config_manager

def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan and generate barcodes for playing music')

    # todo: put this somewhere more accessible to users, like home directory
    parser.add_argument("--config-file", default='./settings/config.json')
    parser.add_argument("--data-file", default='./settings/data.json')

    parser.add_argument("-r", "--reset", action='store_true')

    subparsers = parser.add_subparsers(help='sub-command help', dest="mode")

    play_parser = subparsers.add_parser('play', help='play tracks you scan')
    play.main.set_args(play_parser)

    generate_parser = subparsers.add_parser('generate', help='generate barcodes')
    generate.main.set_args(generate_parser)

    args = parser.parse_args()

    a_config_manager = config_manager.ConfigManager(args.config_file, args.data_file, args.reset)

    if args.mode == 'play':
        play.main.run(a_config_manager)
    elif args.mode == 'generate':
        generate.main.run(args)
    else:
        print("No mode chosen, 'play' or 'generate'")
