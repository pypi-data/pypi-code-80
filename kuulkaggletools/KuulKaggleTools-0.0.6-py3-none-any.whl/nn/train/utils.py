import torch
from torch import nn

class ExtractionLayer(nn.Module):

    def __init__(self,fn : callable = lambda x : x):
        super(self.__class__,self).__init__()
        self.fn = fn

    def forward(self,*args,**kwargs):return self.fn( *args, **kwargs )