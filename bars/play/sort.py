import mutagen

def tracks(locations):
    """
    Sort by:
        disc no
        trackno
        track name
        file name
    """

    file_data = {}

    for location in locations:
        track = mutagen.File(location)

        # TODO: less hackish way to do the lookup (in a tag-system independent way)
        # may have to use https://picard.musicbrainz.org/docs/mappings/
        if track is not None\
            and track.tags is not None:

            data = {}

            tags = track.tags
            if "TPOS" in tags:
                data["disc"] = track.tags["TPOS"].text[0]
            if "TRCK" in tags:
                track_no = track.tags["TRCK"].text[0]
                if "/" in track_no:
                    track_no = track_no.split("/")[0]
                try:
                    data["track"] = int(track_no)
                except ValueError:
                    data["track"] = 0
            if "TIT2" in tags:
                data["title"] = track.tags["TIT2"].text[0]

            file_data[location] = data            

    # this works because python sorts are "stable"
    locations = sorted(locations)
    locations = sorted(locations, key=lambda x: file_data[x].get("title", ""))
    locations = sorted(locations, key=lambda x: file_data[x].get("track", ""))
    locations = sorted(locations, key=lambda x: file_data[x].get("disc", ""))

    return locations
