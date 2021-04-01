import os
import glob
import re
import numpy as np
import pandas as pd

from gingko.utils import load_numpy, save_numpy

re_spaces = re.compile(r'\s+')
re_symbols = re.compile(r'[^a-zA-Z0-9\s\']')

def clean_word(text):
    text = re_symbols.sub(' ', text)
    text = re_spaces.sub(' ', text).strip()
    return text

re_sentence = re.compile(r'(?<=[\.\?\!])\s')

def splitby_sentence(text):
    return re_sentence.split(text)

def splitby_word(text):
    return text.split()

def split_data(df, split_fn, split_name, split_col='data'):
    assert split_col in df.columns
    
    df_dict = {split_name:[]}
    df_dict.update({k:[] for k in df.columns})
    
    for i, split in enumerate(map(split_fn, df[split_col])):
        for k in df_dict.keys():
            if k==split_col:
                df_dict[k].extend(split)
            elif k==split_name:
                df_dict[k].extend([i]*len(split))
            else:
                df_dict[k].extend([df[k].iloc[i]]*len(split))
    return pd.DataFrame(df_dict)

def reindex(idxs_list, sparse=False):
    n_depth = len(idxs_list[0])
    out_idxs = []
    _idx = [0]*n_depth
    for j, idx in enumerate(idxs_list):
        if j>0:
            for i in range(n_depth):
                if i<n_depth-1 and idx[i+1:]!=idxs_list[j-1][i+1:]:
                    if sparse:
                        _idx[i] = 0
                    else:
                        _idx[i] +=1
                elif idx[i]!=idxs_list[j-1][i]:
                    _idx[i] +=1
        out_idxs.append(tuple(_idx))
    return out_idxs

def reindex_df(df, idxs_cols, sparse=True):
    og_cols = df.columns.tolist()
    assert all(x in og_cols for x in idxs_cols)
    
    idxs = df[idxs_cols].to_records(index=False).tolist()
    idxs = reindex(idxs, sparse=sparse)
    return pd.concat([
        df.drop(columns=idxs_cols),
        pd.DataFrame(idxs, columns=idxs_cols)
    ], axis=1)[og_cols]

def get_wiki_urls(data_dir):
    url_list = glob.glob(os.path.join(data_dir, '*'))
    return dict(zip(range(len(url_list)), url_list))

def load_wiki_df(csv_path):
    return pd.read_csv(csv_path).drop(columns=['tags'])

def format_wiki_df(df, split_fn, idxs_cols):
    df = split_data(df, split_fn, 'paragraph', split_col='data')
    df.reset_index(inplace=True)
    df.rename(columns = {'index':'word'}, inplace=True)
    return df

def load_wiki_corpus(url_dict, split_fn, idxs_cols):
    indices = []
    values = []
    
    for k,v in url_dict.items():
        _df = format_wiki_df(load_wiki_df(v), split_fn, idxs_cols=idxs_cols)
        _df['topic'] = np.array([k]*len(_df), dtype=np.int64)

        indices +=[_df[['topic']+idxs_cols].values.astype(np.int64)]
        values +=_df['data'].tolist()
    return {'indices':np.concatenate(indices, axis=0).T, 'values':values}