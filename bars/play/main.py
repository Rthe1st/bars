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
import os.path

from bars.play import input_methods, lookup, output_methods

def set_args(
    parser=argparse.ArgumentParser(description='Scan (and generate) barcodes for playing music')
):

    return parser


def run(config_manager):

    loop_input = True
    previous_barcode = None

    while loop_input:

        input_method = config_manager.read_config("input-method")

        if input_method == 'webcam':
            scan_info, loop_input = input_methods.from_webcam()
        elif input_method == 'file':
            scan_info, loop_input = input_methods.from_image(config_manager.read_config("input-file"))
        elif input_method == 'file-monitoring':
            scan_info, loop_input = input_methods.file_monitoring(config_manager.read_config("input-file"))

        if scan_info is not None:
            barcode, relative_track_locations = lookup.find_track(scan_info, config_manager)

            if relative_track_locations is None:
                print('Search failed')
            elif barcode != previous_barcode:
                print('Found {}'.format(barcode))
                for track in relative_track_locations:
                    print(track)
                
                config_manager.write_data(barcode, relative_track_locations)

                print('output method')
                output_method = config_manager.read_config("output-method")

                if output_method == 'vlc':
                    output_method = output_methods.vlc_output
                elif output_method == 'symlink':
                    output_method = output_methods.symlink_output

                library = os.path.expanduser(config_manager.read_config("library"))

                absolute_track_locations = map(
                    lambda location: os.path.join(library, location),
                    relative_track_locations
                )

                output_method(absolute_track_locations, config_manager.read_config("output-folder"))
                previous_barcode = barcode
