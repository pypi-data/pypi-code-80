from __future__ import print_function
import time


__all__ = ['Data', 'State', 'StateMachine']


class Data(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class State:

    def __init__(self):
        pass

    def run(self, sm):
        sm.end()


class StateMachine:

    def __init__(self, state=State(), data=Data(), freq=10, run_before=None, run_after=None):
        self.state = state
        self.data = data
        self.freq = freq
        self.enabled = False

        self.run_before = run_before
        self.run_after = run_after

    def run(self):
        if self.run_before is not None:
            self.run_before(self)

        self.state.run(self)

        if self.run_after is not None:
            self.run_after(self)

    def begin(self):
        if not self.enabled:
            print('begin ...')
            self.enabled = True
            while self.enabled:
                t = time.time()
                self.run()
                dt = time.time() - t
                if dt < 1 / self.freq:
                    time.sleep(1 / self.freq - dt)

    def end(self):
        if self.enabled:
            print('end ...')
            self.enabled = False

    def set(self, state):
        print('{}: {} --> {}'.format(time.asctime(time.localtime()), self.state.__class__.__name__,
                                     state.__class__.__name__))
        self.state = state
