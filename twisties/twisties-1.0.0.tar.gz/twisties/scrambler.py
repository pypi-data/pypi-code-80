import pickle
from os import path

pickles = path.join(path.dirname(path.realpath(__file__)), 'pickles')

class WCA_Scrambler:
    def __init__(self):
        self.scrambles = {
            '2x2': Scramble2x2(),
            '3x3': Scramble3x3(),
            '4x4': Scramble4x4(),
            '5x5': Scramble5x5(),
            '6x6': Scramble6x6(),
            '7x7': Scramble7x7(),
            'sqn': ScrambleSqn(),
            'mgm': ScrambleMgm(),
            'skb': ScrambleSkb(),
            'pyr': ScramblePyr(),
            'clk': ScrambleClk()}

    def get_wca_scramble(self, cubetype='3x3'):
        return self.scrambles[cubetype].get_wca_scramble()

class Scramble2x2:
    def __init__(self):
        with open(path.join(pickles, 'scrambler222.pkl'), 'rb') as input:
            self.scr = pickle.load(input)

    def get_wca_scramble(self):
        return self.scr.call("scramble_222.getRandomScramble")

class Scramble3x3:
    def __init__(self):
        with open(path.join(pickles, 'scrambler333.pkl'), 'rb') as input:
            self.scr = pickle.load(input)
    
    def get_wca_scramble(self):
        return self.scr.call("scramble_333.getRandomScramble")

class Scramble4x4:
    def __init__(self):
        with open(path.join(pickles, 'scrambler444.pkl'), 'rb') as input:
            self.scr = pickle.load(input)
    
    def get_wca_scramble(self):
        return self.scr.call("scramble_444.getRandomScramble")

class Scramble5x5:
    def __init__(self):
        with open(path.join(pickles, 'mega_scrambler.pkl'), 'rb') as input:
            self.scr = pickle.load(input)
    
    def get_wca_scramble(self):
        return self.scr.call("megaScrambler.get555WCAScramble", 60)

class Scramble6x6:
    def __init__(self):
        with open(path.join(pickles, 'mega_scrambler.pkl'), 'rb') as input:
            self.scr = pickle.load(input)
    
    def get_wca_scramble(self):
        return self.scr.call("megaScrambler.get666WCAScramble", 80)

class Scramble7x7:
    def __init__(self):
        with open(path.join(pickles, 'mega_scrambler.pkl'), 'rb') as input:
            self.scr = pickle.load(input)
    
    def get_wca_scramble(self):
        return self.scr.call("megaScrambler.get777WCAScramble", 100)

class ScrambleSqn:
    def __init__(self):
        with open(path.join(pickles, 'sq1.pkl'), 'rb') as input:
            self.scr = pickle.load(input)
    
    def get_wca_scramble(self):
        return self.scr.call("sql_scrambler.getRandomScramble").replace('/', ' / ')

class ScrambleMgm:
    def __init__(self):
        with open(path.join(pickles, 'util_scrambler.pkl'), 'rb') as input:
            self.scr = pickle.load(input)
    
    def get_wca_scramble(self):
        return self.scr.call("util_scramble.getMegaminxWCAScramble", 70).replace('\n','').replace('  ',' ').replace('  ',' ')
    
    def get_carrot_scramble(self):
        return self.scr.call("util_scramble.getMegaminxCarrotScramble", 70).replace('\n','').replace('  ',' ').replace('  ',' ')

    def get_old_style_scramble(self):
        return self.scr.call("util_scramble.getMegaminxOldStyleScramble", 70)

class ScrambleSkb:
    def __init__(self):
        with open(path.join(pickles, 'skewb.pkl'), 'rb') as input:
            self.scr = pickle.load(input)

    def get_wca_scramble(self):
        return self.scr.call("skewb_scrambler.getSkewbWCAScramble")

class ScramblePyr:
    def __init__(self):
        with open(path.join(pickles, 'pyra.pkl'), 'rb') as input:
            self.scr = pickle.load(input)

    def get_wca_scramble(self):
        return self.scr.call("pyra_scrambler.getPyraWCAScramble")

class ScrambleClk:
    def __init__(self):
        with open(path.join(pickles, 'util_scrambler.pkl'), 'rb') as input:
            self.scr = pickle.load(input)

    def get_wca_scramble(self):
        return self.scr.call("util_scramble.getClockWCAScramble")