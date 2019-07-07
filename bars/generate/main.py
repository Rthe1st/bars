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
import time
import barcode
import shutil
from barcode.writer import ImageWriter
from bars.play import input_methods

def set_args(
    config,
    parser=argparse.ArgumentParser(description='Generate barcodes for playing music')
):
    # TODO: work out the proper way to detect which subparser was used
    parser.add_argument("--mode", required=False, default='generate')

    parser.add_argument("--barcode", required=True)

    return parser

def save(barcode, track_location, config):
    config['mappings'][barcode] = track_location
    with open('./config.json', 'w+') as config_file:
        json.dump(config, config_file, indent=4, sort_keys=True)

def run(args, config):

    release_id = 'b2ac073a-4b6b-3fb2-95e7-c3434792b46a'

    response = requests.get(
        'http://musicbrainz.org/ws/2/release/{}?fmt=json'.format(release_id)
    ).json()

    correct_barcode = response['barcode']

    ean = barcode.EAN13(response['barcode'], writer=ImageWriter())
    fullname = ean.save('ean13_barcode')

    response = requests.get(
        'http://coverartarchive.org/release/{}/'.format(release_id)
    ).json()

    front_path = './front-cover.jpg'
    back_path = './back-cover.jpg'

    for image in response['images']:
        if 'Front' in image['types']:
            response = requests.get(
                image['image']
            )
            with open(front_path, 'wb') as f:
                f.write(response.content)
        elif 'Back' in image['types']:
            response = requests.get(
                image['image']
            )
            with open(back_path, 'wb') as f:
                f.write(response.content)
            
    # Scan cover to see if it has the (correct) barcode
    # If not, we'll have to paste one on

    barcode_found = False

    for path in [front_path, back_path]:
        raw_barcodes, _ = input_methods.from_image(path)

        if raw_barcodes is not None:
            for raw_barcode in raw_barcodes:
                the_barcode = (raw_barcode.data).decode("utf-8")
                if the_barcode ==  correct_barcode:
                    barcode_found = True
                    break

    if not barcode_found:

        # Some logic for working out where to place it would be cool

        background = Image.open(back_path)
        foreground = Image.open("ean13_barcode.png")

        background.paste(foreground, (0, 0))
        background.save('./printable_album.jpg', "JPEG")

    return