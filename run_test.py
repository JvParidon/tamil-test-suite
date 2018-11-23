from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual, event, gui
import reading
import cambridge
import illusions
import repetition
import span
import ravens

def pause():
    win = visual.Window((1200, 900), color='black')
    message = visual.TextStim(win, '||', color='white')
    message.draw()
    win.flip()
    key = event.waitKeys(keyList=['space'])
    win.close()

def get_pp_info():
    win = visual.Window((1200, 900), color='black')
    message = visual.TextStim(win, color='white')
    pp_info = {
        'literate': '',
        'number': '',
        'age': ''
    }
    for key in sorted(pp_info.keys()):
        waiting = True
        while waiting:
            message.text = key + ': ' + pp_info[key]
            message.draw()
            win.flip()
            keypress = event.waitKeys()
            if keypress[0] == 'return':
                waiting = False
            else:
                pp_info[key] += keypress[0]
    win.close()
    return pp_info

def check_current():
    with open('current', 'r') as currentfile:
        return int(currentfile.read())

def save_current(current):
    with open('current', 'w') as currentfile:
        currentfile.write(str(current))

def run_experiment(pp_info, experiment, condition=False):
    if condition:
        experiment.Experiment(condition, pp_info).run()
    else:
        experiment.Experiment(pp_info).run()

def run(pp_info):

    experiments = [
        [reading, 'tamil'],
        [reading, 'english'],
        # sp to perceptual learning
        # sp to mirror
        [cambridge, 'bikes'],
        [cambridge, 'faces'],
        [cambridge, 'cars'],
        [illusions],
        [repetition, 'word'],
        [repetition, 'pseudoword'],
        [span, 'forward'],
        [span, 'backward'],
        [ravens]
    ]

    current = check_current()
    for i in range(current, len(experiments)):
        save_current(i + 1)
        pause()
        run_experiment(pp_info, *experiments[i])
    save_current(0)

if __name__ == '__main__':
    run(get_pp_info())
