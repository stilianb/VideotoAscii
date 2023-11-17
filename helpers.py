import numpy as np
import constants as c
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def getAverageLuminance(image):
    img = np.array(image)
    w, h = img.shape
    return np.average(img.reshape(w*h))


def frameToAscii(frame, cols, scale):
    W, H = frame.size[0], frame.size[1]

    width = W/cols
    height = width / scale
    rows = int(H/height)

    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    ascii = []
    for i in range(rows):
        y1 = int(i*height)
        y2 = int((i+1)*height)

        if i == rows-1:
            y2 = H

        ascii.append("")

        for j in range(cols):
            x1 = int(j*width)
            x2 = int((j+1)*width)

            if j == cols-1:
                x2 = W

            ascii_img = frame.crop((x1, y1, x2, y2))
            avg = int(getAverageLuminance(ascii_img))

            gsval = c.gscale[int((avg*9)/255)]
            ascii[i] += gsval

    return ascii


def asciiToFrame(ascii):
    font = ImageFont.truetype("./fonts/FreeMono.ttf", 34)

    img = Image.new(mode="RGB", size=(1920, 1080))
    img_draw = ImageDraw.Draw(img)

    y = 0
    for i in ascii:
        x = 0
        for j in i:
            img_draw.text((x, y), j, font=font, fill=(255, 255, 255))
            x += 10
        y += 20
    return img


def createGif(frames):
    gif = []
    for i in frames:
        gif.append(i.convert("P", palette=Image.ADAPTIVE))

    gif[0].save('./output/temp_result.gif', save_all=True,
                optimize=False, append_images=gif[1:], loop=0)
