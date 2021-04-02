import torch 

class SGD:
    def __init__(self, model=None, lr=0.1, weight_decay=1e-5, clip_value=1.0, **kwargs):
        self.lr = lr
        self.weight_decay = weight_decay
        self.clip_value = clip_value
        self.model = model
        assert model is not None, 'You need to pass model to optimizer!'
        
    def step(self):
        for name, param in self.model.named_parameters(): 
            param.data = param.data - self.lr*( torch.clamp(param.grad.data , -self.clip_value, self.clip_value)) - self.lr*self.weight_decay*param.data

    def zero_grad(self):
        self.model.zero_grad()
