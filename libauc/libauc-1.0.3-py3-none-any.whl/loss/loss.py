import torch 
import torch.nn.functional as F

class AUCMLoss:
    def __init__(self, m=1.0, imratio=0.1):
        self.m = m
        self.p = imratio
        self.a = torch.zeros(1, dtype=torch.float32, device="cuda", requires_grad=True).cuda()
        self.b = torch.zeros(1, dtype=torch.float32, device="cuda", requires_grad=True).cuda()
        self.alpha = torch.zeros(1, dtype=torch.float32, device="cuda", requires_grad=True).cuda()
        
    def __call__(self, y_pred, y_true):
        loss = (1-self.p)*torch.mean((y_pred - self.a)**2*(1==y_true).float()) + \
                    self.p*torch.mean((y_pred - self.b)**2*(-1==y_true).float())   + \
                    2*self.alpha*(self.p*(1-self.p)*self.m + \
                    torch.mean((self.p*y_pred*(-1==y_true).float() - (1-self.p)*y_pred*(1==y_true).float())) )- \
                    self.p*(1-self.p)*self.alpha**2
        return loss
    
class CELoss:
    def __init__(self):
        self.criterion = F.binary_cross_entropy_with_logits 

    def __call__(self, y_pred, y_true):
        # loss is with sigmoid
        return self.criterion(y_pred, y_true)