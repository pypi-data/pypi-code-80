import pyfsdb
import sys
import pandas as pd

from baseClasses import OutputMixIn

class DF2Stdout(OutputMixIn):
    iostream = sys.stdout
    
    def push_output(self):
        pd.set_option('display.max_rows', self.output_intermediary.shape[0]+1)
        print("DF FRAME OUTPUT: ")
        print("++++++++++++++++")
        print(self.output_intermediary)

class DF2File(OutputMixIn):
    outputFile = None
    
    def push_output(self):
        if self.outputFile == None:
            self.logger.error("No output file given")
            exit()
        try: 
            with open(self.outputFile, 'w') as f:
                if f == None:
                    self.logger.error("Failed to open file %s for writing.", self.outputFile)
                    exit()
                fsdb_obj = pyfsdb.Fsdb(out_file_handle=f)
                fsdb_obj.put_pandas(self.output_intermediary)
        except Exception as ex:
            self.logger.error("Failed to write out to file. %s", ex)
            
            
                