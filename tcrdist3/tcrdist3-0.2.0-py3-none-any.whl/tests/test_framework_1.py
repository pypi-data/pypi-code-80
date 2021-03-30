"""
test_framework_1
"""
#def test_make_a_background():
"""
Example: Appropriate unenriched backgrounds and TCR-specific radii

Motivation: Generating an appropriate set of unenriched reference TCRs is
important. For each set of antigen-associated TCRs. We
created a two part antigen-naive background. First, we combine a set of 100,000
synthetic TCRs generated using the software OLGA (Sethna et al. 2019; Marcou et
al. 2018), whose V-gene and J-gene frequencies match those in the antigen
enriched repertoire. Second we used 100,00 umbilical cord blood TCRs sampled
uniformly from 8 subjects (Britanova et al., 2017). This mix balances dense
sampling of reference sequences nearby the biochemical neighborhoods of
interest with broad sampling of common TCR representative of antigen-naive
repertoire. Importantly, we adjust for the biased sampling by using the gene V
and J gene frequencies observed in the cord-blood data (see methods for details
about inverse probability weighting adjustment). Thus, we are able to estimate
the frequency of TCRs similar to a centroid TCR in an unenriched reference
repertoire down to 1 in 1 million TCRs, using a comparatively modest reference
dataset (200,000 TCRs). While this estimate may not reflect true specificity,
since some of the neighborhood TCRs in the unenriched reference repertoire may
in fact recognize the antigen of interest, it is useful for prioritizing
neighborhoods and selecting a radius that defines a useful meta-clonotype.
See: https://github.com/kmayerb/t3ms/blob/main/example/example_set_specific_background.py
Script: example_set_specific_background.py
Date: 2020-11-11
"""
import sys
import os
import numpy as np
import pandas as pd
from tcrdist.repertoire import TCRrep
from tcrsampler.sampler import TCRsampler
from tcrdist.background import make_gene_usage_counter, get_gene_frequencies, calculate_adjustment, make_gene_usage_counter
from tcrdist.background import make_vj_matched_background, make_flat_vj_background
from tcrdist.background import get_stratified_gene_usage_frequency
from tcrdist.background import sample_britanova
	#from tcrdist.sample import _default_sampler

	# Load a antigen-enriched (sub)repertoire.
source_path = os.path.join('tcrdist','data','covid19')
project_path = "tutorial"
if not os.path.isdir(project_path):
	os.mkdir(project_path)
antigen_enriched_background_file = 'mira_epitope_55_524_ALRKVPTDNYITTY_KVPTDNYITTY.tcrdist3.csv'
assert os.path.isfile(os.path.join(source_path, antigen_enriched_background_file))
	# Read file into a Pandas DataFrame <df>
df = pd.read_csv(os.path.join(source_path, antigen_enriched_background_file))
	# Drop cells without any gene usage information
df = df.query("v_b_gene.notna() & j_b_gene.notna()")
	# Provide a counts column if non is present
	# Initialize a TCRrep class, using ONLY columns that are complete and unique define a a clone.
	# Counts of identical 'clones' will be aggregated into a TCRrep.clone_df.
tr = TCRrep(cell_df = df[['subject','cell_type','v_b_gene', 'j_b_gene', 'cdr3_b_aa']], 
			organism = "human", 
			chains = ['beta'], 
			compute_distances = True)
	# Tip: Users of tcrdist3 should be aware that by default a <TCRrep.clone_df> DataFrame is created out of 
	# non-redundant cells in the cell_df, and pairwise distance matrices automatically computed.
	# Notice that attributes <tr.clone_df>  and  <tr.pw_beta> , <tr.pw_cdr3_b_aa>, are immediately accessible.
	# Attributes <tr.pw_pmhc_b_aa>, <tr.pw_cdr2_b_aa>, and <tr.pw_cdr1_b_aa>  
	# are also available if <TCRrep.store_all_cdr> is set to True.
	# For large datasets, i.e., >15,000 clones, this approach may consume to much memory 
	# so <TCRrep.compute_distances> should be set to False. 

# SAVE FOR PLOTTING
tr.clone_df.to_csv(os.path.join(project_path, f'{antigen_enriched_background_file}.clone_df.tsv'), sep = "\t" )
X = pd.DataFrame(tr.pw_beta)
pd.concat([tr.clone_df, X], axis = 1).to_csv("R55.tsv", sep = "\t")

	# Initialize a TCRsampler -- human, beta, umbilical cord blood from 8 people.
ts = TCRsampler(default_background = 'britanova_human_beta_t_cb.tsv.sampler.tsv')
	# Stratify sample so that each subject contributes similarly to gene usage frequency
ts = get_stratified_gene_usage_frequency(ts = ts, replace = True) 
	# Synthesize an inverse probability weighted V,J gene background that matches usage in your enriched repertoire 
df_vj_background = tr.synthesize_vj_matched_background(ts = ts, chain = 'beta')
	# Get a randomly drawn stratified sampler of beta, cord blood from Britanova et al. 2016 
	# Dynamics of Individual T Cell Repertoires: From Cord Blood to Centenarians
df_britanova_100K = sample_britanova(size = 100000)
	# Append frequency columns using, using sampler above
df_britanova_100K = get_gene_frequencies(ts = ts, df = df_britanova_100K)
df_britanova_100K['weights'] = 1
df_britanova_100K['source'] = "stratified_random"
	# Combine 
df_bkgd = pd.concat([df_vj_background.copy(), df_britanova_100K.copy()], axis = 0).\
	reset_index(drop = True)                                              
	# Assert that the backgrounds have the expected number of rows.
assert df_bkgd.shape[0] == 200000
	# Save df_bkgd for later use:


df_bkgd.to_csv(os.path.join(project_path, f"{antigen_enriched_background_file}.olga100K_brit100K_bkgd.csv"), index = False)

	# Load the archived background
df_bkgd = pd.read_csv(os.path.join(project_path, f"{antigen_enriched_background_file}.olga100K_brit100K_bkgd_2.csv"), sep = ",")
	# Load the background to a TCRrep without computing pairwise distances (i.e., compute_distances = False)
tr_bkgd = TCRrep(cell_df = df_bkgd, organism = "human", chains = ['beta'], compute_distances = False)
	# Compute rectangular distances between each clone in the 
	# antigen-enriched repertoire and each TCR in the background.
	# With a single 1 CPU and < 10GB, 5E2x2E5 = 100 million pairwise distances, across CDR1, CDR2, CDR2.5, and CDR3 
	# 1min 34s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each) 
	# %timeit -r 1 tr.compute_rect_distances(df = tr.clone_df, df2 = tr_bkdg.clone_df, store = False)
tr.compute_rect_distances(df = tr.clone_df, df2 = tr_bkgd.clone_df, store = False)
np.save(file =os.path.join(project_path, 'tr_rw_beta.npy'), arr =tr.rw_beta)
	# 30.8 s ± 0 ns per loop 
	# tr.cpus = 6
	# %timeit -r tr.compute_sparse_rect_distances(df = tr.clone_df, df2 = tr_bkdg.clone_df,radius=50, chunk_size=85)

	# Investigate the density of neighbors to each TCR, based on expanding distance radius.
from tcrdist.ecdf import distance_ecdf, make_ecdf_step, plot_ecdf
	# Compute empirical cumulative density function (ecdf)
	# Compare Antigen Enriched TCRs (against itself).
thresholds, antigen_enriched_ecdf = distance_ecdf(
	tr.pw_beta,
	thresholds=range(0,50,2))
	# Compute empirical cumulative density function (ecdf)
	# Compare Antigen Enriched TCRs (against) 200K probability inverse weighted background
thresholds, background_ecdf = distance_ecdf(
	tr.rw_beta,
	thresholds=range(0,50,2),
	weights= tr_bkgd.clone_df['weights'])

	# plot_ecdf for simple ecdf #
from tcrdist.ecdf import plot_ecdf
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10, 5))
ax = plt.subplot(1, 2, 1)
antigen_enriched_ecdf[antigen_enriched_ecdf == antigen_enriched_ecdf.min()] = 1E-10
plot_ecdf(thresholds, antigen_enriched_ecdf, ax, ylabel = f'Proportion of Antigen Enriched TCRs',  ylim = [1E-10, 1])
ax2 = plt.subplot(1, 2, 2)
plot_ecdf(thresholds, background_ecdf, ax2, ylabel = f'Proportion of Reference TCRs', ylim = [1E-10, 1])
fig.savefig(os.path.join(project_path, "F0.png"))
	# plot_ecdf similar to tcrdist3 manuscript #
from tcrdist.ecdf import _plot_manuscript_ecdfs
import matplotlib.pyplot as plt
antigen_enriched_ecdf[antigen_enriched_ecdf == antigen_enriched_ecdf.min()] = 1E-10
f1 = _plot_manuscript_ecdfs(thresholds, antigen_enriched_ecdf, ylab= 'Proportion of Antigen Enriched TCRs', cdr3_len=tr.clone_df.cdr3_b_aa.str.len(), min_freq=1E-10)
f1.savefig(os.path.join(project_path, "F1.png"))
f2 = _plot_manuscript_ecdfs(thresholds, background_ecdf, ylab= 'Proportion of Umbilical Cord Blood TCRs', cdr3_len=tr.clone_df.cdr3_b_aa.str.len(), min_freq=1E-10)
f2.savefig(os.path.join(project_path, "F2.png"))

	# TCR-specific radius
from tcrdist.centers import find_centers_beta
	# Compute radius specific distances that controls 
	# background neighbor discovery rate at 10^-5
	# <find_centers_beta()> is a procedure:
centers_df, rw_beta_sparse = \
	find_centers_beta(background_filename = os.path.join(project_path, f"{antigen_enriched_background_file}.olga100K_brit100K_bkgd.csv"),
					target_filename = os.path.join(source_path, antigen_enriched_background_file),
					ncpus = 4,
					min_nsubject = 2,
					ctrl_bkgd = 10**-5, 
					prefilter = False)
	# Save centers file to a .tsv file
centers_df.to_csv( os.path.join(project_path, f'{antigen_enriched_background_file}.centers_popweight.tsv'), sep = "\t" )
	# Ranks and get non-redundant centroid TCRs.
from tcrdist.centers import rank_centers
ranked_centers_df = rank_centers(
	centers_df = centers_df, 
	rank_column = 'chi2joint', 
	min_nsubject = 2, 
	min_nr = 1)

	# Save ranked centers file to a .tsv file
ranked_centers_df.to_csv( os.path.join(project_path, f'{antigen_enriched_background_file}.ranked_centers.tsv'), sep = "\t" )

	# Quantify these centers in a bulk un-enriched sample
from tcrdist.centers import centers_v_bulk
result_df, rw_beta_sparse, tr_search = centers_v_bulk(
	search_filename     = os.path.join(project_path, f'{antigen_enriched_background_file}.ranked_centers.tsv'), 
	bulk_filename       = os.path.join(project_path, 'KH20-09691_TCRB.tsv.tcrdist3.v_max.tsv'), 
	sep_search_filename = "\t")

result_df.to_csv(os.path.join(project_path, f'{antigen_enriched_background_file}.results.tsv'), sep= "\t")
rw_beta_sparse.save(os.path.join(project_path, f'{antigen_enriched_background_file}.results.npy'))

# check counts against previously
check_df = pd.read_csv(os.path.join(project_path, 'check.csv'))
check_counts = result_df[['regex', 'cdr3_b_aa', 'v_b_gene', 'j_b_gene', 'bulk_sum_templates_regex_adj']].\
	merge(check_df, how = "left", on = ['regex', 'cdr3_b_aa', 'v_b_gene', 'j_b_gene'])
check_counts[check_counts.bulk_sum_templates_regex_adj_y.notna()].bulk_sum_templates_regex_adj_x
assert check_counts[check_counts.bulk_sum_templates_regex_adj_y.notna()].shape[0] >= 42
assert np.all(check_counts[check_counts.bulk_sum_templates_regex_adj_y.notna()].bulk_sum_templates_regex_adj_x == check_counts[check_counts.bulk_sum_templates_regex_adj_y.notna()].bulk_sum_templates_regex_adj_y)

# OK THIS WORKS AND NOW, WE WANT TO MAKE AN ALTERNATIVE VERSION THAT CAN WORK WITH SPARSE RW_MATS
# 
# from tcrdist.centers import find_centers_beta
# from tcrdist.centers import centers_v_bulk

