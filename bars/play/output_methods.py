import os
import subprocess
from bars.play import track_lookup

def symlink_output(track_location, output_folder):
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass

    symlink_name = output_folder + '/' + track_location.split('/')[-1]
    try:
        os.symlink(track_location, symlink_name)
    except FileExistsError:
        pass

def vlc_output(track_location, poop):
    cmd = ['vlc', '--started-from-file', '--playlist-enqueue', track_location]
    p = subprocess.Popen(cmd)