import json
import cv2
import mutagen
import os
import time
import easygui
import fleep
import glob
from bars.play import sort

def make_locations_relative(locations, library):
    
    library = os.path.expanduser(library)

    relative_locations = map(
        lambda location: location[len(library):],
        locations
    )
    return list(relative_locations)

def check_track_tags(barcode, library):

    matched_tracks = []
    
    library = os.path.expanduser(library)
    
    for subdir, _, files in os.walk(library):
        for file in files:
            location = os.path.join(subdir, file)
            track = mutagen.File(location)

            # TODO: less hackish way to do the lookup (in a tag-system independent way)
            # may have to use https://picard.musicbrainz.org/docs/mappings/
            if track is not None\
                and track.tags is not None\
                and barcode in track.tags.pprint():
                        matched_tracks.append(location)

    return matched_tracks

def ask_user(library):
    folder = easygui.diropenbox(default=library)

    locations = []

    for subdir, _, files in os.walk(folder):
        for file in files:
            location = os.path.join(subdir, file)
            with open(location, "rb") as file:
                info = fleep.get(file.read(128))
                if 'audio' in info.type:
                    locations.append(location)
    print(locations)

    return locations


def find_track(raw_barcodes, config_manager):

    print('processing')
    
    barcodes = []

    for raw_barcode in raw_barcodes:
        barcode = (raw_barcode.data).decode("utf-8")
        barcodes.append(barcode)

        # UPC barcodes are EAN barcodes with an implicit country code of zero
        # Search both UPC and EAN versions
        if len(barcode) == 12:
            # It's a UPC barcode
            # Add EAN equivalent
            barcodes.append('0' + barcode)
        elif len(barcode) == 13 and barcode[0] == '0':
            # It's EAN
            # Add UPC equivalent 
            barcodes.append(barcode[1:])

    print('found barcodes: {}'.format(barcodes))

    for barcode in barcodes:
        track_locations = config_manager.read_data(barcode)
        if track_locations is not None:
            print("Found via mappings")
            # we don't sort results from mappings
            # so users can manual sort entries where our sorting gets it wrong
            return (barcode, track_locations)

    for barcode in barcodes:
        track_locations = check_track_tags(barcode, config_manager.read_config("library"))
        if len(track_locations) > 0:
            print(" Found via tags")
            track_locations = sort.tracks(track_locations)
            return (barcode, make_locations_relative(track_locations, config_manager.read_config("library")))

    print("Couldn't find track automatically, please choose its file/folder")
    track_locations = ask_user(config_manager.read_config("library"))
    if len(track_locations) > 0:
        print(" Found via user")
        track_locations = sort.tracks(track_locations)
        return (barcode, make_locations_relative(track_locations, config_manager.read_config("library")))
    
    return None, None
