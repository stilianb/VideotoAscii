import helpers as h
import constants as c
import cv2
import matplotlib.pyplot as plt
import argparse
import sys


def main():
    video = cv2.VideoCapture(c.input_video_path)  # Video input

    argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true',
                        help="a test flag")
    parser.add_argument('-b', '--blur', dest='b', action='store_true', help='adds blur')

    args = parser.parse_args()

    if len(argv) == 0:
        print("Converting original video to ascii...")
        converted_frames = h.convertFrames(video)

        print("Converting Frames into Gif...")
        h.createGif(converted_frames)

        print("Done!")
    if args.t:
        print("You hit the test flag!")
    if args.b:
        print("You hit the blur flag!")
        h.convertFramesGaussian(video)

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
