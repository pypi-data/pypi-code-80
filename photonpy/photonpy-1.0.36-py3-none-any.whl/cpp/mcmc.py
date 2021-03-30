import ctypes as ct
import numpy as np
import numpy.ctypeslib as ctl

from photonpy import Context,Estimator



class PDFInfo(ct.Structure):
    _fields_ = [
        ("pdf", ctl.ndpointer(np.float32, flags="aligned, c_contiguous")),
        ("size", ct.c_int32),
        ("start", ct.c_float),
        ("end", ct.c_float),
    ]

    def __init__(self, pdf, start=0, end=1):
        pdf = np.ascontiguousarray(pdf, dtype=np.float32)
        
        # normalize (elements of pdf*step should sum up to 1)
        step = (end-start) / len(pdf)
        pdf = pdf / (pdf.sum() * step)
        
        self.step = step
        self._pdf = pdf # Hack to make sure the array doesn't get GCed
        self.pdf = pdf.ctypes.data
        self.start = start
        self.end = end


class MCLocalizer:
    def __init__(self, maxEmitters, numFrames, psf:Estimator, intensityPDF:PDFInfo, ctx:Context=None):
        self.ctx = ctx
        lib = self.ctx.smlm.lib

        #MCLocalizer* MCL_Create(int maxEmitters, int nframes, Estimator* psf, const PDFInfo* intensity_pdf);
        self._MCL_Create = lib.MCL_Create
        self._MCL_Create.argtypes = [
            ct.c_void_p,
            ct.c_int32,
            ct.c_int32,
            ct.c_void_p,
            ct.POINTER(PDFInfo)
        ]
        self._MCL_Create.restype = ct.c_void_p
        #void MCL_Destroy(MCLocalizer* mcl;
        
        self._MCL_Destroy = lib.MCL_Destroy
        self._MCL_Destroy.argtypes =[
            ct.c_void_p,
            ]

        self.paramsDType = np.dtype([
            ('pos','<f4', (3,)),
            ('I','<f4', (numFrames,))
        ])
        
        #void MCL_SetSamples(MCLocalizer* mcl, const float* data, const float* background, int numROIs);
        self._MCL_SetSamples = lib.MCL_SetSamples
        self._MCL_SetSamples.argtypes =[
            ct.c_void_p,
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), 
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), 
            ct.c_int32
            ]
        
        #void MCL_ComputeLikelihood(MCLocalizer* mcl, float* ll, const float* params, bg, const int* sampleIndices, int numEvals);
        self._MCL_ComputeLikelihood = lib.MCL_ComputeLikelihood
        self._MCL_ComputeLikelihood.argtypes =[
            ct.c_void_p,
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), 
            ctl.ndpointer(self.paramsDType, flags="aligned, c_contiguous"), 
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # bg
            #ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), 
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"), 
            ct.c_int32
            ]
        
        #void MCL_ComputeExpVal(MCLocalizer* mcl, float* expval, const float* params, int numEvals);
        self._MCL_ComputeExpVal = lib.MCL_ComputeExpVal
        self._MCL_ComputeExpVal.argtypes =[
            ct.c_void_p,
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), 
            #ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), 
            ctl.ndpointer(self.paramsDType, flags="aligned, c_contiguous"), 
            ct.c_int32
            ]
        
        self.maxEmitters = maxEmitters
        self.numFrames = numFrames
        self.psf = psf
        self.inst = self._MCL_Create(ctx.inst, maxEmitters, numFrames, psf.inst, intensityPDF)
        
    
    def Destroy(self):
        if self.inst is not None:
            self._MCL_Destroy(self.inst)
            self.inst = None

    def MakeParams(self, emitterPos, emitterI):
        numEval = emitterPos.shape[0]
        params = np.zeros((numEval, self.maxEmitters),dtype=self.paramsDType)
        params['pos'] = emitterPos
        params['I'] = emitterI
        return params
            
    def Likelihood(self, emitterPos, emitterI, backgrounds, sampleIndices):
        assert len(emitterPos) == len(sampleIndices)
        assert np.array_equal(backgrounds.shape,[len(emitterPos)])

        backgrounds = np.ascontiguousarray(backgrounds,dtype=np.float32)        
        sampleIndices = np.ascontiguousarray(sampleIndices,dtype=np.int32)
        params = self.MakeParams(emitterPos, emitterI)
        ll = np.zeros(len(params), dtype=np.float32)
        self._MCL_ComputeLikelihood(self.inst, ll, params, backgrounds, sampleIndices, len(params))
        return ll
            
    def SetSamples(self, samples, backgrounds):
        """
        Every sample has an associated background estimate, 
        in practice typically from a temporal median filter over a series of frames
        
        samples: [numsmp, numframes, psf samplecount]
        backgrounds: same as samples
        """
        samples = np.ascontiguousarray(samples,dtype=np.float32)
        backgrounds = np.ascontiguousarray(backgrounds,dtype=np.float32)
        assert np.array_equal(samples.shape, [samples.shape[0], samples.shape[1], *self.psf.sampleshape])
        assert np.array_equal(samples.shape, backgrounds.shape)
        
        self._MCL_SetSamples(self.inst, samples, backgrounds, len(samples))
        
        
            
    def ExpectedValue(self, emitterPos, emitterI):
        """
        emitterPos: [numEval, maxEmitters, 3]
        emitterI: [numEval, maxEmitters, numFrames]
        
        sampleIndices  
        """ 
        
        params = self.MakeParams(emitterPos, emitterI)
        
        expval = np.zeros((len(params), self.numFrames, *self.psf.sampleshape), dtype=np.float32)
        self._MCL_ComputeExpVal(self.inst, expval, params, len(params))
        
        return expval
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.Destroy()
        
if __name__ == '__main__':
    from photonpy import GaussianPSFMethods, Gauss3D_Calibration
    
    with Context() as ctx:
        
        gpm = GaussianPSFMethods(ctx)

        param = [  - 1.7, -0.464,  0.834, 0 ]
        calib = Gauss3D_Calibration(param ,param, zrange=[-1.5,1.5])
        psf = gpm.CreatePSF_XYZIBg(20, calib, cuda=True) # cuda might be faster at n*numFrames>10000
        
        intensityPDF = PDFInfo(np.ones(10), 100, 2000)
        
        maxEm = 3
        numFrames = 10
        mcl = MCLocalizer(maxEm, numFrames, psf, intensityPDF, ctx) 
        
        n = 10
        roisize = psf.sampleshape[0]
        pos = np.random.uniform([2,2,-1],[roisize-2,roisize-2,1], size=(n, maxEm, 3))
        I = np.random.uniform(200, 1000, size=(n, maxEm, numFrames))
        
        bg = 10
        expval = mcl.ExpectedValue(pos, I) +bg
        smp = np.random.poisson(expval)
                
        mcl.SetSamples(smp, smp*0)
        ll = mcl.Likelihood(pos, I, np.ones(n)*bg, np.arange(n))
        
        print(ll)

        import napari
        with napari.gui_qt():
            napari.view_image(smp)

        
        