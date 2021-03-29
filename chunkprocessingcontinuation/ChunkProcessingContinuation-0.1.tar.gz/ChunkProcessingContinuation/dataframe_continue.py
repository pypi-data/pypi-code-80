import pandas as pd

class Continue:

    def __init__(
        self,
        path_old=None,
        path_new=None,
        path_init=None,
        chunk_path=None,
        chunk_processing=None,
        chunksize=None
    ):
        self.path_old = path_old
        self.path_new = path_new
        self.path_init = path_init
        self.chunk_path = chunk_path
        self.chunk_processing = chunk_processing
        self.chunksize = chunksize

    def reader(self, path):
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            if path.endswith(".xls") or path.endswith(".xlsx"):
                df = pd.read_excel(path)

        return df

    
    def get_leftover(self):
        df_old = self.reader(self.path_old)
        df_new = self.reader(self.path_new)

        df_iterator = df_old[df_new.shape[0]:]
        df_iterator.to_csv(self.path_init, index=False)
        df_iterator = pd.read_csv(self.path_init, iterator=True, chunksize=self.chunksize)

        return df_iterator, df_new
    
    def odd(self, num):
        if num%2 == 1:
            return 1
        else:
            return 0

    

    def main_process(self):
        df_iterator, df_new = self.get_leftover()

        chunk_list = [df_new]
        i = 1
        for data_chunk in df_iterator:
            
            processed_chunk = self.chunk_processing(data_chunk)
            chunk_list.append(processed_chunk)


            if len(chunk_list)>1:
                processed_chunk = pd.concat(chunk_list)
                processed_chunk.to_excel(self.chunk_path.format("checkpoint_chunk_"+str(self.odd(i))), index=False)
            i += 1
        return "Done"

if __name__ == "__main__":
    main_process()