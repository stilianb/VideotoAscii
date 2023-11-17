import helpers as h
from PIL import Image
import cv2


def main():
    video = cv2.VideoCapture('./videos/sample.qt')
    count = 0
    converted_frames = []
    control = True

    while video.isOpened():
        ret, frame = video.read()

        if ret == False:
            control = False
            break

        frame_img = Image.fromarray(frame).convert('L')
        ascii = h.frameToAscii(frame_img, 100, 0.43)
        converted_frame = h.asciiToFrame(ascii)
        converted_frames.append(converted_frame)
        count += 1

        print(count)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        # if count == 10: break

    h.createGif(converted_frames)

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
