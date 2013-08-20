from time import time
from PIL import Image

def inbetween(picture):
    xsize, ysize = picture.size
    temp = picture.load()
    bx, by, max_val = 0, 0, 0
    for x in range(xsize):
        for y in range(ysize):
            r, g, b = temp[x, y]
            if r + g + b > max_val:
                bx, by, total = x, y, r + g + b
    return (bx, by), total

def elapsed(func, picture):
   start = time()
   result = func(picture)
   return time() - start, result

pic = Image.open('ngc1333-noao.jpg')
print elapsed(inbetween, pic)
