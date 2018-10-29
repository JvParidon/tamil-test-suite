import csv
from psychopy import visual, core, event


class Experiment(object):

    def __init__(self, pp, fps=60.0):
        trials_fname = 'trial_structure/ravens/' + type + '.csv'
        log_fname = 'logs/ravens/' + type + '_' + pp + '.csv'
        self.stimuli_folder = 'stimuli/ravens/' + type + '/'
        #self.win = visual.Window(fullscr=True)
        bgcolor = 'white'
        txtcolor = 'black'
        self.frame_dur = 1.0 / fps
        self.win = visual.Window((1200, 900), color=bgcolor)
        self.clock = core.Clock()
        self.expclock = core.Clock()


if __name__ = '__main__':
    pp_num = raw_input('Participant number: ')
    pp_name = raw_input('Participant name: ')
    pp_age = raw_input('Participant age: ')
    exp = Experiment(pp=pp_num)
