import argparse
import subprocess


def Main(who, pitch):
    subprocess.Popen("sox -t alsa default -t pulseaudio {} ".format(who) +
                     "pitch {}".format(pitch), shell=True).communicate()


def argumentHandler():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--who", required=True,
                        help="who initiated the modulation? self or target?",
                        type=str, choices=["self", "target"])
    parser.add_argument("-p", "--pitch", required=True,
                        help="What's the pitch value?", type=int)
    args = parser.parse_args()
    return (args.who, args.pitch)

if __name__ == '__main__':
    (who, pitch) = argumentHandler()
    Main(who, pitch)
