from time import time
from PIL import Image

def faster(picture):
    max_val = 0
    for (r, g, b) in picture.getdata():
        if r + g + b > max_val:
            max_val = r + g + b
    return max_val

def elapsed(func, picture):
   start = time()
   result = func(picture)
   return time() - start, result

pic = Image.open('ngc1333-noao.jpg')
print elapsed(faster, pic)
