import os 
import numpy as np
import pandas as pd
from tcrdist.repertoire import TCRrep
from tcrdist.mixcr import mixcr_to_tcrdist3

# The following files are part of preprint manuscript Minervina: 
files_and_chains  = [('contracting_clones_M_alpha.tsv', 'alpha'), 
                    ('contracting_clones_M_beta.tsv',  'beta'),
                    ('contracting_clones_W_alpha.tsv', 'alpha'), 
                    ('contracting_clones_W_beta.tsv',  'beta'),
                    ('expanding_clones_M_alpha.tsv',  'alpha'),
                    ('expanding_clones_M_beta.tsv',  'beta'),
                    ('expanding_clones_W_alpha.tsv',  'alpha'),
                    ('expanding_clones_W_beta.tsv', 'beta')]

# A quick way of importing these uncommon headers is to convert them to MIXCR fields
map_minervina_to_mixcr = \
    {'Rank':'cloneId',
    'Read.count':'cloneCount',
    'Read.proportion':'cloneFraction',
    'bestVGene': 'allVHitsWithScore',
    'bestDGene': 'allDHitsWithScore',
    'bestJGene':'allJHitsWithScore',
    'CDR3.nucleotide.sequence':'nSeqCDR3',
    'CDR3.amino.acid.sequence':'aaSeqCDR3',
    'refPoints':'refPoints'}

def prep_data(f, chain, dest = os.path.join('tcrdist','data', 'covid19')):
    fn =os.path.join(dest, f)
    df = pd.read_csv(fn, sep = "\t")
    df['bestVGene'] = df['bestVGene'].apply(lambda s : s + "*00")
    df['bestJGene'] = df['bestJGene'].apply(lambda s : s + "*00")
    df = df.rename(columns = map_minervina_to_mixcr)
    df.to_csv('dfmix.clns.txt', index = False, sep = "\t")
    dfmix = mixcr_to_tcrdist3(  chain = chain,
                                organism = "human",
                                clones_fn = 'dfmix.clns.txt')
    dfmix['tag'] = f
    return dfmix

# All files as dataframes
dfs = {(f,c): prep_data(f=f, chain = c) for f,c in files_and_chains}
all_beta = pd.concat([df for key,df in dfs.items() if key[1] == "beta"])
all_alpha = pd.concat([df for key,df in dfs.items() if key[1] == "alpha"])
all_beta.to_csv(os.path.join('tcrdist','data', 'covid19', 'Minervina_dynamic_beta_clones.tsv'), index = False, sep = "\t")
all_alpha.to_csv(os.path.join('tcrdist','data', 'covid19', 'Minervina_dynamic_alpha_clones.tsv'), index = False, sep = "\t")

