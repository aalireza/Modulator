import time
import os
import subprocess


def checkDataDir():
    # r'../data/temp' directory is used to temporary storage of
    # to-be-transmitted audio-files.
    if not os.path.exists("../data/"):
        os.makedirs("../data/")
    if not os.path.exists("../data/self"):
        os.makedirs("../data/self")
    if not os.path.exists("../data/self/log"):
        os.makedirs("../data/self/log")
    if not os.path.exists("../data/target"):
        os.makedirs("../data/target")
    if not os.path.exists("../data/target/log"):
        os.makedirs("../data/target/log")


def loadNull(who):
    # Loading null-sink-module for the messanger.
    assert who in ["self", "target"], "'who' is neither self nor target"
    procID = subprocess.check_output("pactl load-module module-null-sink " +
                                     "sink_name={}".format(who),
                                     shell=True)
    procID = int(procID.rstrip('\n'))
    if type(procID) != int:
        print "Loading module for '{}' failed".format(who)
        raise SystemExit
    print ("Loaded module-null-sync with index: " + str(procID) +
           ", for '{}' successfuly.".format(who))
    return procID


def unloadNull(ID):
    subprocess.Popen("pactl unload-module " + str(ID), shell=True)


def callMessenger(messenger, who):
    # Must have used loadNull() first. Also, you may change the messenger type
    # in config.txt
    subprocess.Popen(str("PULSE_SOURCE={}.monitor " + messenger).format(who),
                     shell=True)
