from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual, event, gui

def pause():
    win = visual.Window((1200, 900), color='black')
    message = visual.TextStim(win, '||', color='white')
    message.draw()
    win.flip()
    key = event.waitKeys(keyList=['return', 'escape'])
    if key[0] == 'escape':
        core.quit()
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
