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
        self.log_fname = 'logs/reading/' + mode + '_' + pp_info['number'] + '_' + pp_info['literate'] + '.wav'


    def run(self):
        # set up presentation window color, and size
        bgcolor = 'black'
        txtcolor = 'white'
        #self.win = visual.Window(fullscr=True, color=bgcolor)
        self.win = visual.Window((1200, 900), color=bgcolor)  # temporary presentation window setup, exchange for line above when running actual experiment
        #microphone.switchOn()
        #self.mic = microphone.AdvAudioCapture(filename=self.log_fname)
        self.text = visual.TextStim(self.win, color=txtcolor)

        for i in range(5, 0, -1):
            self.text.setText('+' * (2 * i - 1))
            self.text.draw()
            self.win.flip()
            core.wait(1)

        self.text.setText('READ')  # replace with spoken instruction
        self.text.draw()
        self.win.flip()
        # record
        samples = audio.record(60, wait=True)

        self.text.setText('STOP')  # replace with spoken instruction
        self.text.draw()
        self.win.flip()
        audio.write(self.log_fname, samples)
        core.wait(3)


        self.win.close()


if __name__ == '__main__':
    Experiment('tamil', {'literate': 'no', 'age': '1', 'number': '1'}).run()
