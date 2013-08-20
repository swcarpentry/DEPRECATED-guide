import sys
import Image

def monochrome(picture, threshold):
    '''Convert an image to black and white.'''

    black = (  0,   0,   0)
    white = (255, 255, 255)
    xsize, ysize = picture.size
    temp = picture.load()

    for x in range(xsize):
        for y in range(ysize):
            r, g, b = temp[x, y]
            if r + g + b >= threshold:
                temp[x, y] = black
            else:
                temp[x, y] = white

if __name__ == '__main__':
    pic = Image.open(sys.argv[1])
    monochrome(pic, 200 + 200 + 200)
    pic.save(sys.argv[2])
