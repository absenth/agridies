""" Pull and Parse Band & Mode information from the attached rig. """

import shutil
import subprocess

model = "1"  # CHANGEME - get your rig id from `rigctl -l`
rig = "/dev/ttyUSB0"  # CHANGEME - set this to the tty your rig is on


def get_riginfo():
    """ pull band and mode data from the rig """
    mode = subprocess.run(['rigctl', '-m ' + model, '-r ' + rig, 'm'],
                          capture_output=True, text=True).stdout
    band = subprocess.run(['rigctl', '-m ' + model, '-r ' + rig, 'f'],
                          capture_output=True, text=True).stdout

    return(mode.splitlines()[0], band.splitlines()[0])


def detect_rigctl():
    if shutil.which("rigctl"):
        get_riginfo()
    else:
        print("rigctl doesn't appear installed.")
        # FIXME - Determine what the least painful path forward is
