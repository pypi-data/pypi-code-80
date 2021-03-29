import pandas as pd
from Bio import SeqIO
from gisaid.exceptions import *
import glob
import re


def logfile(*args):
    if args[1]["rc"] != "ok":
        with open("logfile.csv", "a+") as f:
            reason = str((args[1]["validation"])).replace(",", "")
            line = str("\n" + f'{args[0]}, {reason}')
            f.write(line)
    else:
        with open("logfile.csv", "a+") as f:
            line = str("\n" + f"{args[0]}, success")
            f.write(line)


def check_file(fname):
    d = {}
    if "collated" in fname:
        d.update(collated=True)
    else:
        d.update(collated=False)
    try:
        for i in fname:
            if re.search("\.csv$", i, flags=re.IGNORECASE):
                d["csv"] = i
            elif re.search("\.fa$", i, flags=re.IGNORECASE):
                d["fa"] = i
            elif i == "collated":
                pass
            else:
                raise FileError
                
    except IndexError:
        raise DataError
    return d


def collate(data):
    x = pd.read_csv(data["csv"], index_col=0)
    x.rename({"CollectionDate": "covv_collection_date"}, axis=1, inplace=True)
    x["covv_collection_date"] = pd.to_datetime(x["covv_collection_date"])
    x["covv_collection_date"] = x["covv_collection_date"].astype(str)
    x = (x.fillna("")).replace("NaT", "")
    metadata = x.apply(lambda x: x.to_dict(), axis=1)
    return metadata


def read_files(args):
    try:
        data = check_file(args)
    except IndexError:
        raise FileError
        
    metadata = collate(data)    
    if not data["collated"]:
        try:
            seq = {k.id: str(k.seq) for k in SeqIO.parse(data["fa"], "fasta")}

            {
                i.update({"covv_sequence": seq[k] for k in i.values() if k in seq})
                for i in metadata
            }
            
        except KeyError:
            raise DataError
        except TypeError:
            raise DataError
    else:
        pass
    return metadata


def collate_fa(kwargs):
    """Collate folder or subfolders of fasta files"""
    if kwargs["sub"]:
        folder = "**/*"
    else:
        folder = "*"
        
    sequences = {}
    for file in glob.iglob("{}/{}".format(kwargs["fa"], folder)):
        sequence = {k.id: str(k.seq) for k in SeqIO.parse(file, "fasta")}
        sequences.update(sequence)  

    metadata = collate(kwargs["csv"])

    {
        i.update({"covv_sequence": seq[k] for k in i.values() if k in sequences})
        for i in metadata
    }
    return metadata
