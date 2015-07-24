from multiprocessing import Process
import Toolbox
import ConfigParser
import subprocess
import time


configParser = ConfigParser.RawConfigParser()
configFilePath = r'../config.txt'
configParser.read(configFilePath)
messenger = configParser.get('System', 'MESSENGER')
pitch = int(configParser.get('Modulator', 'PITCH'))


def init():
    Toolbox.checkDataDir()
    selfID = Toolbox.loadNull("self")
    Toolbox.callMessenger(messenger, "self")
    return selfID


def terminate(selfID):
    Toolbox.unloadNull(selfID)


def Main(who, pitch):
    subprocess.Popen(str("x-terminal-emulator -e 'python ./Modulator.py " +
                         "-w {} -p {}'".format(who, pitch)),
                     shell=True).communicate()

if __name__ == '__main__':
    selfID = init()
    start = None
    while start not in ["y", "n"]:
        start = str(raw_input("Enter 'y' to start, enter 'n' to terminate: "))
        if start == "n":
            terminate(selfID)
            raise SystemExit
    try:
        selfProcess = Process(target=Main,
                            args=("self", pitch,))
        selfProcess.start()
        while selfProcess.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        selfProcess.terminate()
        selfProcess.join()
        print "Program is about to be terminated"
    finally:
        terminate(selfID)
        print "Program is terminated"
