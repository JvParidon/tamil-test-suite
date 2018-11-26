from PIL import Image, ImageDraw
import os

green = (29, 183, 121)
yellow = (255, 242, 0)
blue = (63, 71, 205)
red = (228, 37, 65)

def add_color(im, coords, color, dot=False):
    factor = 4  # for smoothing
    box_size = 30
    width, height = im.size
    im = im.resize((width * factor, height * factor), Image.BICUBIC)
    draw = ImageDraw.Draw(im)
    box = ((coords[0] - (box_size / 2))  * factor,
           (coords[1] - (box_size / 2)) * factor,
           (coords[0] + (box_size / 2)) * factor,
           (coords[1] + (box_size / 2)) * factor)
    halfbox = ((coords[0] - (box_size / 4))  * factor,
               (coords[1] - (box_size / 4)) * factor,
               (coords[0] + (box_size / 4)) * factor,
               (coords[1] + (box_size / 4)) * factor)
    draw.ellipse(box, fill=color)
    if dot:
        draw.ellipse(halfbox, fill='black')
    im = im.resize((width, height), Image.BICUBIC)
    return im

'''
# faces routine
folder = 'stimuli/cambridge/faces_color/'
for fname in sorted(os.listdir(folder)):
    if fname.endswith('.jpg'):
        im = Image.open(folder + fname).convert('RGB')
        width, height = im.size
        thirds = [width / 6, width / 2, width / 6 * 5]
        im = add_color(im, (thirds[0], height - 30), green)
        im = add_color(im, (thirds[1], height - 30), yellow)
        im = add_color(im, (thirds[2], height - 30), blue)
        im.save(folder + fname, quality=95)
'''
'''
# bikes routine
folder = 'stimuli/cambridge/bikes_color/'
for fname in sorted(os.listdir(folder)):
    if fname.endswith('.jpg'):
        im = Image.open(folder + fname).convert('RGB')
        width, height = im.size
        thirds = [width / 6, width / 2, width / 6 * 5]
        im = add_color(im, (thirds[0], height - 30), green)
        im = add_color(im, (thirds[1], height - 30), yellow)
        im = add_color(im, (thirds[2], height - 30), blue)
        im.save(folder + fname, quality=95)
'''
'''
# cars routine
folder = 'stimuli/cambridge/cars_color/'
for fname in sorted(os.listdir(folder)):
    if fname.endswith('.jpg'):
        im = Image.open(folder + fname).convert('RGB')
        width, height = im.size
        thirds = [height / 6, height / 2, height / 6 * 5]
        stagger = [0, width / 5, width / 5 * 2]
        im = add_color(im, (30 + stagger[0], thirds[0]), green)
        im = add_color(im, (30 + stagger[1], thirds[1]), yellow)
        im = add_color(im, (30 + stagger[2], thirds[2]), blue)
        im.save(folder + fname, quality=95)
'''
folder = 'stimuli/ravens/'
for fname in sorted(os.listdir(folder)):
    if fname.endswith('.jpg'):
        im = Image.open(folder + fname).convert('RGB')
        im = im.resize((600, 800), Image.BICUBIC)
        width, height = im.size
        spots = [100, 200, 400, 500]
        im = add_color(im, (spots[0], 80), green)
        im = add_color(im, (spots[1], 80), yellow)
        im = add_color(im, (spots[2], 80), blue)
        im = add_color(im, (spots[3], 80), red)
        im = add_color(im, (spots[0], 40), green, dot=True)
        im = add_color(im, (spots[1], 40), yellow, dot=True)
        im = add_color(im, (spots[2], 40), blue, dot=True)
        im = add_color(im, (spots[3], 40), red, dot=True)
        im.save('stimuli/ravens_color/' + fname, quality=95)
