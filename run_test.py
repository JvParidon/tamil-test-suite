import ravens
import cambridge
import reading
import illusions

if __name__ == '__main__':
    pp = raw_input('Participant number: ')
    pp_name = raw_input('Participant name: ')
    pp_age = raw_input('Participant age: ')
    reading.Experiment(pp).run()
    for category in ['faces', 'cars', 'bikes']:
        cambridge.Experiment(pp, category).run()
    illusions.Experiment.run()
    ravens.Experiment(pp).run()
