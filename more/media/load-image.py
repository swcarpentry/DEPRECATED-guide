from PIL import Image
pic = Image.open('ngc1333-noao.jpg')
pic.format
pic.size
colors = pic.getpixel((0, 0))
