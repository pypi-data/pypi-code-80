

class visdom_torch:
    def __init__(self, plot, update = 'reduce'):
#        assert isinstance(plot,type(Visdom().line)), "visdom.Visdom must be instantiated"
        self.plot = plot
        self.update = update
        self.win = None
    def __call__(self,**args):
        if not self.win:
            self.win = self.plot(**args)
        else:
            self.plot(**args,win = self.win, update = self.update,)
            

