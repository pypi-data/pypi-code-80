import torch 
import copy

class PESG:
    def __init__(self, model=None, a=None, b=None, alpha=None, imratio=0.1, m=1.0, lr=0.1, gamma=500, clip_value=1.0, weight_decay=1e-5, **kwargs):
       
        self.p = imratio
        self.m = m
        self.model = model
        
        self.lr = lr
        self.gamma = gamma
        self.clip_value = clip_value
        self.weight_decay = weight_decay
        
        assert a is not None, 'You are missing variable a!'
        assert b is not None, 'You are missing variable b!'
        assert alpha is not None, 'You are missing variable alpha!'
        self.a = a 
        self.b = b 
        self.alpha = alpha 
    
        self.model_ref = {}
        for name, var in model.state_dict().items(): 
            self.model_ref[name] = torch.empty(var.shape).normal_(mean=0, std=0.01).cuda() 
        self.a_ref = torch.empty(self.a.shape).normal_(mean=0,std=0.01).cuda() 
        self.b_ref = torch.empty(self.b.shape).normal_(mean=0,std=0.01).cuda() 
        
        self.model_acc = copy.deepcopy(model.state_dict()) 
        self.a_acc = self.a.clone().detach().requires_grad_(False)
        self.b_acc = self.b.clone().detach().requires_grad_(False)
        self.T = 0

    def step(self):
        for name, param in self.model.named_parameters(): 
            param.data = param.data - self.lr*( torch.clamp(param.grad.data , -self.clip_value, self.clip_value) + 1/self.gamma*(param.data - self.model_ref[name].data)) - self.lr*self.weight_decay*param.data
            self.model_acc[name].data = self.model_acc[name].data + param.data
        self.a.data = self.a.data - self.lr*(torch.clamp(self.a.grad.data, -self.clip_value, self.clip_value) + 1/self.gamma*(self.a.data - self.a_ref.data))- self.lr*self.weight_decay*self.a.data 
        self.b.data = self.b.data - self.lr*(torch.clamp(self.b.grad.data , -self.clip_value, self.clip_value) + 1/self.gamma*(self.b.data - self.b_ref.data))- self.lr*self.weight_decay*self.b.data 
        self.alpha.data = self.alpha.data + self.lr*(2*(self.m + self.b.data - self.a.data)-2*self.alpha.data)
        self.alpha.data  = torch.clamp(self.alpha.data,  0, 999)
        self.a_acc.data = self.a_acc.data + self.a.data
        self.b_acc.data = self.b_acc.data + self.b.data
        self.T = self.T + 1

    def zero_grad(self):
        self.model.zero_grad()
        self.a.grad = None
        self.b.grad = None
        self.alpha.grad =None
        
    def update_regularizer(self):
        print ('Update Regularizer @ T=%s!'%(self.T))
        for name, param in self.model.named_parameters():
            self.model_ref[name].data = self.model_acc[name].data/self.T
        self.a_ref.data = self.a_acc.data/self.T
        self.b_ref.data = self.b_acc.data/self.T

        # reset
        self.a_acc = self.a.clone().detach().requires_grad_(False)
        self.b_acc = self.b.clone().detach().requires_grad_(False)
        self.model_acc = copy.deepcopy(self.model.state_dict())  
        self.T = 0
        
        
        