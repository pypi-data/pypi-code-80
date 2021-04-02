import logging
import itertools
import pandas as pd
import typing
import ast
import numpy as np
#from numpy.typing import ArrayLike
from numpy.lib.stride_tricks import as_strided
from numpy.lib import pad
from matrixprofile import matrixProfile
from tspf_stomp.stomp import TSPFStomp

from baseClasses import AnalysisMixIn
from helpers.timeseries import get_full_index_for_padding, pad_out_data

class timeMotifBasic(AnalysisMixIn):
    _str_name = "Time Motif Basic"

    output_intermediary = None
    event_cut_off_ts = 1617330749
    
    # A chance to add additional motifs to look for
    # outside of what is discovered.
    # Input is a string to allow for commandline/file input.
    extra_shapes_str = "[]"
    
    # Col for y value of timeseries.
    y_value_col = None
    group_on_key = 'key'

    def set_y_value_col(self, val):
        self.y_value_col = val

    def set_group_on_key(self, val):
        self.group_on_key = val

    def set_corr_feature(self, val):
        self.corr_feature = val

    def set_event_cut_off_ts(self, val):
        try:
            self.event_cut_off_ts = int("23".split('.')[0])
        except Exception as ex:
            self.logger.error("Failed to convert %s to a time for event cut off.", val)
            self.event_cut_off_ts = 1617330749
            
    def _get_single_key_data(self, key):
        is_key = self.df[self.group_on_key] == key
        key_df = self.df[is_key].sort_index()
        return key_df
    
    def _perturb_repeat_series(self, ts, upper_noise_val=.005):
        # We need to add noise to avoid divide by zero issues in std dev and
        # closest neighbor calculations.
        noise = np.random.normal(0, upper_noise_val, ts.shape)

        df = pd.DataFrame({'x':ts})
        noise = np.random.normal(0, upper_noise_val, df['x'].shape)
        df['dup'] = df.duplicated(subset='x', keep=False)
        df['y'] = np.where(df['dup'] == True, df['x'] + noise, df['x'])
        return np.array(df['y'].tolist())
        
    def _remove_zero_runs(self, ts):
        # The below just masks out 0s
        #ts = np.ma.masked_values(ts, 0)
        #return ts.compressed(), ts.mask
        
        # We want to leave 0s, but not runs of 0s.
        # So we shift the ts
        # and & this with the orginal on all values =0 
        ts = np.array(ts)
        ts_shifted = np.roll(ts, shift=-1)
        mask = (ts == 0) & (ts_shifted == 0)
        
        ts = np.ma.masked_array(ts, mask=mask)
        
        return ts.compressed(), ts.mask
    
    def _add_back_zero_runs_to_mp(self, mp, mask):
        mp_index = 0
        mask_index = 0
    
        # Matrix profiles near 0 indicate a motif
        # so we don't want to pad back out our mp timeseries
        # with 0s. Instead, we pick between the min and max.
        mp_fill_in = (np.amin(mp) + np.amax(mp))/2
    
        zeroed_mp = []
    
        while mask_index < len(mask):
            if not mask[mask_index]:
            # Mask is False, so use the actual MP value.
                if mp_index < len(mp):
                    zeroed_mp.append(mp[mp_index])
                    mp_index = mp_index + 1
                else:
                    zeroed_mp.append(mp_fill_in)
            else:
            # Mask is True, so this is a "zero run"
            # Fill with fill in value.
                zeroed_mp.append(mp_fill_in)
            mask_index = mask_index + 1            
        return zeroed_mp

    def _ranges_of_strong_motifs(self, mp_with_zero_runs):
        """
        Currently not used, but thresholding for motifs is not all it could be.
        This is a stop-gap so that we can ensure the entirety of a motif is below
        the threshold, not just parts of it.
        """
        run = []
        ranges = []
        expected_next = -1
        print(mp_with_zero_runs)
        THRESHOLD = 1
        
        this_index = 0
        last_index = -1
        for v in mp_with_zero_runs:
            if (v < THRESHOLD):
                print("Current run", run, " Ranges", ranges, "this index", this_index, "last index", last_index)
                if last_index + 1 == this_index:
                    run.append(this_index)
                else:
                    if(len(run) > 0):
                        ranges.append(run)
                    run = [this_index]
                last_index = this_index 
                
            this_index = this_index + 1
            
        return ranges
    
            
    def analyze(self):
        
        self.output_intermediary = pd.DataFrame(columns=['key1', 'key2', 'window_size', 'corr_start', 'corr_stop', 'corr_len', 'min_kendall_rank', 'corr_type'])
        self.output_intermediary.astype({'key1':'string', 'key2':'string', 'window_size':'int', 'min_kendall_rank':'float', 'corr_type':'string'}).dtypes

        try:
            self.df, self.group_list, self.group_on_key, group_size = self.input_intermediary
            if self.df.empty:
                self.logger.debug("%s: Received empty pandas DataFrame for analysis.", type(self).__name__)        
        except ValueError:
            self.logger.error("%s: Did not receive expected input.", type(self).__name__)
            exit()

        # Check to be sure we have a y_val_col.
        if self.y_value_col == None:
            self.logger.error("%s: No y-val column specification for time series.", type(self).__name__)
            exit()

        # If we have groups, we only handle groups
        # of size 1 for now.
        if group_size == 1:
            tspf = TSPFStomp()
            master_ts = []
            group_dfs = {}
            full_index = []
            master_df = pd.DataFrame()
            ts_dict = {}
            max_ts_len = -1
            min_ts_len = -1
            
            # Get the full index so we know how to pad out data 
            # to normalize across all time series.
            self.logger.debug("Building full index for all groups.")
            for group in self.group_list:
                group_df = self._get_single_key_data(group)
                if(len(group_df.index)) > 10:
                    if master_df.empty:
                        # Get the column names from the group.
                        master_df = pd.DataFrame(columns=group_df.columns)
                
                    full_index = get_full_index_for_padding([master_df,group_df])
                    master_df, group_df = pad_out_data([master_df, group_df], full_index, fill_vals={self.y_value_col:0})
            self.logger.debug("Full index covers from %s to %s.", str(full_index[0]), str(full_index[-1])) 
            self.full_index = full_index
     
            
            # Now that we have a full index, loop through again
            # and create one single time series.
            for group in self.group_list:
                group_df = self._get_single_key_data(group)
                master_df, group_df = pad_out_data([master_df, group_df], full_index, fill_vals={self.y_value_col:0})
                
                # Do a rolling average if we can:
                #try:
                #    group_df['rolling'] = group_df.rolling(window=7).mean().fillna(0)
                #    group_df[self.y_value_col] = group_df['rolling']
                #except:
                #    print("Failed to do rolling average.")
                #    pass
                
                #noise = np.random.normal(0, .001, group_df[self.y_value_col].shape)
                #group_df[self.y_value_col] = group_df[self.y_value_col] + noise
                
                # Save the df for later?
                group_dfs[group] = group_df
                
                # Get just the timeseries for the group (no index, just y_val)
                group_ts = group_df[self.y_value_col].to_list()
                #group_ts = group_df['rolling'].to_list()
                
                # Keep tabs on our min and max length of non-zero time series.
                if len(list(filter((0).__ne__, group_ts))) > max_ts_len:
                    max_ts_len = len(list(filter((0).__ne__, group_ts)))
                if len(list(filter((0).__ne__, group_ts))) < min_ts_len or min_ts_len == -1:
                    min_ts_len = len(list(filter((0).__ne__, group_ts)))
                
                # Concatonate padded time series to our master time series (where we'll do motif discovery).  
                master_ts = master_ts + group_ts
                
            # Get list of all motifs across all groups.
            master_np = np.array(master_ts)
            no_zeros_master_ts, master_mask = self._remove_zero_runs(master_np)
            
            # Add noise
            #minval = np.min(no_zeros_master_ts[np.nonzero(no_zeros_master_ts)])
            #upper_noise_val = minval/500
            #no_zeros_master_ts = self._perturb_repeat_series(no_zeros_master_ts, upper_noise_val=upper_noise_val)
            
            np.set_printoptions(suppress=True)
            print(no_zeros_master_ts)
            
            # XXX Add noise?
            # Get the smallest val
            #minval = np.min(no_zeros_master_ts[np.nonzero(no_zeros_master_ts)])
            #upper_noise_val = minval/200
            #
            #self.logger.debug("Adding noise, up to: %.3f", upper_noise_val)
            #noise = np.random.normal(0, upper_noise_val, no_zeros_master_ts.shape)
            #no_zeros_master_ts = no_zeros_master_ts + noise
            # XXX            

            # Discover motifs

            min_motif_len = min(5, int(min_ts_len/10))
            max_motif_len = min(min_motif_len*2, int(max_ts_len/10))

            self.logger.debug("Looking for motifs in step duration of %d steps and %d steps over ts of len %d.", min_motif_len, max_motif_len, len(no_zeros_master_ts))
            all_motifs = tspf.discover(no_zeros_master_ts, min_duration=min_motif_len, max_duration=max_motif_len)
            
            # Filter motifs
            self.logger.debug("Discovered %d motifs.", len(all_motifs))
            all_motifs = tspf.filter_candidates(all_motifs)
            self.logger.debug("Filtered down to %d motifs", len(all_motifs))
            
            # Get motif shapes to search for
            self.logger.debug(all_motifs)
            shapes = tspf.motif_shapes_from_tuple(all_motifs, no_zeros_master_ts)
            self.logger.debug("Total of %d motifs found across groups." % len(shapes))
            
            # Get any extra shapes to search for.
            extra_shapes = []
            try:
                self.logger.debug("Parsing shape string: %s", self.extra_shapes_str)
                tmp = ast.literal_eval(self.extra_shapes_str)
                if not isinstance(tmp, list):
                    raise ValueError("Not given list for extra shapes.")
                if not any(isinstance(tmp, list) for el in tmp):
                    raise ValueError("Not given list of lists for extra shapes.")
                for el in tmp:
                    try:
                        if len(el) > 4:
                            extra_shapes.append(list(map(float, el)))
                    except Exception as ex1:
                        self.logger.warn("Failed to translate string %s to shape list: %s", el, ex1)
                        continue
            except Exception as ex2:
                self.logger.warn("Failed to parse input of extra shapes: %s %s", self.extra_shapes_str, ex2)
                extra_shapes = []
                pass
            shapes = extra_shapes + shapes
            # Keep only the unique shapes.
            shapes = [list(i) for i in set(tuple(i) for i in shapes)]
            
            self.output_intermediary = pd.DataFrame(columns=['motif_id', 'motif_len', 'motif_shape', 'key', 'locations', 'score'])
            self.output_intermediary.astype({'motif_id':'int', 'motif_len':'int', 'motif_shape':'string', 'key':'string', 'locations':'string', 'score':'float64'})
            
            motif_id = 0
            for shape in shapes:
                # De-noise shape?
                shape = np.rint(shape)
                motif_len = len(shape)
                if motif_len < 4:
                    self.logger.warn("Too short motif. Skipping: %s", ",".join(shape))
                    continue
                
                print("Motif----------------->", end="")
                print(shape)
                for group in group_dfs:
                    # Get the df
                    group_df = group_dfs[group]
                    
                    # Get the y_vals in a time series, and remove 0 runs
                    group_ts = group_df[self.y_value_col].to_list()
                    #group_ts = group_df['rolling'].to_list()
                    group_np = np.array(group_ts)
                    
                    #group_ts, mask = self._remove_zero_runs(group_np)
                    #group_np = np.array(group_ts)
                    
                    # XXX Add noise?
                    #noise = np.random.normal(0,upper_noise_val, group_np.shape)
                    #group_np = group_np + noise
                    #group_np = self._perturb_repeat_series(group_np, upper_noise_val=upper_noise_val)
                    #
                    
                    # Locate previously identified motif shapes.
                    try:
                        located_motifs = tspf.locate(group_np, [shape])
                        if len(located_motifs) > 0:
                            print("\t\t", end="")
                            print(group, end=" ")
                            print(located_motifs)
                            found_locations = []
                            include = False 
                            for loc in located_motifs[0][2]:
                                t = self.full_index[loc]
                                found_locations.append(t)
                                if t > self.event_cut_off_ts:
                                    include = True
                            
                            if include:
                                row = {'motif_id':motif_id, 'motif_len':motif_len, 'motif_shape':str(shape), 'key':str(group), 'locations':str(found_locations), 'score':(located_motifs[0][1])}
                                self.output_intermediary = self.output_intermediary.append(row, ignore_index=True)

                    except Exception as ex:
                        self.logger.error("Failed because %s", ex)
            
                motif_id = motif_id + 1    
            self.group_dfs = group_dfs
        # If we don't have groups, we make an entire
        # time series from the df and look for motifs there.
        else:
            pass
            
    








