import numpy as np

def nearest(array, value): 
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


#noise filtering functions for TA
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