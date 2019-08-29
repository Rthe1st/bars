# Bars

A project to make to make it easier to reconcile your physical and digital music collections and make interactions between them easier.

It's made of 2 parts, playing and generation.

Requirements:

* [vlc](https://www.videolan.org/vlc/index.en-GB.html)
* A webcam (ideally 1080p, less may struggle to scan properly)
* python (with [tkinter](https://wiki.python.org/moin/TkInter))

```bash
pipenv install bars
python -m bars play
```

## Playing

Using a web-camera, it scans physical media for a barcode.
It then finds the matching track(s) in your digital music collection and plays them.

If it can't find matching tracks, it'll ask you what tracks that barcode maps to (and remember that for next time)

## Generation

When you don't have a physical copy of track(s) in your digital collection (or when the physical media doesn't have a barcode), bars will generate one for you.

## Build/distribution

```bash
pyinstaller bars.spec
./dist/bars/bars.bin -h
```

## Physical -> Digitial mapping algorithm

Relies on the digital library being labeled.
This is either done via:

* Mappings in the JSON config file
  * These mappings are wildcarded filepaths
  * Wildcards will be expanded and overwritten to full track list when the program is run (todo: maybe change that)
* Tags on the digital tracks themselves

When physical media is scanned, it must provide a barcode. The locations above will then be searched for a match and all tracks matching will be loaded for playing.

Later versions will use 3rd party services to lookup meta-data from barcodes and match to digital tracks without pre-configuration.

## When physical media has no barcode

This program will do a reverse lookup, searching JSON config and tags for barcodes.

It will then generate a physical barcode from this that can be printed and scanned to play those tracks.

* This requires there to be a barcode common to all tracks on the physical media, and not used by any tracks NOT on that media. If none exists, this program will invent one.
