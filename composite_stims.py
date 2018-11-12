import csv
from PIL import Image

with open('trial_structure/cambridge/bikes.csv', 'rU') as trial_file:
    trials = csv.DictReader(trial_file)

    for trial in trials:
        if trial['stim3'] != '':
            im1 = Image.open('stimuli/cambridge/bikes/' + trial['stim1'] + trial['stimFormat']).resize((400, 400), Image.BICUBIC)
            im2 = Image.open('stimuli/cambridge/bikes/' + trial['stim2'] + trial['stimFormat']).resize((400, 400), Image.BICUBIC)
            im3 = Image.open('stimuli/cambridge/bikes/' + trial['stim3'] + trial['stimFormat']).resize((400, 400), Image.BICUBIC)

            im = Image.new('RGB', (1200, 400))
            im.paste(im1, (0, 0))
            im.paste(im2, (400, 0))
            im.paste(im3, (800, 0))
            print(trial['trialNo'] + '.jpg')
            im.save(trial['trialNo'] + '.jpg')
