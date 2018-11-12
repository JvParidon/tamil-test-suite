import sounddevice as sd
import soundfile as sf

# basic setup for audio recording with sounddevice
sd.default.samplerate = 48000
sd.default.channels = 1

def record(duration, wait=True):
    samples = sd.rec(int(duration * sd.default.samplerate))
    if wait is True:
        sd.wait()
    return samples

def play(samples, wait=True):
    sd.play(samples)
    if wait is True:
        sd.wait()

def read(fname):
    samples, _ = sf.read(fname)
    return samples

def write(fname, samples):
    sf.write(fname, samples, sd.default.samplerate)

if __name__ == '__main__':
    print('recording')
    samples = record(5)
    print('playing')
    play(samples)
    write('sftest.wav', samples)
