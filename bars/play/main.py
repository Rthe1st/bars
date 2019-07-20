import json
from pyzbar import pyzbar
from PIL import Image
import cv2
import os
import time
import argparse
import subprocess
import requests
import json
import os
import os.path

from bars.play import input_methods, lookup, output_methods


def set_args(
    config,
    parser=argparse.ArgumentParser(description='Scan (and generate) barcodes for playing music')
):
    # TODO: work out the proper way to detect which subparser was used
    parser.add_argument("--mode", required=False, default='play')

    parser.add_argument(
        '--input-method',
        choices=['webcam', 'file', 'file-monitoring'],
        default=config['input-method']
    )
    parser.add_argument('--input-file', required=False, default=config['input-file'])
    parser.add_argument('--library', required=False, default=config['library'])
    parser.add_argument(
        '--output-method',
        choices=['vlc', 'symlink'],
        required=False,
        default=config['output-method']
    )

    parser.add_argument(
        '--output-folder',
        required=False,
        default=config['output-folder']
    )

    # TODO: correctly parse strings feed to this as dicts
    parser.add_argument(
        '--mappings',
        required=False,
        default=config['mappings']
    )

    return parser

def save(barcode, relative_track_locations, config):

    config['mappings'][barcode] = relative_track_locations
    with open('./config.json', 'w+') as config_file:
        json.dump(config, config_file, indent=4, sort_keys=True)

def run(args, config):

    loop_input = True
    previous_barcode = None

    while loop_input:

        if args.input_method == 'webcam':
            scan_info, loop_input = input_methods.from_webcam()
        elif args.input_method == 'file':
            scan_info, loop_input = input_methods.from_image(args.input_file)
        elif args.input_method == 'file-monitoring':
            scan_info, loop_input = input_methods.file_monitoring(args.input_file)

        if scan_info is not None:
            barcode, relative_track_locations = lookup.find_track(scan_info, args.mappings, args.library)

            if relative_track_locations is None:
                print('Search failed')
            elif barcode != previous_barcode:
                print('Found {}'.format(barcode))
                for track in relative_track_locations:
                    print(track)
                
                save(barcode, relative_track_locations, config)

                if args.output_method == 'vlc':
                    args.output_method = output_methods.vlc_output
                elif args.output_method == 'symlink':
                    args.output_method = output_methods.symlink_output

                library = os.path.expanduser(config["library"])

                absolute_track_locations = map(
                    lambda location: os.path.join(library, location),
                    relative_track_locations
                )

                args.output_method(absolute_track_locations, args.output_folder)
                previous_barcode = barcode