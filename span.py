import audio
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual
import random
import os

class Experiment(object):


    def __init__(self, mode, pp_info, fps=60.0):
        self.mode = mode
        self.pp_info = pp_info
        self.fps = fps
        # set up file paths, etc.
        self.stimuli_folder = 'stimuli/span/' + mode + '/'
        self.log_prefix = 'logs/span/' + mode + '/' + pp_info['literate'] + '_' + pp_info['number'] + '_'


    def run(self):
        # set up presentation window color, and size
        bgcolor = 'black'
        txtcolor = 'white'
        #self.win = visual.Window(fullscr=True, color=bgcolor)
        self.win = visual.Window((1200, 900), color=bgcolor)  # temporary presentation window setup, exchange for line above when running actual experiment

        random.seed(int(self.pp_info['number']))
        fnames = sorted(os.listdir(self.stimuli_folder))
        random.shuffle(fnames)

        stimuli = [audio.read(self.stimuli_folder + fname) for fname in fnames if fname.endswith('.wav')]

        recordings = []

        for stimulus in stimuli:
            audio.play(stimulus, wait=True)
            recordings += [audio.record((len(stimulus) / 44100.0) + 1, wait=True)]

        for i in range(len(recordings)):
            audio.write(self.log_prefix + fnames[i], recordings[i])

        self.win.close()


if __name__ == '__main__':
    Experiment('forward', {'literate': 'no', 'age': '1', 'number': '1'}).run()
