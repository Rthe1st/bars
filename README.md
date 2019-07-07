# Bars

A project to make to make it easier to reconcile your physical and digital music collections and make interactions between them easier.

It's made of 2 parts, playing and generation.

## Playing

Using a web-camera, it scans physical media for a barcode.
It then finds the matching track(s) in your digital music collection and plays them.

## Generation

When you don't have a physical copy of track(s) in your digital collection (or when the physical media doesn't have a barcode), bars will generate one for you.

## Physical -> Digitial mapping algorithm

Relies on the digital library being labeled.
This is either done via:

* Mappings in the JSON config file
* Tags on the digital tracks themselves

When physical media is scanned, it must provide a barcode. The locations above will then be searched for a match and all tracks matching will be loaded for playing.

Later versions will use 3rd party services to lookup meta-data from barcodes and match to digital tracks without pre-configuration.

## When physical media has no barcode

This program will do a reverse lookup, searching JSON config and tags for barcodes.

It will then generate a physical barcode from this that can be printed and scanned to play those tracks.

* This requires there to be a barcode common to all tracks on the physical media, and not used by any tracks NOT on that media. If none exists, this program will invent one.
