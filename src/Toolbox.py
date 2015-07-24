import ConfigParser
import os
import subprocess


def config():
    configParser = ConfigParser.RawConfigParser()
    srcDir = os.path.dirname(os.path.abspath(__file__))
    srcParentDir = os.path.dirname(srcDir)
    configFilePath = '{}/config.txt'.format(srcParentDir)
    configParser.read(configFilePath)
    messenger = configParser.get('System', 'MESSENGER')
    pitch = int(configParser.get('Modulator', 'PITCH'))
    return messenger, pitch, srcDir


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
