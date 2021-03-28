import os
import pandas as pd

def load_dataset(name, index_name, from_day, to_day, image_size):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, 'data', name + '.csv')
    df = pd.read_csv(path, parse_dates=True, index_col=index_name)
    
    if name == 'GBPUSD15':
        
        df['ma200'] = df['Close'].rolling(200).mean()
        df['ma100'] = df['Close'].rolling(100).mean()
        df['ma50'] = df['Close'].rolling(50).mean()
        df['ma22'] = df['Close'].rolling(22).mean()
        df_dropna = df.dropna()
        df_out = df_dropna[from_day:to_day]
        n_drop = image_size*4 - 3 -image_size
        df_hdrop = df_out.drop(index=df_out[0:n_drop].index)
        df_final = df_hdrop.drop(index=df_hdrop[-3:].index)
    
    if name == 'GBPUSD60':
        
        df['ma200'] = df['Close'].rolling(200).mean()
        df['ma100'] = df['Close'].rolling(100).mean()
        df['ma50'] = df['Close'].rolling(50).mean()
        df['ma22'] = df['Close'].rolling(22).mean()
        df_dropna = df.dropna()
        df_final = df_dropna[from_day:to_day]

    
    return df_final