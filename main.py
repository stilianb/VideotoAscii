import helpers as h
import cv2
import argparse
import sys


def main():
    argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', dest='v',
                        action='store', help='Convert given video into ASCII')
    parser.add_argument('-i', '--input', dest='input',
                        action='store', help='Path of input video')
    parser.add_argument('-d', '--depth', dest='depth', type=int,
                        action='store', help='Size of ASCII scale')
    parser.add_argument('-f', '--frame', dest='f',
                        action='store', help='outputs image at given location')
    parser.add_argument('-g', '--gaussian', dest='g',
                        action='store_true', help='Apply Gaussian blur')
    parser.add_argument('-l', '--laplacian', dest='l',
                        action='store_true', help='Apply Laplacian filter')

    args = parser.parse_args()

    if len(argv) == 0:
        print("no flags")
        exit(0)

    video = cv2.VideoCapture(args.input)  # Video input

    if args.v != None:
        output_path = './output/' + args.v + '.gif'
    else:
        output_path = './output/output.gif'

    if args.depth == None:
        args.depth = 9

    flags = {'g': args.g, 'l': args.l}
    if args.v:
        print("Converting original video to ascii...")
        converted_frames = h.convertFrames(video, args.depth, flags)

        print("Converting Frames into Gif...")
        h.createGif(converted_frames, output_path)

        print("Done! Output located here: /output/" + args.v + '.gif')
    if args.f:
        print("Creating Ascii Image")
        output_path = './output/' + args.f + '.png'
        h.outputFrame(video, args.depth, output_path, flags)

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
