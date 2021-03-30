


#This worked example shows a use of tcrdist3 to analyze CD8+ bulk dataset from Minervina et al 2020
#together with MIRA data from Nolan et al. 2020. Share this particular examples with Anastasia Minervina and Mikhail V. Pogorelyy 

#  .d8888b.                    888                               888b     d888          888    888                    888 
# d88P  Y88b                   888                               8888b   d8888          888    888                    888 
# 888    888                   888                               88888b.d88888          888    888                    888 
# 888        888  888 .d8888b  888888 .d88b.  88888b.d88b.       888Y88888P888  .d88b.  888888 88888b.   .d88b.   .d88888 
# 888        888  888 88K      888   d88""88b 888 "888 "88b      888 Y888P 888 d8P  Y8b 888    888 "88b d88""88b d88" 888 
# 888    888 888  888 "Y8888b. 888   888  888 888  888  888      888  Y8P  888 88888888 888    888  888 888  888 888  888 
# Y88b  d88P Y88b 888      X88 Y88b. Y88..88P 888  888  888      888   "   888 Y8b.     Y88b.  888  888 Y88..88P Y88b 888 
#  "Y8888P"   "Y88888  88888P'  "Y888 "Y88P"  888  888  888      888       888  "Y8888   "Y888 888  888  "Y88P"   "Y88888 
#
# You may just want to form meta-clonotypes quickly. For this you can find 
# background_controlling_radii, neighbors, and regex using some transparent functions.
# We provide this example for researchers intersted in implementing custom workflows.
from tcrdist.centers import calc_radii
from tcrdist.public import _neighbors_variable_radius, _neighbors_sparse_variable_radius
from tcrdist.regex import _index_to_regex_str
# Using the same methodology as above we can get radii based on background discovery rate
# <max_radii> list, <thresholds> np.array (1D), <ecdfs> np.array (2D)
max_radii, thresholds, ecdfs = calc_radii(
	tr = tr,
	tr_bkgd = tr_bkgd, 
	chain = 'beta', 
	ctrl_bkgd = 10**-5, 
	use_sparse = True, 
	max_radius=50, 
	chunk_size=100)
# We assign the <max_radii> to clone_df
tr.clone_df['radius'] = max_radii
# We get all the neighbors within the variable radius
tr.clone_df['neighbors'] = _neighbors_variable_radius(pwmat=tr.pw_beta, radius_list = tr.clone_df['radius'])
# We can also get all the neighbors in the bulk_background
tr.clone_df['unwanted_neighbors'] = _neighbors_sparse_variable_radius(csrmat=tr.rw_beta, radius_list = tr.clone_df['radius'])
# We count the number of neighbors
tr.clone_df['K_neighbors'] = tr.clone_df['neighbors'].apply(lambda x : len(x))
# We determine how many <nsubjects> are in the set of neighbors 
tr.clone_df['nsubject']  = tr.clone_df['neighbors'].\
		apply(lambda x: tr.clone_df['subject'].iloc[x].nunique())
# We determine publicity
tr.clone_df['qpublic']     = tr.clone_df['nsubject'].\
		apply(lambda x: x > 1)
# Now we can generate a regex quickly based on the set of neighbors, with each sequence in the Antigen-Enriched Rep as the centroid
tr.clone_df['regex'] = [_index_to_regex_str(
	ind = r['neighbors'], 
	clone_df = tr.clone_df, 
	pwmat = None, 
	col = 'cdr3_b_aa', 
	centroid = tr.clone_df['cdr3_b_aa'][i],
	ntrim = 3,
	ctrim = 2,
	max_ambiguity = 5) for i,r in tr.clone_df.iterrows()]
# Notice that the radii returned by this method are exactly the same as those returned by the 
# previous method. However, there is now much more information about how well the regex 
# and distance radius perfomed in terms of forming pure neigborhoods enriched with antigen-enriched clones.
assert np.all(centers_df['radius'] == max_radii)
#  .d8888b.                                                                 
# d88P  Y88b                                                                
# Y88b.                                                                     
#  "Y888b.   888  888 88888b.d88b.  88888b.d88b.   8888b.  888d888 888  888 
#     "Y88b. 888  888 888 "888 "88b 888 "888 "88b     "88b 888P"   888  888 
#       "888 888  888 888  888  888 888  888  888 .d888888 888     888  888 
# Y88b  d88P Y88b 888 888  888  888 888  888  888 888  888 888     Y88b 888 
#  "Y8888P"   "Y88888 888  888  888 888  888  888 "Y888888 888      "Y88888 
#                                                                       888 
#                                                                  Y8b d88P 
#                                                                   "Y88P" 
# this visual summary method plots all clones
from tcrdist.public import TCRpublic
tp = TCRpublic(
    tcrrep = tr, 
    output_html_name = os.path.join(project_path, f'{antigen_enriched_file}.quasi_public_clones.html'))
tp.report()






# 888888b.            888 888            .d8888b.                                    888      
# 888  "88b           888 888           d88P  Y88b                                   888      
# 888  .88P           888 888           Y88b.                                        888      
# 8888888K.  888  888 888 888  888       "Y888b.    .d88b.   8888b.  888d888 .d8888b 88888b.  
# 888  "Y88b 888  888 888 888 .88P          "Y88b. d8P  Y8b     "88b 888P"  d88P"    888 "88b 
# 888    888 888  888 888 888888K 888888      "888 88888888 .d888888 888    888      888  888 
# 888   d88P Y88b 888 888 888 "88b      Y88b  d88P Y8b.     888  888 888    Y88b.    888  888 
# 8888888P"   "Y88888 888 888  888       "Y8888P"   "Y8888  "Y888888 888     "Y8888P 888  888 


############################################################################
# Step 6A: Against Dynamic Clones #########################################
############################################################################
# Minervina et al. previously idenfified clones that are extracting or expanding


############################################################################
# Step 6B: Against Bulk Data 5: Output Meta-Clonotypes Summary ##############
############################################################################





#####################################################################################
# Optional Step 7: Higher Performance Computing Example #############################
#####################################################################################
# Ideally, using a more powerful computer with a big FAN!
import os 
import re
import pandas as pd
import numpy as np
from tcrdist.repertoire import TCRrep
from tcrdist.public import _neighbors_sparse_variable_radius, _neighbors_sparse_fixed_radius, _neighbors_variable_radius, _neighbors_fixed_radius
df1 = pd.read_csv('/fh/fast/gilbert_p/fg_data/tcrdist/minervina/min_search_cd8.tsv', sep = "\t")
tr1 = TCRrep(cell_df = df1[['cdr3_b_aa', 'v_b_gene', 'j_b_gene', 'pgen', 'radius', 'nsubject', 'tag']], organism = 'human', chains = ['beta'], compute_distances = False)
df2 = pd.read_csv('/fh/fast/gilbert_p/fg_data/tcrdist/minervina/mincd8.tsv', sep = "\t")
tr2 = TCRrep(cell_df = df2[['count', 'fraction', 'v_b_gene', 'j_b_gene', 'cdr3_b_aa', 'tag','subject', 'days', 'cell_type', 'chain']], organism = 'human', chains = ['beta'], compute_distances = False)
#tr1.cpus = 10
#tr1.compute_sparse_rect_distances(df = tr1.clone_df, df2 = tr2.clone_df, chunk_size = 100, radius = 36)
import scipy.sparse
tr1.rw_beta = scipy.sparse.load_npz("mincd8_radius38.sparse.npz")
tr1.clone_df['neighbors18'] = _neighbors_sparse_fixed_radius(tr1.rw_beta, radius = 18 )
tr1.clone_df['K_neighbors18'] = tr1.clone_df['neighbors18'].apply(lambda x : len(x))
tr1.clone_df['neighbors'] = _neighbors_sparse_variable_radius(tr1.rw_beta, radius_list = tr1.clone_df['radius'])
tr1.clone_df['K_neighbors'] = tr1.clone_df['neighbors'].apply(lambda x : len(x))
# We are going to create a feature tag
tr1.clone_df['feature'] = tr1.clone_df.v_b_gene + "+" + tr1.clone_df.cdr3_b_aa + "+"+ tr1.clone_df['radius'].apply(lambda x : str(x))
discovered_clones = [tr2.clone_df.iloc[x,].copy() for x in tr1.clone_df.query("K_neighbors > 0").neighbors]
query_tags = tr1.clone_df.query("K_neighbors > 0").tag
query_feature = tr1.clone_df.query("K_neighbors > 0").feature
for x,t,f in zip(discovered_clones, query_tags, query_feature):
	x['tag'] = t
	x['feature'] = f
all_discovered = pd.concat(discovered_clones).reset_index(drop = True)
all_discovered.to_csv("minervina_cd8_all_discovered_radius_E5.tsv", index = False, sep = "\t")
discovered_clones18 = [tr2.clone_df.iloc[x,].copy() for x in tr1.clone_df.query("K_neighbors18 > 0").neighbors]
query_tags = tr1.clone_df.query("K_neighbors18 > 0").tag
query_feature = tr1.clone_df.query("K_neighbors18 > 0").feature
for x,t,f in zip(discovered_clones18, query_tags, query_feature):
	x['tag'] = t
	x['feature'] = f
all_discovered18 = pd.concat(discovered_clones18).reset_index(drop = True)
all_discovered18.to_csv("minervina_cd8_all_discovered_radius18.tsv", index = False, sep = "\t")

dfregex = pd.read_csv('/fh/fast/gilbert_p/fg_data/tcrdist/minervina/min_search_cd8_wregex.tsv', sep = "\t")
dfregex['feature'] = dfregex.v_b_gene + "+" + dfregex.cdr3_b_aa + "+"+ dfregex['radius'].apply(lambda x : str(x))
all_discovered_regex = all_discovered.merge(dfregex[['feature', 'tag', 'regex']], how = "left", on = ['feature', 'tag'])
all_discovered_regex['motif'] = [re.search(string = r['cdr3_b_aa'], pattern = r['regex']) is not None for _,r in all_discovered_regex.iterrows()]
all_discovered_regex.to_csv("minervina_cd8_all_discovered_radius_E5_motif.tsv", index = False, sep = "\t")

all_discovered_regex18 = all_discovered18.merge(dfregex[['feature', 'tag', 'regex']], how = "left", on = ['feature', 'tag'])
all_discovered_regex18['motif'] = [re.search(string = r['cdr3_b_aa'], pattern = r['regex']) is not None for _,r in all_discovered_regex18.iterrows()]
all_discovered_regex18.to_csv("minervina_cd8_all_discovered_radius18_motif.tsv", index = False, sep = "\t")














"""
FOR TREES
# Save the clones_df for future use
tr.clone_df.to_csv(os.path.join(project_path, f'{antigen_enriched_file}.clone_df.tsv'), sep = "\t" )
X = pd.DataFrame(tr.pw_beta)
pd.concat([tr.clone_df, X], axis = 1).to_csv("R48.tsv", sep = "\t")
"""


"""
########################################
### FUNCTIONS FOR OPENING MANY FILES ###
########################################
"""
import os 
import re
import pandas as pd
import numpy as np
from tcrdist.repertoire import TCRrep
from tcrdist.public import _neighbors_sparse_variable_radius, _neighbors_variable_radius, _neighbors_fixed_radius
def all_files(dest, suffix = ".tsv"):
	"""get all files in a <dest> : str with some <suffix> : str """
	return [f for f in os.listdir(dest) if f.endswith(suffix)]
def read_and_tag(dest,f,sep):
	"""reads a <f> : str filename in <dest> : str path to Dataframe, tagging it with filename so that it can be tracked when it is concatenated with other dataframes"""
	df = pd.read_csv(os.path.join(dest, f), sep = sep); df['tag'] = f; return df;
def collapse_files(dest, files, sep = "\t"):
	"""Combine many files in a dest folder"""
	dfs = [read_and_tag(dest, f, sep = sep) for f in files]; return pd.concat(dfs);
def _valid_cdr3(cdr3):
    """
    Examples
    --------
    >>> _valid_cdr3("AAAA")
    True
    >>> _valid_cdr3("AA.A")
    False
    """
    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    valid = np.all([aa in amino_acids for aa in cdr3])
    return valid
"""
###############
### SEARCH ####
###############
Here we consider all pubic-metaclonotypes found from MIRA (Nolan et al. 2020 setting delta to 10^-5)
"""
# <folder> is full file path containing metaclonotypes
folder = '/Volumes/Samsung_T5/kmayerbl/tcr_data/ImmuneCODE-MIRA-Release002/adpt_mira_r2_ranked_centers_bE5ctrl'
# <fs> 
fs = all_files(dest = folder, suffix = ".tsv")
# <df> DataFrame containing 8298 metaclonotypes
df   = collapse_files(dest = folder, files = fs, sep = '\t')
df   = df[df.tag.apply(lambda x : re.search(string = x, pattern = '^mira_epitope_3[0-1][0-9]*') is None) ].reset_index(drop = True)
cols = ['cdr3_b_aa', 'v_b_gene', 'j_b_gene', 'pgen', 'max_radi','nsubject','tag', 'regex']
df   = df[cols].rename(columns = {'max_radi':'radius'})
df.to_csv('min_search_cd8_wregex.tsv', sep = "\t", index = False)
# 1. Load TCRrep to enable searching for previosly identified metaclonotypes
tr_search = TCRrep(cell_df = df, organism = 'human', chains = ['beta'], compute_distances = False)
# 2. Load the dynamic beta clones from Minervenia et al. (see tcrdist/data/covid19/clean_minervin)
dynamic_beta = pd.read_csv(os.path.join('tcrdist','data','covid19','Minervina_dynamic_beta_clones.tsv'), sep = "\t")
dynamic_beta = dynamic_beta[(dynamic_beta['v_b_gene'].notna() ) & (dynamic_beta['cdr3_b_aa'].notna())]
dynamic_beta = dynamic_beta.rename(columns = {'tag':'subject'})
tr_dynamic = TCRrep(cell_df = dynamic_beta[['count', 'v_b_gene', 'j_b_gene', 'cdr3_b_aa', 'subject']], organism = 'human', chains = ['beta'], compute_distances = False)
# 3. Are any of the metaclonotypes found in the dynamic set 
tr_search.compute_rect_distances(df = tr_search.clone_df, df2 = tr_dynamic.clone_df)
# 4. Which of the contrating and expanding clones match one of the MIRA meta-clonotypes
from tcrdist.public import _neighbors_sparse_variable_radius, _neighbors_variable_radius
tr_search.clone_df['neighbors'] = _neighbors_variable_radius(
    pwmat = tr_search.rw_beta, 
    radius_list = tr_search.clone_df['radius'])
tr_search.clone_df['K_neighbors']=tr_search.clone_df['neighbors'].apply(lambda x : len(x))
matching_dynamic_clones = [tr_dynamic.clone_df.iloc[x,].copy() for x in tr_search.clone_df.query("K_neighbors > 0").neighbors]
query_tags = tr_search.clone_df.query("K_neighbors > 0").tag
for x,t in zip(matching_dynamic_clones , query_tags):
	x['tag'] = t
all_matching_dynamic_clones = pd.concat(matching_dynamic_clones ).drop_duplicates().reset_index(drop = True)
#######################
### SEARCH IN BULK ####
#######################

# 5. Let's look at raw bulk data.

# Let's look at longitudinal CD8 trafjectories. 

fs_cd8  = all_files(dest = '/Volumes/Samsung_T5/kmayerbl/tcr_data/minervina/beta/CD8', suffix = ".txt")
dfs_cd8 = collapse_files(dest = '/Volumes/Samsung_T5/kmayerbl/tcr_data/minervina/beta/CD8', files = fs_cd8, sep = "\t")
dfs_cd8 = dfs_cd8[['cloneCount', 'cloneFraction', 'bestVGene', 'bestJGene', 'aaSeqCDR3','tag']].\
	rename(columns = {'cloneCount':'count', 
			'cloneFraction':'fraction',
			'bestVGene': 'v_b_gene', 
			'bestJGene': 'j_b_gene', 
			'aaSeqCDR3': 'cdr3_b_aa',
			'tag': 'tag'}).\
	reset_index(drop = True)
parts = pd.DataFrame(dfs_cd8.tag.str.split('_').tolist(), columns = ['subject','days','cell_type','chain'])
dfs_cd8=pd.concat([dfs_cd8, parts],1)
dfs_cd8['v_b_gene'] = dfs_cd8['v_b_gene'].apply(lambda x : f"{x}*01")
dfs_cd8['j_b_gene'] = dfs_cd8['j_b_gene'].apply(lambda x : f"{x}*01")
dfs_cd8['valid_cdr3_b_aa'] = dfs_cd8['cdr3_b_aa'].apply(lambda x : _valid_cdr3(x))
dfs_cd8 = dfs_cd8[(dfs_cd8['valid_cdr3_b_aa']) & (dfs_cd8['v_b_gene'].notna()) & (dfs_cd8['cdr3_b_aa'].apply(lambda x : len(x) >= 5))].reset_index(drop = True)
# Because this is a large number of clones, we use an approach that only stores distance <= 36 in a sparse representation
tr_cd8 = TCRrep(cell_df = dfs_cd8, organism = "human", chains = ['beta'], compute_distances = False)
tr_cd8.clone_df.shape
tr_search.cpus = 4
tr_search.compute_sparse_rect_distances(df = tr_search.clone_df, df2 = tr_cd8.clone_df, chunk_size = 10, radius = 36)


tr_meta_clonotypes.clone_df['neighbors']   = _neighbors_sparse_fixed_radius(csrmat = tr_meta_clonotypes.rw_beta , radius = 18)
tr_meta_clonotypes.clone_df['K_neighbors'] = tr_meta_clonotypes.clone_df['neighbors'].apply(lambda x : len(x))






# answer a very limited question:
def all_files(dest, suffix = ".tsv"):
	"""get all files in a <dest> : str with some <suffix> : str """
	return [f for f in os.listdir(dest) if f.endswith(suffix)]
def read_and_tag(dest,f,sep):
	"""reads a <f> : str filename in <dest> : str path to Dataframe, tagging it with filename so that it can be tracked when it is concatenated with other dataframes"""
	df = pd.read_csv(os.path.join(dest, f), sep = sep); df['tag'] = f; return df;
def collapse_files(dest, files, sep = "\t"):
	"""Combine many files in a dest folder"""
	dfs = [read_and_tag(dest, f, sep = sep) for f in files]; return pd.concat(dfs);

raw_fs = all_files(dest = '/Users/kmayerbl/TCRDIST/tcrdist3/data-raw/tcr_by_epitope', suffix = 'tcrdist3.csv')
all_tcrs = collapse_files(dest ='/Users/kmayerbl/TCRDIST/tcrdist3/data-raw/tcr_by_epitope', files= raw_fs, sep = "," )
all_tcrs['feature'] = all_tcrs['v_b_gene'] + "+" + all_tcrs['cdr3_b_aa']
k = all_tcrs[['feature', 'tag']].groupby('feature')['tag'].agg(['unique'])
k['k'] = k['unique'].apply(lambda x: len(x))
k.sort_values('k', ascending = False).query('k > 1').to_csv("multiplicity.tsv", sep = '\t')











# Load TCRrep to search dynamic clones
tr_search.compute_rect_distances(df2 = tr_dynamic.clone_df)

tr_search.clone_df['neighbors'] = _neighbors_variable_radius(
    pwmat = tr_search.rw_beta, 
    radius_list = tr_search.clone_df['radius'])
tr_search.clone_df['K_neighbors']=tr_search.clone_df['neighbors'].apply(lambda x : len(x))

discovered_clones = [tr_dynamic.clone_df.iloc[x,].copy() for x in tr_search.clone_df.query("K_neighbors > 0").neighbors]
query_tags = tr_search.clone_df.query("K_neighbors > 0").tag
for x,t in zip(discovered_clones, query_tags):
	x['tag'] = t
all_discovered = pd.concat(discovered_clones).drop_duplicates().reset_index(drop = True)








# Load the dynamic beta clones from Minervenia et al. (see tcrdist/data/covid19/clean_minervin)
dynamic_beta = pd.read_csv(os.path.join('tcrdist','data','covid19','Minervina_dynamic_beta_clones.tsv'), sep = "\t")
dynamic_beta = dynamic_beta[(dynamic_beta['v_b_gene'].notna() ) & (dynamic_beta['cdr3_b_aa'].notna())]
dynamic_beta = dynamic_beta.rename(columns = {'tag':'subject'})
tr_dynamic = TCRrep(cell_df = dynamic_beta[['count', 'v_b_gene', 'j_b_gene', 'cdr3_b_aa', 'subject']], organism = 'human', chains = ['beta'])

	# 1.  Full search against MIRA data
tr.compute_rect_distances(df = tr.clone_df, df2 = tr_dynamic.clone_df)
	# NOTE THERE ARE MANY MATCHES
np.sum(tr.rw_beta.min(axis = 1) <= 18)
	# 2. Search only the meta_clonotypes 
tr_meta_clonotypes = TCRrep(cell_df = ranked_centers_df[['v_b_gene', 'j_b_gene', 'cdr3_b_aa','max_radi','regex','pgen']].rename(columns = {'max_radi':'radius'}), organism = 'human', chains = ['beta'])
tr_meta_clonotypes.compute_rect_distances( df2 = tr_dynamic.clone_df)
np.sum(tr_meta_clonotypes.rw_beta.min(axis = 1) <= 18)


# Suppose you want to see the neigbors to each meta_clonotypes
from tcrdist.public import _neighbors_sparse_variable_radius, _neighbors_variable_radius, _neighbors_fixed_radius
tr_meta_clonotypes.clone_df['neighbors'] = _neighbors_variable_radius(
    pwmat = tr_meta_clonotypes.rw_beta, 
    radius_list = tr_meta_clonotypes.clone_df['radius'])
tr_meta_clonotypes.clone_df['neighbors18'] = _neighbors_fixed_radius(
    pwmat = tr_meta_clonotypes.rw_beta, 
    radius = 18)



#



# Quick Check
row_ind = (tr_meta_clonotypes.rw_beta.min(axis = 1) <= 18).tolist()
col_ind = (tr_meta_clonotypes.rw_beta.min(axis = 0) <= 18).tolist()
tr_meta_clonotypes.clone_df.iloc[row_ind, :]
tr_dynamic.clone_df.iloc[col_ind, :]






#
def all_files(dest, suffix = ".tsv"):
	"""get all files in a <dest> : str with some <suffix> : str """
	return [f for f in os.listdir(dest) if f.endswith(suffix)]

def read_and_tag(dest,f,sep):
	"""reads a <f> : str filename in <dest> : str path to Dataframe, 
	tagging it with filename so that it can be tracked when it is 
	concatenated with other dataframes"""
	df = pd.read_csv(os.path.join(dest, f), sep = sep)
	df['tag'] = f
	return df

def collapse_files(dest, files, sep = "\t"):
	"""Combine many files in a dest folder"""
	dfs = [read_and_tag(dest, f, sep = sep) for f in files]
	return pd.concat(dfs)


# Let's look at longitudinal CD8 trafjectories
fs_cd8 = all_files(dest = '/Volumes/Samsung_T5/kmayerbl/tcr_data/minervina/beta/CD8', suffix = ".txt")
dfs_cd8= collapse_files(dest = '/Volumes/Samsung_T5/kmayerbl/tcr_data/minervina/beta/CD8', files = fs_cd8, sep = "\t")

dfs_cd8 = dfs_cd8[['cloneCount', 'cloneFraction', 'bestVGene', 'bestJGene', 'aaSeqCDR3','tag']].\
	rename(columns = {'cloneCount':'count', 
			'cloneFraction':'fraction',
			'bestVGene': 'v_b_gene', 
			'bestJGene': 'j_b_gene', 
			'aaSeqCDR3': 'cdr3_b_aa',
			'tag': 'tag'}).\
	reset_index(drop = True)


def _valid_cdr3(cdr3):
    """
    Examples
    --------
    >>> _valid_cdr3("AAAA")
    True
    >>> _valid_cdr3("AA.A")
    False
    """
    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    valid = np.all([aa in amino_acids for aa in cdr3])
    return valid

parts = pd.DataFrame(dfs_cd8.tag.str.split('_').tolist(), columns = ['subject','days','cell_type','chain'])
dfs_cd8=pd.concat([dfs_cd8, parts],1)
dfs_cd8['v_b_gene'] = dfs_cd8['v_b_gene'].apply(lambda x : f"{x}*01")
dfs_cd8['j_b_gene'] = dfs_cd8['j_b_gene'].apply(lambda x : f"{x}*01")
dfs_cd8['valid_cdr3_b_aa'] = dfs_cd8['cdr3_b_aa'].apply(lambda x : _valid_cdr3(x))
dfs_cd8 = dfs_cd8[(dfs_cd8['valid_cdr3_b_aa']) & (dfs_cd8['v_b_gene'].notna()) & (dfs_cd8['cdr3_b_aa'].apply(lambda x : len(x) >= 5))].reset_index(drop = True)


tr_cd8 = TCRrep(cell_df = dfs_cd8, organism = "human", chains = ['beta'], compute_distances = False)
tr_cd8.clone_df.shape
tr_meta_clonotypes.compute_sparse_distances
tr.cpus = 4
tr_meta_clonotypes.compute_sparse_rect_distances(df = tr_meta_clonotypes.clone_df, df2 = tr_cd8.clone_df)
from tcrdist.public import _neighbors_sparse_variable_radius, _neighbors_sparse_fixed_radius
tr_meta_clonotypes.clone_df['neighbors'] = _neighbors_variable_radius(
    pwmat = tr_meta_clonotypes.rw_beta, 
    radius_list = tr_meta_clonotypes.clone_df['radius'])

tr_meta_clonotypes.clone_df['neighbors'] = _neighbors_sparse_fixed_radius(csrmat = tr_meta_clonotypes.rw_beta , radius = 18)
tr_meta_clonotypes.clone_df['K_neighbors'] = tr_meta_clonotypes.clone_df['neighbors'].apply(lambda x : len(x))

discovered_clones_cd8 = [tr_cd8.clone_df.iloc[x,].copy() for x in tr_meta_clonotypes.clone_df.query("K_neighbors > 0").neighbors]
tr_meta_clonotypes.clone_df['feature'] = tr_meta_clonotypes.clone_df.v_b_gene + "+" + tr_meta_clonotypes.clone_df.cdr3_b_aa + "+"+ tr_meta_clonotypes.clone_df['radius'].apply(lambda x : str(x))
query_tags = tr_meta_clonotypes.clone_df.query("K_neighbors > 0")['feature']
for x,t in zip(discovered_clones_cd8, query_tags):
	x['tag'] = t
all_discovered_cd8 = pd.concat(discovered_clones_cd8).drop_duplicates().reset_index(drop = True)
all_discovered_cd8.to_csv("all_discovered_cd8_rc_MIRA48.tsv", sep = '\t', index = False)




# # From a directory of multiple .tsv files, create a DataFrame.
# r = '/Volumes/Samsung_T5/kmayerbl/tcr_data/ImmuneCODE-MIRA-Release002/adpt_mira_r2_ranked_centers_bE5ctrl'
# fs = all_files(dest = r, suffix = ".tsv")
# df = collapse_files(dest = r, files = fs, sep = '\t')
# # Load DataFrame to TCRrep to enable searching
cols = ['cdr3_b_aa', 'v_b_gene', 'j_b_gene', 'pgen', 'max_radi','nsubject','tag']
from tcrdist.repertoire import TCRrep
tr_search = TCRrep(cell_df = df[cols].rename(columns = {'max_radi':'radius'}), organism = 'human', chains = ['beta'], compute_distances = False)
tr_search.compute_rect_distances(df2 = tr_dynamic.clone_df)
tr_search.clone_df['neighbors'] = _neighbors_variable_radius(
    pwmat = tr_search.rw_beta, 
    radius_list = tr_search.clone_df['radius'])
tr_search.clone_df['K_neighbors']=tr_search.clone_df['neighbors'].apply(lambda x : len(x))

discovered_clones = [tr_dynamic.clone_df.iloc[x,].copy() for x in tr_search.clone_df.query("K_neighbors > 0").neighbors]
query_tags = tr_search.clone_df.query("K_neighbors > 0").tag
for x,t in zip(discovered_clones, query_tags):
	x['tag'] = t
all_discovered = pd.concat(discovered_clones).drop_duplicates().reset_index(drop = True)






row_ind = (tr_search.rw_beta.min(axis = 1) <= 18).tolist()
col_ind = (tr_search.rw_beta.min(axis = 0) <= 18).tolist()
tr_search.clone_df.iloc[row_ind, :]
tr_dynamic.clone_df.iloc[col_ind, :]





















	# Quantify these centers in a bulk un-enriched sample
from tcrdist.centers import centers_v_bulk
result_df, rw_beta_sparse, tr_search = centers_v_bulk(
	search_filename     = os.path.join(project_path, f'{antigen_enriched_file}.ranked_centers.tsv'), 
	bulk_filename       = os.path.join(project_path, 'KH20-09691_TCRB.tsv.tcrdist3.v_max.tsv'), 
	sep_search_filename = "\t")

result_df.to_csv(os.path.join(project_path, f'{antigen_enriched_file}.results.tsv'), sep= "\t")
rw_beta_sparse.save(os.path.join(project_path, f'{antigen_enriched_file}.results.npy'))

np.sum(tr.rw_beta.min(axis = 1) <= 18)

result_df







# check counts against previously
check_df = pd.read_csv(os.path.join(project_path, 'check.csv'))
check_counts = result_df[['regex', 'cdr3_b_aa', 'v_b_gene', 'j_b_gene', 'bulk_sum_templates_regex_adj']].\
	merge(check_df, how = "left", on = ['regex', 'cdr3_b_aa', 'v_b_gene', 'j_b_gene'])
check_counts[check_counts.bulk_sum_templates_regex_adj_y.notna()].bulk_sum_templates_regex_adj_x
assert check_counts[check_counts.bulk_sum_templates_regex_adj_y.notna()].shape[0] >= 42
assert np.all(check_counts[check_counts.bulk_sum_templates_regex_adj_y.notna()].bulk_sum_templates_regex_adj_x == check_counts[check_counts.bulk_sum_templates_regex_adj_y.notna()].bulk_sum_templates_regex_adj_y)

# (Doveryai, no proveryai)





