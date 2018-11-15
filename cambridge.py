import csv
import random
#import soundfile as sf
#import sounddevice as sd
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual, event, sound
print(sound.Sound)


class Experiment(object):


    def __init__(self, pp, category, fps=60.0):
        self.pp = pp
        self.fps = fps
        self.category = category
        # set up file paths, etc.
        self.trials_fname = 'trial_structure/cambridge/' + category + '.csv'
        self.log_fname = 'logs/cambridge/' + category + '_' + pp + '.csv'
        self.stimuli_folder = 'stimuli/cambridge/' + category + '/'
        self.instructions_folder = 'instructions/cambridge/' + category + '/'


    def run(self):
        # set up presentation window color, and size
        bgcolor = 'black' if category != 'cars' else 'white'
        txtcolor = 'white' if category != 'cars' else 'black'
        #self.win = visual.Window(fullscr=True, color=bgcolor)
        self.win = visual.Window((1200, 900), color=bgcolor)  # temporary presentation window setup, exchange for line above when running actual experiment

        # set up timing related stuff
        self.frame_dur = 1.0 / self.fps
        self.clock = core.Clock()  # trial timer
        self.expclock = core.Clock()  # whole experiment timer
        # inter trial interval setup
        self.isi = core.StaticPeriod()
        self.isi.start(.5)

        # set sound defaults
        #sd.default.samplerate = 44100
        #sd.default.channels = 2

        # various stimulus presentation boxes for text and images
        self.message = visual.TextStim(self.win, color=txtcolor)
        self.message.wrapWidth = 1.5
        self.title = visual.TextStim(self.win, pos=(0, .8), color=txtcolor)
        self.title.wrapWidth = 1.5
        self.image = visual.ImageStim(self.win)

        # actually run the experiment routines
        with open(self.trials_fname, 'rU') as trial_file, open(self.log_fname, 'w') as log_file:
            # read trial structure
            trials = csv.DictReader(trial_file)

            # set up log file
            log_fields = trials.fieldnames + ['keypress', 'RT', 'ACC', 't']
            log = csv.DictWriter(log_file, fieldnames=log_fields)
            log.writeheader()

            # preload block and instructions
            blocks = {}
            self.instructions = {}
            for trial in trials:
                if (trial['trialAudio'] != '') and (trial['trialAudio'] not in self.instructions.keys()):
                    self.instructions[trial['trialAudio']] = sound.Sound(self.instructions_folder + trial['trialAudio'])
                if trial['block'] not in blocks.keys():
                    blocks[trial['block']] = [trial]
                else:
                    blocks[trial['block']].append(trial)

            # present the trials
            random.seed(self.pp)
            for block_number in sorted(blocks.keys()):
                trials = blocks[block_number]
                if trials[0]['randomize'] == 'yes':
                    random.shuffle(trials)
                for trial in trials:
                    self.clock.reset()  # reset trial clock
                    trial = self.present_trial(trial)  # present the trial
                    log.writerow(trial)  # log the trial data


    # select the appriopriate trial subroutine
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
            # unknown trial type, return some kind of error?
            print('ERROR: unknown trial type')

        # log experiment timer and return trial data
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
        if trial['trialAudio'] != '':
            self.instructions[trial['trialAudio']].play()
        keys = event.waitKeys(keyList=['escape'] + trial['button1'].split(' '), timeStamped=self.clock)
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == 'escape':
            core.quit()
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
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == 'escape':
            core.quit()
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
        print(trial['stim1'])
        self.image.draw()
        self.title.text = trial['trialText']
        self.title.draw()
        self.win.callOnFlip(self.clock.reset)
        self.isi.complete()
        self.win.flip()
        keys = event.waitKeys(keyList=['escape'] + trial['keyboard'].split(' '), timeStamped=self.clock)
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == 'escape':
            core.quit()
        if trial['keypress'] == trial['key']:
            trial['ACC'] = 1
        else:
            trial['ACC'] = 0
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial


if __name__ == '__main__':
    category_selected = False
    while category_selected is False:
        category = raw_input('What category of picture recognition do you want to test? (faces, cars, or bikes)\n')
        if category in ['faces', 'cars', 'bikes']:
            category_selected = True
        else:
            print(category + ' is not a valid picture category, try again')
    pp = raw_input('Participant number: ')
    pp_name = raw_input('Participant name: ')
    pp_age = raw_input('Participant age: ')
    Experiment(pp, category).run()
