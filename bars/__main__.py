import argparse
from bars import play
import bars.play.main
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan and generate barcodes for playing music')

    with open('./config.json') as config_file:
        config = json.load(config_file)
    
    subparsers = parser.add_subparsers(help='sub-command help')

    play_parser = subparsers.add_parser('play', help='play tracks you scan')
    play.main.set_args(config, play_parser)

    play_parser = subparsers.add_parser('generate', help='generate barcodes')
    
    args = parser.parse_args()

    if args.mode == 'play':
        play.main.run(args, config)
    elif args.mode == 'generate':
        print('frrrrrrrp')