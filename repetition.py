import audio
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual

# experiment routines for presenting word reading stimuli and recording spoken responses

class Experiment(object):


    def __init__(self, mode, pp_info, fps=60.0):
        self.mode = mode
        self.pp_info = pp_info
        self.fps = fps
        # set up file paths, etc.
        self.stimuli_prefix = 'stimuli/repetition/' + mode + '/' + mode
        self.log_prefix = 'logs/repetition/' + mode + '/' + pp_info['literate'] + '_' + pp_info['number'] + '_' + mode


    def run(self):
        # set up presentation window color, and size
        bgcolor = 'black'
        txtcolor = 'white'
        #self.win = visual.Window(fullscr=True, color=bgcolor)
        self.win = visual.Window((1200, 900), color=bgcolor)  # temporary presentation window setup, exchange for line above when running actual experiment

        words = [audio.read(self.stimuli_prefix + str(i + 1) + '.wav') for i in range(24)]
        recordings = []

        for word in words:
            audio.play(word, wait=True)
            recordings += [audio.record(((len(word) / 44100) + 1), wait=True)]

        for i in range(24):
            audio.write(self.log_prefix + str(i + 1) + '.wav', recordings[i])

        self.win.close()


if __name__ == '__main__':
    Experiment('word', {'literate': 'no', 'age': '1', 'number': '1'}).run()
