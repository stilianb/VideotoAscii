import helpers as h
import constants as c
import cv2


def main():
    video = cv2.VideoCapture(c.input_video_path)  # Video input

    converted_frames = h.convertFrames(video)

    print("Converting Frames into Gif")
    h.createGif(converted_frames)

    print("Done!")

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
