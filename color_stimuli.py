from PIL import Image, ImageDraw
import os

def add_color(im, coords, color):
    draw = ImageDraw.Draw(im)
    box = (coords[0], coords[1], coords[0] + 50, coords[1] + 50)
    draw.ellipse(box, fill=color)
    return im

# ravens routine
folder = 'stimuli/ravens/'
for fname in sorted(os.listdir(folder))[0:2]:
    if fname.endswith('.jpg'):
        im = Image.open(folder + fname).convert('RGB')
        im = im.resize((600, 800), Image.BICUBIC)
        im = add_color(im, (0, 0), 'red')
        im.show()
