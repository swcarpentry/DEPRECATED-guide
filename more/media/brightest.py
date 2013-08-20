from PIL import Image

pic = Image.open('ngc1333-noao.jpg')

xsize, ysize = pic.size
bx, by, max_val = 0, 0, 0

for x in range(xsize):
    for y in range(ysize):
        r, g, b = pic.getpixel((x, y))
        if r + g + b > max_val:
            bx, by, total = x, y, r + g + b

print (bx, by), total
