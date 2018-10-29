import csv
from psychopy import visual, core, event


class Experiment(object):

    def __init__(self, type, pp, fps=60.0):
        trials_fname = 'trial_structure/cambridge/' + type + '.csv'
        log_fname = 'logs/cambridge/' + type + '_' + pp + '.csv'
        self.stimuli_folder = 'stimuli/cambridge/' + type + '/'
        #self.win = visual.Window(fullscr=True)
        bgcolor = 'black' if type != 'cars' else 'white'
        txtcolor = 'white' if type != 'cars' else 'black'
        self.frame_dur = 1.0 / fps
        self.win = visual.Window((1200, 900), color=bgcolor)
        self.clock = core.Clock()
        self.expclock = core.Clock()
        self.isi = core.StaticPeriod()
        self.isi.start(.5)
        self.message = visual.TextStim(self.win, color=txtcolor)
        self.message.setAutoLog()
        self.message.wrapWidth = 1.5
        self.title = visual.TextStim(self.win, pos=(0, .8), color=txtcolor)
        self.title.wrapWidth = 1.5
        self.title.setAutoLog()
        self.image = visual.ImageStim(self.win)
        with open(trials_fname, 'rU') as trial_file, open(log_fname, 'w') as log_file:
            trials = csv.DictReader(trial_file)
            log_fields = trials.fieldnames + ['keypress', 'RT', 'ACC', 't']
            log = csv.DictWriter(log_file, fieldnames=log_fields)
            log.writeheader()
            # do experiment
            for trial in trials:
                self.clock.reset()
                trial = self.present_trial(trial)
                log.writerow(trial)

    def present_trial(self, trial):
        type = trial['type']
        if type == 'instructions':
            trial = self.instruction_trial(trial)
        elif type == 'learn':
            trial = self.learn_trial(trial)
        elif type == 'practice':
            trial = self.practice_trial(trial)
        elif type == 'test':
            trial = self.test_trial(trial)
        else:
            # LOG ERROR using logging module
            print('ERROR: unknown trial type')
        trial['t'] = self.expclock.getTime()
        return trial

    def instruction_trial(self, trial):
        # present instruction trial
        self.title.text = trial['title']
        self.title.draw()
        self.message.text = trial['content'].replace('<br>', '\n')
        self.message.draw()
        self.win.callOnFlip(self.clock.reset)
        self.isi.complete()
        self.win.flip()
        keys = event.waitKeys(keyList=['escape'] + trial['button1'].split(' '), timeStamped=self.clock)
        if keys[0][0] == 'escape':
            core.quit()
        trial['keypress'], trial['RT'] = keys[0]
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial

    def learn_trial(self, trial):
        # present learn trial
        # set up trial display
        self.image.image = self.stimuli_folder + trial['stim1'] + trial['stimFormat']
        self.image.draw()
        self.title.text = trial['trialText']
        self.title.draw()
        #self.win.callOnFlip(self.clock.reset)
        # run out ISI clock
        self.isi.complete()
        # flip frame buffer and reset trial clock
        self.win.flip()
        # wait for prespecified duration while stimulus is on screen
        core.wait(float(trial['presTime']) / 1000 - self.frame_dur)
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial

    def practice_trial(self, trial):
        # present practice trial
        self.image.image = self.stimuli_folder + trial['stim1'] + trial['stimFormat']
        self.image.draw()
        self.title.text = trial['trialText']
        self.title.draw()
        self.win.callOnFlip(self.clock.reset)
        self.isi.complete()
        self.win.flip()
        keys = event.waitKeys(keyList=['escape'] + trial['keyboard'].split(' '), timeStamped=self.clock)
        if keys[0][0] == 'escape':
            core.quit()
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == trial['key']:
            trial['ACC'] = 1
        else:
            trial['ACC'] = 0
            self.message.text = trial['feedbackIncorrect']
            self.message.draw()
            self.win.callOnFlip(self.clock.reset)
            self.win.flip()
            core.wait(3.0 - self.frame_dur)
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial

    def test_trial(self, trial):
        # present instruction trial
        self.image.image = self.stimuli_folder + trial['stim1'] + trial['stimFormat']
        self.image.draw()
        self.title.text = trial['trialText']
        self.title.draw()
        self.win.callOnFlip(self.clock.reset)
        self.isi.complete()
        self.win.flip()
        keys = event.waitKeys(keyList=['escape'] + trial['keyboard'].split(' '), timeStamped=self.clock)
        if keys[0][0] == 'escape':
            core.quit()
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == trial['key']:
            trial['ACC'] = 1
        else:
            trial['ACC'] = 0
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial


if __name__ == '__main__':
    type_selected = False
    while type_selected is False:
        exp_type = raw_input('What type of picture recognition do you want to test? (faces, cars, or bikes)\n')
        if exp_type in ['faces', 'cars', 'bikes']:
            type_selected = True
        else:
            print(exp_type + ' is not a valid picture type, try again')
    pp_num = raw_input('Participant number: ')
    pp_name = raw_input('Participant name: ')
    pp_age = raw_input('Participant age: ')
    exp = Experiment(type=exp_type, pp=pp_num)
