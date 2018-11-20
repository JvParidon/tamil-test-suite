import reading
import cambridge
import illusions
import ravens
from psychopy import core, visual, event

def pause():
    win = visual.Window((1200, 900), color='black')
    message = visual.TextStim(win, 'Press SPACE to continue', color='white')
    message.draw()
    win.flip()
    key = event.waitKeys(keyList=['space'])
    win.close()

def get_pp_info():
    pp_info = {}
    for key in ['literate', 'number', 'age']:
        pp_info[key] = raw_input('Participant ' + key + ': ')
    return pp_info

def run(pp_info):
    # run experiments in order

    # word reading tamil/english
    reading.Experiment('tamil', pp_info).run()
    reading.Experiment('english', pp_info).run()

    # sp to perceptual learning
    # sp to mirror

    # pause
    pause()

    # cambridge memory tests
    for category in ['bikes', 'faces', 'cars']:
        cambridge.Experiment(category, pp_info).run()

    # pause
    pause()

    # visual illusions
    illusions.Experiment(pp_info).run()

    # word/pseudoword repetition
    repetition.Experiment('word', pp_info).run()
    repetition.Experiment('pseudoword', pp_info).run()

    # digit span forward/backward
    span.Experiment('forward', pp_info).run()
    span.Experiment('backward', pp_info).run()

    # raven's progressive matrices
    ravens.Experiment(pp_info).run()

if __name__ == '__main__':
    run(get_pp_info())
