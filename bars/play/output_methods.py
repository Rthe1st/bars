import os
import subprocess
from bars.play import track_lookup

def symlink_output(track_locations, output_folder):
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass

    for track_location in track_locations:

        symlink_name = output_folder + '/' + track_location.split('/')[-1]
        try:
            os.symlink(track_location, symlink_name)
        except FileExistsError:
            pass

def vlc_output(track_locations, poop):
    """
    VLC will be killed when bars.py exits
    TODO: Cross platform support for letting vlc live on
    """
    cmd = ['vlc', '--started-from-file', '--playlist-enqueue']
    # TODO: sort by album order
    cmd.extend(track_locations)
    # TODO: redirect STDOUT and STDERR to a log file
    p = subprocess.Popen(cmd, stdout=None, stderr=subprocess.STDOUT)