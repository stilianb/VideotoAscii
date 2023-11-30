import helpers as h
import constants as c
from PIL import Image
import cv2
from tqdm import tqdm
import time


def main():
    video = cv2.VideoCapture(c.input_video_path)  # Video input
    count = c.frame_count
    converted_frames = []

    total_video_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = tqdm(range(total_video_frames))
    
    while count <= total_video_frames:
        ret, frame = video.read()

        if ret == False:
            break

        frame_img = Image.fromarray(frame).convert('L')
        ascii = h.frameToAscii(frame_img, c.frame_columns, c.frame_scale)
        converted_frame = h.asciiToFrame(ascii)
        converted_frames.append(converted_frame)

        progress_bar.update(1)
    progress_bar.close()

    h.createGif(converted_frames)

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
