from bars.play import track_lookup
import json
import cv2
import mutagen
import os
import time

def check_track_tags(barcode, library):

    matched_tracks = []

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

def find_track(raw_barcodes, mappings, library):

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

    for barcode in barcodes:
        if barcode in mappings:
            track_locations = mappings[barcode]
            return (barcode, track_locations)
        track_locations = check_track_tags(barcode, library)
        if len(track_locations) > 0:
            return (barcode, track_locations)
        track_locations = track_lookup.lookup_barcode_info(barcode, library)
        if track_locations is not None:
            return (barcode, track_locations)
    return None, None