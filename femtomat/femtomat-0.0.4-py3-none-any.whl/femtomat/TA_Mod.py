import numpy as np
import matplotlib.pyplot as plt

class TA:
    def __init__(self, TA, time, wave):
        if time.shape[0] < wave.shape[0]:
            if TA.shape[0] == wave.shape[0]:
                self.TA   = svd_reconstruction_E15(TA,k_opt(TA))
            else:
                self.TA   = svd_reconstruction_E15(TA.T,k_opt(TA.T))
        else:
            self.TA = TA
        self.time = time
        self.wave = wave
        self.u, self.s, self.vh = np.linalg.svd(self.TA, full_matrices=False)
        
    def nearest(self,array, value): 
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx
    
    def plot(self, times = None, norm = False, title = None, ylim = None, norm_at = None, norm_flip = False):
        if not times:
            times = np.asarray([1500,1000,500,100,50,10,5,1,0.2])
        color=plt.cm.rainbow(np.linspace(0,1,len(times)))
        if title:
            plt.title(title, fontsize=15)
        for t,c in zip(times,color):
            norm_factor = 1
            if norm:
                if norm_at:
                    norm_factor = 1/self.TA[self.nearest(self.wave, norm_at),self.nearest(self.time, t)]
                else:
                    norm_factor = 1/max(self.TA[:,self.nearest(self.time, t)])
                if norm_flip:
                        norm_factor = -norm_factor
            VIS_indx = np.where(self.wave < 800)[0]
            plt.plot(self.wave[VIS_indx],self.TA[VIS_indx,self.nearest(self.time, t)]*norm_factor, label = str(t) + ' ps',c=c)
            NIR_indx = np.where(self.wave > 800)[0]
            plt.plot(self.wave[NIR_indx],self.TA[NIR_indx,self.nearest(self.time, t)]*norm_factor,c=c)
        plt.hlines(0,min(self.wave),max(self.wave), lw=2)
        plt.xlim(min(self.wave),max(self.wave))
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('\u0394A ')
        plt.legend(loc="best",ncol = 2)
        if ylim:
            plt.ylim(ylim)
            
    def plotdyn(self, w, log = True, norm = False, scale = 1, label = None):
        if norm:
            dyn = self.TA[self.nearest(self.wave,w),:].T/max(np.abs(self.TA[self.nearest(self.wave,w),:].T))
        else:
            dyn = self.TA[self.nearest(self.wave,w),:].T
        if label:
            plt.plot(self.time,dyn*scale, label = label)
        else:
            plt.plot(self.time,dyn*scale, label = str(w) + ' nm')
        if log:
            plt.xscale('log')
        if norm:
            plt.ylim(0,1.1)
        plt.xlim(min(self.time),max(self.time))
        plt.legend()
        plt.xlabel('Timedelays (ps)')
        plt.ylabel('\u0394A ')
        
    def plotsvd(self,num = 3, neg = False):
        plt.subplot(121)
        plt.plot(self.s,'.')
        plt.subplot(122)
        self.svdguess = np.zeros((self.wave.shape[0],num))
        for i in range(num):
            if neg:
                plt.plot(self.wave,-self.u[:,i], label = 'SVD_' + str(i+1))
                self.svdguess[:,i] = -self.u[:,i]
            else:
                plt.plot(self.wave,self.u[:,i], label = 'SVD_' + str(i+1))
                self.svdguess[:,i] = -self.u[:,i]
        plt.hlines(0,min(self.wave),max(self.wave), lw=2)
        plt.xlim(min(self.wave),max(self.wave))
        plt.legend()
    
    def setGuess(self, MCR_guess):
        self.MCR_guess = MCR_guess
    
    def setMCRRes(self, MCR_spec, MCR_dyn):
        self.MCR_spec  = MCR_spec
        self.MCR_dyn   = MCR_dyn
        
        
    def plotMCR(self, guess = False, norm = False):
        if norm:
            init_total = 0
            for i in range(self.MCR_dyn.shape[1]):
                init_total += self.MCR_dyn[0,i]
            init_total = 1/init_total
        else:
            init_total = 1
        if guess:
            plt.suptitle('Initial Component Guess', fontsize=20,fontweight="bold")
            plt.plot(self.wave,self.MCR_guess)
            plt.hlines(0,self.wave.min(),self.wave.max(),lw =1)
            plt.xlim(self.wave.min(),self.wave.max())
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('\u0394A ')
        else:
            plt.figure(figsize=(20,5))
            plt.subplot(121)
            plt.title('Spectral Components', fontsize=15)
            plt.plot(self.wave,self.MCR_spec)
            plt.hlines(0,min(self.wave),max(self.wave), lw=2)
            plt.xlim(min(self.wave),max(self.wave))
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('\u0394A (norm.)')
            plt.subplot(122)
            plt.title('Component Dynmics', fontsize=15)
            plt.plot(self.time,self.MCR_dyn*init_total)
            plt.xscale('log')
            plt.ylim(0)
            plt.xlim(min(self.time),max(self.time))
            plt.xlabel('Timedelays (ps)')
            plt.ylabel('\u0394A (norm.)')

        
def svd_reconstruction_E15(Data,k):
    D = Data.shape[0]
    T = Data.shape[1]
    u, s, vh = np.linalg.svd(Data, full_matrices=False)
    rec = np.zeros_like(Data)
    for i in range(k):
        rec = rec + np.dot(u[:,i].reshape(D,1) * s[i], vh[i,:].reshape(1,T))
    return rec

def rmse_special(Data, rec):
    D = Data.shape[0]
    temp = np.sqrt(np.sum((Data-rec)**2)/D)
    if temp >= np.sqrt(2/D):
        return temp
    else:
        return np.sqrt(2/D)

def k_opt(Data):
    '''
    Function returning the optimal number of eigen vectors and values for reconstruction (k)
    ----------------------------------------------------------------------------------------
    input:  Data
    output: k
    '''
    D = Data.shape[0]
    T = Data.shape[1]
    rms = [rmse_special(Data, svd_reconstruction_E15(Data,i)) for i in range(T)]
    tk = [(np.log(rms[i]) - np.log(np.sqrt(2/D)))/(np.log(rms[0]) - np.log(np.sqrt(2/D))) for i in range(T)]
    return np.where(np.array(tk) > 0.05)[0][-1] 

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        