import os
import json
import requests
import mutagen

def lookup_barcode_info(barcode, library, debug=False):
    # https://musicbrainz.org/doc/Development/JSON_Web_Service#Release
    # https://musicbrainz.org/doc/Release
    # TODO: https://www.discogs.com/developers/#page:database,header:database-search
    response = requests.get('http://musicbrainz.org/ws/2/release/?query=barcode:{}&fmt=json'.format(barcode))
    result = json.loads(response.content)
    if debug:
        print(json.dumps(result, indent=4, sort_keys=True))
    if result['count'] != 1:
        print('More then one found')
    else:
        release_info = result['releases'][0]
        name = release_info['release-group']['title']
        for dirpath, dirnames, filenames in os.walk(library, followlinks=True):
            if name in dirnames:
                # TODO: return list of files instead
                return [os.path.join(dirpath, name)]
    return None

def lookup_track_info(track_location):
    """
    This should be the exact opposite of lookup_barcode_info
    Because if we generate a barcode based on looking up a track
    Our program should return that exact same track when someone
    else looks up the barcode
    """
    return