import numpy as np
import constants as c
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Get the average luminance value of a given image
# References:


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

def frameToAscii(frame, cols, scale):
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
            gsval = c.gscale[int((avg * c.depth) / 255)]

            # Add resulting key to ascii array
            ascii[i] += gsval

    return ascii


# Apply generated ascii text onto newly created image
# References:

def asciiToFrame(ascii):
    # Accessing font for ascii image
    font = ImageFont.truetype(c.font_path, c.font_size)

    # Creating a scaffold image
    img = Image.new(mode="RGB", size=(c.scaffold_w, c.scaffold_h))

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


# Add created ascii images together into playable gif and output the file
# References:
# Input (frames):
#   frames: VideoFrame (output from asciiToFrame(ascii))


def createGif(frames):
    gif = []
    for i in frames:
        gif.append(i.convert("P", palette=Image.ADAPTIVE))

    gif[0].save(c.output_file_path, save_all=True,
                optimize=False, append_images=gif[1:], loop=0)


