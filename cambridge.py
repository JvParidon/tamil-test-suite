import csv
import random
import audio
import os
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual, event
from test_tools import pause, get_pp_info


class Experiment(object):


    def __init__(self, category, pp_info, fps=60.0):
        self.pp_info = pp_info
        self.fps = fps
        self.category = category
        # set up file paths, etc.
        self.trials_fname = 'trial_structure/cambridge/' + category + '.tsv'
        self.log_fname = 'logs/cambridge/' + category + '_' + pp_info['number'] + '_' + pp_info['literate'] + '.tsv'
        self.stimuli_folder = 'stimuli/cambridge/' + category + '_color/'
        self.instructions_folder = 'instructions/cambridge/' + category + '/'


    def run(self):
        # set up presentation window color, and size
        bgcolor = 'black' if self.category != 'cars' else 'white'
        txtcolor = 'white' if self.category != 'cars' else 'black'
        #self.win = visual.Window(fullscr=True, color=bgcolor)
        self.win = visual.Window((1200, 900), color=bgcolor)  # temporary presentation window setup, exchange for line above when running actual experiment

        # set up timing related stuff
        self.frame_dur = 1.0 / self.fps
        self.clock = core.Clock()  # trial timer
        self.expclock = core.Clock()  # whole experiment timer
        # inter trial interval setup
        self.isi = core.StaticPeriod()
        self.isi.start(.5)

        # stimulus presentation boxes for images and text
        self.image = visual.ImageStim(self.win)
        self.text = visual.TextStim(self.win, color=txtcolor)

        # check if participant number has not been previously used
        if os.path.isfile(self.log_fname):
            self.text.text = 'Error: participant number has been used previously,\nplease wait and then retry'
            self.text.draw()
            self.win.flip()
            core.wait(3)
            core.quit()

        # actually run the experiment routines
        with open(self.trials_fname, 'rU') as trial_file, open(self.log_fname, 'w') as log_file:
            # read trial structure
            trials = csv.DictReader(trial_file, delimiter='\t')

            # set up log file
            log_fields = trials.fieldnames + ['keypress', 'RT', 'ACC', 't'] + list(self.pp_info.keys())
            log = csv.DictWriter(log_file, fieldnames=log_fields, delimiter='\t')
            log.writeheader()

            # preload block and instructions
            blocks = {}
            self.instructions = {}
            for trial in trials:
                trial.update(self.pp_info)
                if (trial['trialAudio'] != '') and (trial['trialAudio'] not in self.instructions.keys()):
                    #self.instructions[trial['trialAudio']] = sound.Sound(self.instructions_folder + trial['trialAudio'])
                    self.instructions[trial['trialAudio']] = audio.read(self.instructions_folder + trial['trialAudio'])
                if trial['block'] not in blocks.keys():
                    blocks[trial['block']] = [trial]
                else:
                    blocks[trial['block']].append(trial)

            for i in range(5, 0, -1):
                self.text.text = '+' * (2 * i - 1)
                self.text.draw()
                self.win.flip()
                core.wait(1)

            # present the trials
            random.seed(int(self.pp_info['number']))
            for block_number in sorted(blocks.keys()):
                trials = blocks[block_number]
                if trials[0]['randomize'] == 'yes':
                    random.shuffle(trials)
                for trial in trials:
                    self.clock.reset()  # reset trial clock
                    trial = self.present_trial(trial)  # present the trial
                    trial['t'] = self.expclock.getTime()
                    log.writerow(trial)  # log the trial data

            self.win.close()


    # trial subroutine
    def present_trial(self, trial):
        if trial['stim1'] != '':
            self.image.image = self.stimuli_folder + trial['stim1'] + trial['stimFormat']
            self.image.draw()
        elif trial['text'] != '':
            self.text.text = trial['text']
            self.text.draw()
        self.win.callOnFlip(self.clock.reset)
        self.isi.complete()
        self.win.flip()
        if trial['trialAudio'] != '':
            #self.instructions[trial['trialAudio']].play()
            audio.play(self.instructions[trial['trialAudio']], wait=False)
        if trial['keyboard'] != '':
            keys = event.waitKeys(keyList=['escape'] + trial['keyboard'].split(' '), timeStamped=self.clock)
            trial['keypress'], trial['RT'] = keys[0]
            if trial['keypress'] == 'escape':
                core.quit()
            if trial['keypress'] == trial['key']:
                trial['ACC'] = 1
            else:
                trial['ACC'] = 0
            if trial['trialAudio'] != '':
                #self.instructions[trial['trialAudio']].stop()
                audio.stop()
        else:
            if trial['presTime'] != '':
                core.wait(float(trial['presTime']) / 1000 - self.frame_dur)
            elif trial['trialAudio'] != '':
                core.wait(len(self.instructions[trial['trialAudio']]) / 44100.0)
                #core.wait(self.instructions[trial['trialAudio']].getDuration())
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial


if __name__ == '__main__':
        pp_info = get_pp_info()
        for mode in ['bikes', 'faces', 'cars']:
            pause()
            Experiment(mode, pp_info).run()
