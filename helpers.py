import numpy as np
import constants as c
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Get the average luminance value of a given image
# References:
# Input (image): JPEG or opencv image


def getAverageLuminance(image):
    # Convert image to NumPy Array
    img = np.array(image)

    # Using NumPy .shape to get image width and height
    width, height = img.shape

    # Rotate array by image shape
    reshaped = img.reshape(width * height)

    # Get average luminance value of reshaped image
    avg = np.average(reshaped)

    return avg


# Convert a given frame into a 2d ascii array
# References:

def frameToAscii(frame, cols, scale, depth):
    # Getting input frame size
    W, H = frame.size[0], frame.size[1]

    width = W / cols
    height = width / scale
    rows = int(H / height)

    # Check if image fits output columns
    if cols > W or rows > H:
        print(c.scale_err)
        exit(0)

    ascii = []  # Holds generated ascii characters
    for i in range(rows):
        y1 = int(i * height)
        y2 = int((i + 1) * height)

        if i == rows - 1:
            y2 = H

        ascii.append("")

        for j in range(cols):
            x1 = int(j * width)
            x2 = int((j + 1) * width)

            if j == cols - 1:
                x2 = W

            # Crop pixel at location
            ascii_img = frame.crop((x1, y1, x2, y2))

            # Get average luminance value of cropped image
            avg = int(getAverageLuminance(ascii_img))

            # Assign key in gscale according to average luminance
            gsval = c.gscale[int((avg * depth) / 255)]

            # Add resulting key to ascii array
            ascii[i] += gsval

    return ascii


# Apply generated ascii text onto newly created image
# References:

def asciiToFrame(ascii):
    # Accessing font for ascii image
    font = ImageFont.truetype(c.font_path, c.font_size)

    # Creating a scaffold image
    img = Image.new(mode="RGBA", size=(
        c.scaffold_w, c.scaffold_h), color=(0, 0, 0, 0))

    # Canvas to draw on newly created scaffold
    img_draw = ImageDraw.Draw(img)

    # Adding ascii characters to scaffold image
    y = 0
    for i in ascii:
        x = 0
        for j in i:
            img_draw.text((x, y), j, font=font, fill=c.white_bg)
            # gap-x between keys on image
            x += c.key_variance_x
        # gap-y between keys on image
        y += c.key_variance_y

    return img


def convertFrames(video, depth, flags):
    converted_frames = []  # for function output

    # total number of frames that need to be converted
    total_video_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # status bar based on number of converted frames
    progress_bar = tqdm(range(total_video_frames))

    while video.isOpened():
        # Read frame
        ret, frame = video.read()

        if ret == False:
            break

        # Check for any image processing
        if flags['g']:
            frame = cv2.GaussianBlur(frame, (151, 151), 0)
        if flags['l']:
            frame = cv2.Laplacian(frame, -1, ksize=5)

        # Convert frame into a PIL Image
        frame_img = Image.fromarray(frame).convert('L')

        # Convert Image to ASCII
        ascii = frameToAscii(frame_img, c.frame_columns, c.frame_scale, depth)

        # Convert newly created ASCII to a frame
        converted_frame = asciiToFrame(ascii)

        # Add created frame to output array
        converted_frames.append(converted_frame)

        # Update progress bar
        progress_bar.update(1)

    progress_bar.close()

    return converted_frames


# Add created ascii images together into playable gif and output the file
# References:
# Input (frames):
#   frames: VideoFrame (output from asciiToFrame(ascii))


def createGif(frames, output):
    gif = []
    progress_bar = tqdm(range(len(frames)))
    for i in frames:
        gif.append(i.convert("P", palette=Image.ADAPTIVE))
        progress_bar.update(1)

    gif[0].save(output, save_all=True,
                optimize=False, append_images=gif[1:], format="GIF",
                loop=0, disposal=2, transparency=0)

    progress_bar.close()


# def convertFramesBlur(video, depth, flags):

#     ret, frame = video.read()

#     if flags['g']:
#         blurred_frame = cv2.GaussianBlur(frame, (151, 151), 0)
#     else:
#         blurred_frame = frame

#     image = Image.fromarray(blurred_frame).convert('L')
#     ascii = frameToAscii(image, c.frame_columns, c.frame_scale, depth)
#     output = asciiToFrame(ascii)

#     return output

#     frame_laplacian = cv2.Laplacian(frame, -1, ksize=5)

#     original = asciiToFrame(original_ascii)
#     average = asciiToFrame(average_ascii)
#     gaussian = asciiToFrame(gaussian_ascii)
#     laplacian = asciiToFrame(laplacian_ascii)

#     original.save(r"./output/originalascii.jpg")

#     picture = plt.figure(figsize=(10, 10))
#     rows = 1
#     columns = 1

#     picture.add_subplot(rows, columns, 1)
#     plt.axis("off")
#     plt.title("Original Ascii")
#     plt.imshow(original)

#     plt.show()


def outputFrame(video, depth, output):
    ret, frame = video.read()
    frame_img = Image.fromarray(frame).convert('L')

    ascii_img = frameToAscii(frame_img, c.frame_columns, c.frame_scale, depth)
    ascii = asciiToFrame(ascii_img)

    ascii.save(r"" + output)
    print("File saved to: " + output)
