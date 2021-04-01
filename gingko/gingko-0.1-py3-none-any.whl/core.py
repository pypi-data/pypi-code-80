import itertools
import numpy as np

import dataclasses
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

@dataclass
class Gingko:
    """
    COO sparse tensor for text data that allows for hierarchical slicing
    """
    indices: np.ndarray
    values: List[Union[float, int, str]]
    ptrs: Optional[List[np.array]] = None
    check: Optional[bool] = False
    
    def __post_init__(self):
        self.d, self.n = self.indices.shape
        
        if self.n!=len(self.values):
            raise ValueError("length of values and indices should be equal")

        self.ptrs = self._make_ptrs()
        if self.check:
            if all((self[:].indices==self.indices).reshape(-1)):
                print('Check successful: indices match')
            else:
                raise ValueError('Check error: index mismatch')
        
    def __getitem__(self, *args):
        slices = self._args2slices(args)
        combs = list(itertools.product(*slices))
        return self._dfs_output(combs[0])
    
    def _dfs_output(self, comb):
        indices = []
        values = []
        for _out in self._dfs_record(comb):
            length = _out[0].stop - _out[0].start
            indices += list(map(lambda x: tuple(reversed([x]+_out[1])), range(length)))
            values += self.values[_out[0]]
        del self._output
        return Gingko(indices=np.array(indices).T, values=values)
    
    def _dfs_record(self, comb):
        self._output = []
        self._dfs_recursion(comb)
        return self._output
    
    def _dfs_next(self, ptr, slc1, slc2=slice(None, None)):
        return list(map(lambda x: slice(*x), zip(ptr[slc2], ptr[1:][slc2])))[slc1]
    
    def _dfs_recursion(self, comb, slc2=slice(None, None), i=0, idx=None):
        if idx is None:
            idx = [0]*len(self.ptrs)
            
        if i<len(self.ptrs):
            for j,child in enumerate(self._dfs_next(self.ptrs[i], comb[i], slc2)):
                idx[i] = j
                self._dfs_recursion(comb, child, i+1, idx)
        else:
            slice_start = slc2.start+comb[i].start if comb[i].start is not None else slc2.start
            slice_stop = min(slc2.stop, slice_start+comb[i].stop) if comb[i].stop is not None else slc2.stop
            self._output.append((slice(slice_start, slice_stop), list(reversed(idx))))
        
    def _args2slices(self, args):
        """Convert mixed subscripts into a list-of-list of slices"""
        if isinstance(args[0], int):
            slices = [slice(args[0], args[0]+1)]
        elif isinstance(args[0], slice):
            slices = [args[0]]
        else:
            slices = list(args[0])
        
        if len(slices)>self.d:
            raise ValueError("too many indices for tensor")
            
        for i,s in enumerate(slices):
            if isinstance(s, int):
                slices[i] = [slice(s, s+1)]
            elif isinstance(s, list) or isinstance(s, np.ndarray):
                slices[i] = list(map(lambda x: slice(x, x+1), s))
            elif isinstance(s, slice):
                slices[i] = [s]
            else:
                raise ValueError("args must be slice, int, list-like")
                
        if len(slices)<self.d:
            slices +=[[slice(None, None)] for _ in range(self.d-len(slices))]
            
        return slices
        
    def _make_ptrs(self):
        """Make hierarhical pointers for slicing"""
        _ptrs, _ptrset = list(), set()
        for x in self.indices[:-1]:
            _ptrset.update(np.diff(x,prepend=[-1],append=[-1]).nonzero()[0])
            _ptrs.append(np.array(sorted(list(_ptrset))))

        ptrs = [_ptrs[-1]]
        self.shape = (max(np.diff(ptrs[-1])),)
        for i in range(len(_ptrs)-2,-1,-1):
            ptrs.insert(0, np.array(list(map(lambda x: np.where(_ptrs[i+1]==x)[0], _ptrs[i]))).squeeze())
            self.shape = (max(np.diff(ptrs[0])),) + self.shape
        self.shape = (len(ptrs[0])-1,) + self.shape
        return ptrs