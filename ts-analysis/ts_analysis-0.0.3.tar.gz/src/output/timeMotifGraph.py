import sys
import pandas as pd
import matplotlib.pyplot as plt

from baseClasses import OutputMixIn

class timeMotifGraph(OutputMixIn):
    group_dfs = None
    full_index = None
    
    def _str_to_float_list(self, str_list):
        if ',' in str_list:
            list_list = str_list.strip('][').split(',')
        else:
            list_list = str_list.strip('][').split()
        return_list = []
        for s in list_list:
            try:
                return_list.append(float(s.strip()))
            except ValueError as ex:
                self.logger.error("Failed to convert string ('%s') to float: %s", s, ex)
                return return_list
        return return_list
    
    def push_output(self):
        if self.group_dfs == None:
            self.logger.error("Failed to find timeseries data to graph.")
            exit()
        if self.output_intermediary.empty:
            self.logger.error("Failed to find motif data to graph.")
            exit()
        
        motif_ids = pd.unique(self.output_intermediary['motif_id']).tolist()
        motif_count = len(motif_ids)
                 
        f,ax=plt.subplots(motif_count,1,figsize=(14,6),sharex=True)
        plt.xticks(rotation=45)
        
        for motif_id in motif_ids:
            #ax[motif_id].set_ylim(top=100)

            # Pull just this motif
            motif_id_int = int(motif_id)
            motif_df = self.output_intermediary[self.output_intermediary['motif_id'] == motif_id_int]
            print(motif_id)
            print(motif_df)

            # Get the top scores only.
            high_scores_df = motif_df.nsmallest(15, columns=['score'])

            # Get the group names
            keys = high_scores_df.key.unique()

            # Get the shape of the motif
            motif_shape = self._str_to_float_list(high_scores_df['motif_shape'].any())
            motif_len = len(motif_shape)
            print("Motif shape", end=" ")
            print(motif_shape)

            for key in keys:
                # Get index location(s) of motif for this key
                strloc = motif_df.loc[motif_df['key'] == key].iloc[-1]['locations']
                locs = self._str_to_float_list(strloc)
                
                # Get score for this key & motif
                score = motif_df.loc[motif_df['key'] == key].iloc[-1]['score']
                if float(score) > .02:
                    continue
                
                # Check if this key is in the self.group_dfs
                # Get the time series.
                key_ts = self.group_dfs[key][self.y_value_col].to_list()
                
                # Add to plot as labled line
                ax[motif_id].plot(self.full_index, key_ts)
                ax[motif_id].lines[-1].set_label('%s' % (key))
                c = ax[motif_id].lines[-1].get_color()
                
                # Highlight location of motif using motif shape and key loc.
                print(locs)
                print(motif_len)
                for l in locs:
                    print("l: ", end=" ")
                    print(l)
                    xs = []
                    xs = self.full_index[int(l):int(l)+motif_len]

                    ax[motif_id].plot(xs, motif_shape, 'o--', color=c, alpha=0.3)
                    
            ax[motif_id].legend()
        
        plt.savefig('the_graph.png')
        plt.close('all')    
