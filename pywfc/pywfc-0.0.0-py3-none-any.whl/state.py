import random
from .rule import Rule


class State:
    def __init__(self, identifier: str, rule: Rule):
        self.name = identifier
        self.rule = rule

    def rulecheck(self, wave, xy, constrain = False):
        return self.rule.check(wave, xy, constrain)


class Potential:
    def __init__(self, states):
        self.states = states
        self.state = None

    def constrain(self, states):
        self.states = states

    def count(self, wave, xy):
        return len([
            x for x in self.states if x.rulecheck(wave, xy)
        ]) if self.state is None else False

    def collapse(self, wave, xy):
        self.state = random.choice([
            x for x in self.states if x.rulecheck(wave, xy)
        ])
        self.state.rulecheck(wave, xy, True)
