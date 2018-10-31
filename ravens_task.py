import csv
from psychopy import visual, core, event


class Experiment(object):

    def __init__(self, pp, fps=60.0):
        trials_fname = 'trial_structure/ravens/ravens.tsv'
        log_fname = 'logs/ravens/ravens_' + pp + '.tsv'
        self.stimuli_folder = 'stimuli/ravens/'
        #self.win = visual.Window(fullscr=True)
        bgcolor = 'white'
        txtcolor = 'black'
        self.frame_dur = 1.0 / fps
        self.win = visual.Window((1200, 900), color=bgcolor)
        self.clock = core.Clock()
        self.expclock = core.Clock()
        self.title = visual.TextStim(self.win, pos=(0, .8), color=txtcolor)
        self.title.wrapWidth = 1.5
        self.title.setAutoLog()
        self.image = visual.ImageStim(self.win)
        with open(trials_fname, 'rU') as trial_file, open(log_fname, 'w') as log_file:
            trials = csv.DictReader(trial_file, delimiter='\t')
            log_fields = trials.fieldnames + ['keypress', 'RT', 'ACC', 't']
            log = csv.DictWriter(log_file, fieldnames=log_fields, delimiter='\t')
            log.writeheader()
            # do experiment
            for trial in trials:
                self.clock.reset()
                trial = self.present_trial(trial)
                log.writerow(trial)
                if self.expclock.getTime() > 20 * 60.0:
                    core.quit()


    def present_trial(self, trial):
        type = trial['type']
        if type == 'message':
            trial = self.message_trial(trial)
        elif type == 'practice':
            trial = self.practice_trial(trial)
        elif type == 'test':
            trial = self.test_trial(trial)
        else:
            # LOG ERROR using logging module
            print('ERROR: unknown trial type')
        trial['t'] = self.expclock.getTime()
        return trial


    def message_trial(self, trial):
        # present instruction trial
        self.title.text = trial['title']
        self.title.draw()
        self.win.callOnFlip(self.clock.reset)
        self.win.flip()
        keys = event.waitKeys(keyList=['escape'] + trial['keyboard'].split(','), timeStamped=self.clock)
        if keys[0][0] == 'escape':
            core.quit()
        trial['keypress'], trial['RT'] = keys[0]
        self.expclock.reset()
        return trial


    def practice_trial(self, trial):
        # present practice trial
        self.image.image = self.stimuli_folder + trial['picture']
        self.image.draw()
        self.win.callOnFlip(self.clock.reset)
        self.win.flip()
        keys = event.waitKeys(keyList=['escape'] + trial['keyboard'].split(','), timeStamped=self.clock)
        if keys[0][0] == 'escape':
            core.quit()
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == trial['key']:
            trial['ACC'] = 1
        else:
            trial['ACC'] = 0
        return trial

    def test_trial(self, trial):
        # present instruction trial
        self.image.image = self.stimuli_folder + trial['picture']
        self.image.draw()
        self.win.callOnFlip(self.clock.reset)
        self.win.flip()
        keys = event.waitKeys(keyList=['escape'] + trial['keyboard'].split(','), timeStamped=self.clock)
        if keys[0][0] == 'escape':
            core.quit()
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == trial['key']:
            trial['ACC'] = 1
        else:
            trial['ACC'] = 0
        return trial


if __name__ == '__main__':
    pp_num = raw_input('Participant number: ')
    pp_name = raw_input('Participant name: ')
    pp_age = raw_input('Participant age: ')
    exp = Experiment(pp=pp_num)
