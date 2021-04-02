"""
Helper functions for time series analysis.
"""
def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expected = -1
    
    for v in vals:
        if (v == expected) or (expected == -1):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expected = v + step
    return result

def remove_zero_runs(ts):
    ts = np.ma.masked_equal(ts,0)
    return ts.compressed(), ts.mask

def add_zero_runs(mp, ts_orig):
    mp_index = 0
    ts_index = 0
    
    zeroed_mp = []
    
    while(ts_index < len(ts_orig)):
        if ts_orig[ts_index] != 0:
            if mp_index < len(mp):
                zeroed_mp.append(mp[mp_index])
                mp_index = mp_index + 1
            else:
                zeroed_mp.append(3)
        else:
            zeroed_mp.append(3)
        ts_index = ts_index + 1            
    return zeroed_mp
