from bars.play import track_lookup
import json
import cv2

def find_track(barcodes, mappings, library):

    #TODO: decide how we prioritize acting on multiple barcodes
    print('processing')
    barcode_info = barcodes[0]
    barcode = (barcode_info.data).decode("utf-8")

    if barcode in mappings:
        track_location = mappings[barcode]
    else:
        track_location = track_lookup.lookup_barcode_info(barcode, library)

    if track_location is None:
        print('Search failed')
    
    print('Found {}'.format(track_location))
    print(track_location)
    return track_location