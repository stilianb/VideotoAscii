import helpers as h
import cv2
import argparse
import sys


def main():
    argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='t', action='store_true',
                        help="a test flag")
    parser.add_argument('-b', '--blur', dest='b',
                        action='store_true', help='adds blur')
    parser.add_argument('-v', '--video', dest='v',
                        action='store_true', help='Convert given video into ASCII')
    parser.add_argument('-i', '--input', dest='input',
                        action='store', help='Path of input video')
    parser.add_argument('-o', '--output', dest='output',
                        action='store', help='Name of output video file')

    args = parser.parse_args()

    if len(argv) == 0:
        print("no flags")
        exit(0)

    video = cv2.VideoCapture(args.input)  # Video input

    if args.output != None:
        output_path = './output/' + args.output + '.gif'
    else:
        output_path = './output/output.gif'

    if args.v:
        print("Converting original video to ascii...")
        converted_frames = h.convertFrames(video)

        print("Converting Frames into Gif...")
        h.createGif(converted_frames, output_path)

        print("Done! Output located here: /output/" + args.output + '.gif')
    if args.t:
        print("You hit the test flag!")
        print(args.input)
        print(output_path)
    if args.b:
        print("You hit the blur flag!")
        h.convertFramesGaussian(video)

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
