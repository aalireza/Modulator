from multiprocessing import Process
import Toolbox
import subprocess
import time


def init():
    messenger, pitch, srcDir = Toolbox.config()
    selfID = Toolbox.loadNull("self")
    Toolbox.callMessenger(messenger, "self")
    return selfID, pitch, srcDir


def terminate(selfID):
    Toolbox.unloadNull(selfID)


def Main(who, pitch, srcParentDir):
    subprocess.Popen(str("x-terminal-emulator -e 'python {}/Modulator.py " +
                         "-w {} -p {}'").format(srcDir, who, pitch),
                     shell=True).communicate()

if __name__ == '__main__':
    selfID, pitch, srcDir = init()
    start = None
    while start not in ["y", "n"]:
        start = str(raw_input("Enter 'y' to start, enter 'n' to terminate: "))
        if start == "n":
            terminate(selfID)
            raise SystemExit
    try:
        selfProcess = Process(target=Main,
                              args=("self", pitch, srcDir))
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
