import audio
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual
import random
import os
import csv


class Experiment(object):


    def __init__(self, mode, pp_info, fps=60.0):
        self.mode = mode
        self.pp_info = pp_info
        self.fps = fps
        # set up file paths, etc.
        self.stimuli_folder = 'stimuli/span/' + mode + '/'
        self.trials_fname = 'trial_structure/span/' + mode + '.tsv'
        self.log_prefix = 'logs/span/' + mode + '/' + pp_info['literate'] + '_' + pp_info['number'] + '_'


    def run(self):
        # set up presentation window color, and size
        bgcolor = 'black'
        txtcolor = 'white'
        #self.win = visual.Window(fullscr=True, color=bgcolor)
        self.win = visual.Window((1200, 900), color=bgcolor)  # temporary presentation window setup, exchange for line above when running actual experiment

        with open(self.trials_fname, 'rU') as trial_file:
            # read trial structure
            trials = csv.DictReader(trial_file, delimiter='\t')

            # preload stimuli
            stimuli = [audio.read(self.stimuli_folder + trial['stimulus']) for trial in trials]

            recordings = []

            for stimulus in stimuli:
                audio.play(stimulus, wait=True)
                recordings += [audio.record((len(stimulus) / 44100.0) + 1, wait=True)]

            for i in range(len(recordings)):
                audio.write(self.log_prefix + trials[i]['stimulus'], recordings[i])

            self.win.close()


if __name__ == '__main__':
    Experiment('forward', {'literate': 'no', 'age': '1', 'number': '1'}).run()
