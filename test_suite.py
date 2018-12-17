from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual, event, gui
import reading
import cambridge
import illusions
import repetition
import span
import ravens
from test_tools import pause, get_pp_info

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
        [cambridge, 'bikes'],
        [cambridge, 'faces'],
        [cambridge, 'cars'],
        [illusions],
        [repetition, 'word'],
        [repetition, 'pseudoword'],
        [span, 'forward'],
        [span, 'backward'],
        [ravens, 'a'],
        [ravens, 'b']
    ]

    current = check_current()
    for i in range(current, len(experiments)):
        save_current(i)
        pause()
        run_experiment(pp_info, *experiments[i])
    save_current(0)

if __name__ == '__main__':
    run(get_pp_info())
