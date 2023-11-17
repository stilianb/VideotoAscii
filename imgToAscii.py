from io import BytesIO
import numpy as np
import math
import cv2
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib import cm
from array import array
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#img = Image.open('./circles.jpg').convert('L')
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '


def getAverageLuminance(image):
    img = np.array(image)
    w, h = img.shape
    return np.average(img.reshape(w*h))


def convertImageToAscii(image, cols, scale, moreLevels):
    global gscale1, gscale2
    W, H = image.size[0], image.size[1]

    width = W/cols
    height = width/scale

    rows = int(H/height)

    #print("cols: %d, rows: %d" % (cols, rows))
    #print("tile dims: %d x %d" % (width, height))

    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    asciiImg = []

    for i in range(rows):
        y1 = int(i*height)
        y2 = int((i+1)*height)

        if i == rows-1:
            y2 = H

        asciiImg.append("")

        for j in range(cols):
            x1 = int(j*width)
            x2 = int((j+1)*width)

            if i == cols-1:
                x2 = W

            newImg = image.crop((x1, y1, x2, y2))
            avg = int(getAverageLuminance(newImg))

            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]

            asciiImg[i] += gsval

    return asciiImg


def create_new_img(ascii):
    font = ImageFont.truetype("FreeMono.ttf", 34)

    newImg = Image.new(mode="RGB", size=(1920, 1080))
    newImgDraw = ImageDraw.Draw(newImg)
    
    y = 0
    for i in ascii:
        x = 0
        for j in i:
            newImgDraw.text((x, y), j, font=font, fill=(255, 255, 255))
            x += 10
        y += 20
    return newImg

def main():

    #ascii = convertImageToAscii(img, 100, 0.43, False)

    
    cap = cv2.VideoCapture('sample.qt')
    count = 0
    test = []
    control = True
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            control == False
            break
        imgFrame = Image.fromarray(frame).convert('L')
        ascii = convertImageToAscii(imgFrame, 101, 0.43, False)
        converted_image = create_new_img(ascii)
        test.append(converted_image)
        count = count + 1 
        print(count)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        # if count == 10: break

    gif = []
    for i in test:
        gif.append(i.convert("P",palette=Image.ADAPTIVE))

    gif[0].save('temp_result.gif', save_all=True,optimize=False, append_images=gif[1:], loop=0)


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
