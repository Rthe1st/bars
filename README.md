# Bars

A project to make to make it easier to physically interact with digital music collections

Boundary:
This program scans physical media and outputs the information needed by a music player to play the tracks on it.
If a music player is barcode aware, that could be as simple as a barcode
In reality, it's normally a list of files.

Stretch goal:
Before a system for reconciling a persons physical and digital music collections.

# Next
* Run acousticID on libary to try and find barcodes
** Save results to our config file (not file tags - in case we're wrong)
** This is a 'run once' kinda thing
*** Afterwards, should only need to be done on new tracks added to library
* Even if a track has no accoustic id found, might be worth doing a lookup on
filename/tags/etc during the 'run once' anyway

For users, we should recommend manual tagging with picard/etc
but strive to make it unnecessary

## Spec
* User scans a barcode
** Computer looks up and loads/plays matching track(s) (from existing library)
*** Support commercial barcodes (on CDs, etc)
*** Support VLC and Mixxx
* User can generate their own bar codes
** And choose what track(s) these match to
* User can scan barcodes for tracks not in their library
** Links them to ways to listen to/get the track(s)
** Should be global and zero config to support scanning someone elses code
* A way to print codes on a 'cardboard vinyl'
** Integrating them into pre-made or custom art work
** Printing in a standard form on good quality material

## What it can do

* Scan a barcode from an image or webcam
* Lookup that barcode on musicbrainz
** Look up 'title' of result to find file in users library
* Play that file with VLC
* Save the barcode->file mapping for next time

## Future
* improve barcode detection
    * buy hardware
    * try out techniques in comments
* generate barcodes that will map to a file
    * try to make config independant
        * so they can be used with different machines
* Inteligently map new barcodes to files
    * Using musicbrainz and/or by searching music directory
    * i.e. get track info for barcode from music brains
    * then compare this to folder names, tags, etc
    * cache this info
* generate machine-independant codes
    * spotify codes
    * dropbox urls
* machine-independant interpretation of pre-made codes?
    * music brain again?
* option for media player to play scanned tracks
* make it work with a real barcode scanner
    * this will need to support qr
* Scan a barcode on a computer and be able to play the track
** Track must already be on the computer
* Generate a barcode for a track on the computer

* Program maps barcode to a local file
** Could use musicbrainz for lookup
** https://python-musicbrainzngs.readthedocs.io/en/v0.6/usage/#identification
* A defined 'bars' file is sym-linked to that file

# Lookup

 2 pronged approach
 1) From music -> metadata -> barcode
 1) From barcode -> metadata -> track

1) Use accoustic ID to generate finter prints of libary
    acoustid.org
    https://pypi.org/project/pyacoustid/
    Then look those up on musicbrainz to find barcode (or mbid)
    Tag files localy with that info
    (MVB: store it in json and use that)

2) Scan libary/JSON for the barcode from step 1
    (Make this compatible with people who tagged barcodes via picard)
    If none found, lookup on musicbrains
        Then so match based on files names/tags etc
