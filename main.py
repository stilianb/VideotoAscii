import helpers as h
import constants as c
import cv2
import argparse


def main():
    video = cv2.VideoCapture(c.input_video_path)  # Video input

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', dest='v', action='store_true',
                        help="create video from input folder")

    args = parser.parse_args()

    if args.v:
        print("Converting original video to ascii...")
        converted_frames = h.convertFrames(video)

        print("Converting Frames into Gif...")
        h.createGif(converted_frames)

        print("Done!")

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
