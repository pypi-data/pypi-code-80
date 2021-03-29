from .scrambler import *

if __name__ == '__main__':
    wca = WCA_Scrambler()
    print(wca.get_wca_scramble(input('Cubetype: ')))