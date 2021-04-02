import itertools
import pandas as pd
import typing
import numpy as np
from numpy.lib.stride_tricks import as_strided
from numpy.lib import pad

from baseClasses import AnalysisMixIn
from helpers.timeseries import get_full_index_for_padding, pad_out_data


class PairWiseKendallCorr(AnalysisMixIn):
    output_intermediary = None
    window_size = 7
    group_size = 2
    group_on_key = 'key'
    corr_feature = 'value'
    NEG_CORR_THRESH = -0.86
    POS_CORR_THRESH = 0.86
    
    # Events must be ongoing or newer than 
    # the below date to be output.
    event_cut_off_ts = '1617241625'
    
    def set_window_size(self, val):
        self.window_size = val
    
    def set_group_on_key(self, val):
        self.group_on_key = val
    
    def set_corr_feature(self, val):
        self.corr_feature = val

    def set_event_cut_off_ts(self, val):
        self.event_cut_off_ts = val
    
    def _get_single_key_data(self, key):
        is_key = self.df[self.group_on_key] == key
        key_df = self.df[is_key].sort_index()
        return key_df
    
    def _rolling_corr(self, pseqa:pd.Series, pseqb:pd.Series):
        # Panads no longer passes numpy
        # array properties (e.g. strides).
        seqa = pseqa.to_numpy()
        seqb = pseqb.to_numpy()
        
        stridea = seqa.strides[0]
        ssa = as_strided(seqa, shape=[len(seqa) - self.window_size + 1, self.window_size], strides=[stridea, stridea])
        strideb = seqa.strides[0]
        ssb = as_strided(seqb, shape=[len(seqb) - self.window_size + 1, self.window_size], strides=[strideb, strideb])
        ar = pd.DataFrame(ssa)
        br = pd.DataFrame(ssb)
        ar = ar.rank(1)
        br = br.rank(1)
        corrs = ar.corrwith(br, 1, method='kendall')
        result = pad(corrs, (self.window_size - 1, 0), 'constant', constant_values=np.nan)
        presult = pd.Series(result)
        presult = presult.shift(periods=-(int)(self.window_size/2), fill_value=np.nan)
        return presult
    
    def _ranges_of_corr(self, df:pd.DataFrame, key1:str, key2:str):
        df['neg'] = (df['kendall'] < self.NEG_CORR_THRESH)
        df['pos'] = (df['kendall'] > self.POS_CORR_THRESH)

        start_neg = df.index[df['neg'] & ~ df['neg'].shift(1).fillna(False)] 
        last_neg =  df.index[df['neg'] & ~ df['neg'].shift(-1).fillna(False)] 

        start_pos = df.index[df['pos'] & ~ df['pos'].shift(1).fillna(False)] 
        last_pos = df.index[df['pos'] & ~ df['pos'].shift(-1).fillna(False)] 
        
        nr = [(i,j) for i, j in zip(start_neg, last_neg) if j > 0]
        pr = [(i,j) for i, j in zip(start_pos, last_pos) if j > 0]

        for start, stop in nr:
            if len(df[start:stop]) > 0:
                row = self._return_output_row(df, start, stop, key1, key2, "neg")
                self.output_intermediary = self.output_intermediary.append(row, ignore_index=True)        
        for start, stop in pr:
            if len(df[start:stop] > 0):
                row = self._return_output_row(df, start, stop, key1, key2, "pos")
                self.output_intermediary = self.output_intermediary.append(row, ignore_index=True)        
                
    def _return_output_row(self, df:pd.DataFrame, start, stop, key1:str, key2:str, corr_type:str='pos'):
        row = {'key1':key1, 'key2':key2, 'window_size':self.window_size}
        row['corr_start'] = df[start:stop]['timestamp'].min()
        row['corr_stop'] = df[start:stop]['timestamp'].max()
        row['min_kendall_rank'] = df[start:stop]['kendall'].min()
        row['corr_len'] = len(df[start:stop])
        row['corr_type'] = corr_type
        return row
            
    def analyze(self):
        
        self.output_intermediary = pd.DataFrame(columns=['key1', 'key2', 'window_size', 'corr_start', 'corr_stop', 'corr_len', 'min_kendall_rank', 'corr_type'])
        self.output_intermediary.astype({'key1':'string', 'key2':'string', 'window_size':'int', 'min_kendall_rank':'float', 'corr_type':'string'}).dtypes
        
        try:
            self.df, self.group_list, self.group_on_key, group_size = self.input_intermediary
            # Fill in values with 0 if FSDB had blanks in int/float columns.
            self.df['value'] = self.df['value'].fillna(0)
            self.df['value'] = self.df['value'].astype(int)
            
            if self.df.empty:
                self.logger.error("Received empty df for analysis.")        
        except ValueError:
            self.logger.error("Did not receive expected input.")
            exit()

        for pair in self.group_list:
            self.logger.debug("Doing pair: %s x %s", pair[0], pair[1])
            key_one_df = self._get_single_key_data(pair[0])
            key_two_df = self._get_single_key_data(pair[1])
 
            full_index = get_full_index_for_padding([key_one_df,key_two_df])
            key_one_df, key_two_df = pad_out_data([key_one_df, key_two_df], full_index,fill_vals={'value':0})
        
            try:
                kendall = self._rolling_corr(key_one_df[self.corr_feature], key_two_df[self.corr_feature])
                corr_df = pd.DataFrame(list(zip(key_one_df.index.tolist(),kendall.values)), columns = ['timestamp', 'kendall'])
                self._ranges_of_corr(corr_df, pair[0], pair[1])
            except ValueError as ex1:
                self.logger.warn("Failed to compute kendall correlation for %s x %s: %s", pair[0], pair[1], ex1)
                pass
            except Exception as ex2:
                self.logger.error("Failed to compute kendall correlation for %s x %s: %s", pair[0], pair[1], ex2)
                pass
            

        # Filter out any events that don't match our time window we care about..
        # Only report out events that match our cut off
        event_cut_off_ts_val = 1617241625
        try:
            event_cut_off_ts_val = int(self.event_cut_off_ts)
            self.logger.debug("Time cut off for events is %d", event_cut_off_ts_val)
        except Exception as ex:
            self.logger.error("Could not parse time cut off given: %s :%s", self.event_cut_off_ts, ex)
            event_cut_off_ts_val = 1617241625

        self.logger.debug("Before filtering for *only* current events (cut off at %d), %d events", event_cut_off_ts_val, len(self.output_intermediary.index))
        tmp_df = self.output_intermediary[self.output_intermediary['corr_stop'] > event_cut_off_ts_val]
        self.output_intermediary = tmp_df
        self.logger.debug("After filtering for *only* current events, %d events", len(self.output_intermediary.index))
        
        