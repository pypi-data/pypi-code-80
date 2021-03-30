"""
test_ecdf_upgrade.py
--------------------
test_that neighbors.compute_ecdf produces equivalent output as ecdf.distance_ecdf
"""

"""
>>> compute_ecdf(data = np.array([1,2,3,4,5,6]), counts =np.array([100,100,100,100,100,100]), thresholds = np.array([3]))
array([0.5])
>>> compute_ecdf(data = np.array([1,2,3,4,5,6]), weights =np.array([1,1,1,1,1,1]), counts =np.array([100,100,100,100,100,100]), thresholds = np.array([3]))
array([0.5])
>>> compute_ecdf(data = np.array([1,2,3,4,5,6]), weights =np.array([10,1,1,1,1,1]), counts =np.array([100,100,100,100,100,100]), thresholds = np.array([3]))
array([0.8])
"""

from tcrdist.ecdf import distance_ecdf
_,new_method = distance_ecdf(pwrect= tr.rw_beta, thresholds = range(0,26,2))
_,new_method_weighted = distance_ecdf(pwrect= tr.rw_beta, weights = [.001]*tr.rw_beta.shape[1],  thresholds = range(0,26,2), absolute_weight = False)
_,new_method_weighted_abosolute = distance_ecdf(pwrect= tr.rw_beta, weights = [.001]*tr.rw_beta.shape[1],  thresholds = range(0,26,2), absolute_weight = True)

new_method_weighted.sum()
new_method_weighted_abosolute.sum()


from tcrdist.neighbors import compute_population_estimate_ecdf
old_method_weighted = np.array([compute_population_estimate_ecdf(data = tr.rw_beta[i,:], weights = [.001]*tr.rw_beta.shape[1], thresholds = np.array(range(26))) for i in range(tr.rw_beta.shape[0])])
old_method_weighted.sum()




a = compute_ecdf(data = tr.pw_beta, thresholds = list(range(26)))
assert np.all(a == np.array([0.5, 0.5]))



# NEW METHOD, WILL ACCOMODATE SPARSE
from tcrdist.ecdf import distance_ecdf
# CRAPY OLD METHOD
from tcrdist.neighbors import compute_ecdf
def test_upgrade_without_weights():
	_,new_method = distance_ecdf(pwrect= tr.pw_beta, thresholds = range(26))
	old_method = np.array([compute_ecdf(data = tr.pw_beta[i,:], thresholds = np.array(range(26))) for i in range(tr.pw_beta.shape[0])])
	assert np.all(new_method == old_method)

def test_upgrade_with_weights():
	_,new_method_unweighted = distance_ecdf(pwrect= tr.pw_beta, weights = [1]*tr.pw_beta.shape[0],  thresholds = range(26))
	_,new_method_weighted = distance_ecdf(pwrect= tr.pw_beta, weights = [.001]*tr.pw_beta.shape[0],  thresholds = range(26))
	old_method_weighted = np.array([compute_ecdf(data = tr.pw_beta[i,:], weights = [.001]*tr.pw_beta.shape[0], thresholds = np.array(range(26))) for i in range(tr.pw_beta.shape[0])])
	new_method_unweighted = np.array([compute_ecdf(data = tr.pw_beta[i,:], weights = [.001]*tr.pw_beta.shape[0], thresholds = np.array(range(26))) for i in range(tr.pw_beta.shape[0])])

	assert np.all(new_method == old_method)



def test_distance_ecdf():
	import numpy as np 
	from tcrdist.neighbors import compute_population_estimate_ecdf
	from tcrdist.ecdf import distance_ecdf
	rw_mat = np.array([[1,2,3,4,5,6],[2,4,6,8,10,12],[2,4,8,16,32,64]])
	# NO WEIGHTS, METHODS SHOULD AGREE :
	_, new_method_unweighted    = distance_ecdf(pwrect= rw_mat, thresholds = range(0,10), absolute_weight = False)
	_, new_method_unweighted_ab = distance_ecdf(pwrect= rw_mat, thresholds = range(0,10), absolute_weight = True)
	old_method_unweighted = np.array([compute_ecdf(data = rw_mat[i,:], thresholds = np.array(range(0,10))) for i in range(rw_mat.shape[0])] )
	old_method2_unweighted = np.array([compute_population_estimate_ecdf(data = rw_mat[i,:], thresholds = np.array(range(0,10))) for i in range(rw_mat.shape[0])] )
	expected = np.array( 
		[[0.        , 0.16666667, 0.33333333, 0.5       , 0.66666667,
		0.83333333, 1.        , 1.        , 1.        , 1.        ],
		[0.        , 0.        , 0.16666667, 0.16666667, 0.33333333,
		0.33333333, 0.5       , 0.5       , 0.66666667, 0.66666667],
		[0.        , 0.        , 0.16666667, 0.16666667, 0.33333333,
		0.33333333, 0.33333333, 0.33333333, 0.5       , 0.5       ]])
	assert np.all( np.isclose(expected, new_method_unweighted    ))
	assert np.all( np.isclose(expected, new_method_unweighted_ab ))
	assert np.all( np.isclose(expected, old_method_unweighted    ))
	assert np.all( np.isclose(expected, old_method2_unweighted   ))
	# WEIGHTS, METHOD SHOULD DIVERGE BY FACTOR IN UNIFORM WEIGHTS: 
	_, new_method_weighted    = distance_ecdf(pwrect= rw_mat, weights = [0.1]*rw_mat.shape[1] , thresholds = range(0,10), absolute_weight = False)
	_, new_method_weighted_ab = distance_ecdf(pwrect= rw_mat, weights = [0.1]*rw_mat.shape[1], thresholds = range(0,10), absolute_weight = True)
	old_method_weighted = np.array([compute_ecdf(data = rw_mat[i,:], weights = [0.1]*rw_mat.shape[1], thresholds = np.array(range(0,10))) for i in range(rw_mat.shape[0])] )
	old_method2_unweighted = np.array([compute_population_estimate_ecdf(data = rw_mat[i,:], weights = [0.1]*rw_mat.shape[1], thresholds = np.array(range(0,10))) for i in range(rw_mat.shape[0])] )
	assert np.all( np.isclose(expected, new_method_weighted    ))
	assert np.all( np.isclose(0.1 *expected, new_method_weighted_ab    ))
	assert np.all( np.isclose(expected, old_method_weighted    ))
	assert np.all( np.isclose(0.1*expected, old_method2_unweighted   ))


# How About a real example
import os
import numpy as np
import pandas as pd
from tcrdist.repertoire import TCRrep
from tcrdist.neighbors import compute_population_estimate_ecdf
from tcrdist.ecdf import distance_ecdf
project_path = os.path.join('tutorial')
source_path = os.path.join('tcrdist','data','covid19')
antigen_enriched_background_file = 'mira_epitope_55_524_ALRKVPTDNYITTY_KVPTDNYITTY.tcrdist3.csv'
assert os.path.isfile(os.path.join(source_path, antigen_enriched_background_file))
	# Read file into a Pandas DataFrame <df>
df = pd.read_csv(os.path.join(source_path, antigen_enriched_background_file))
	# Drop cells without any gene usage information
df = df.query("v_b_gene.notna() & j_b_gene.notna()")
	# Provide a counts column if non is present
df['count'] = 1
	# Initialize a TCRrep class, using ONLY columns that are complete and unique define a a clone.
	# Counts of identical 'clones' will be aggregated into a TCRrep.clone_df.
tr = TCRrep(cell_df = df[['cdr3_b_aa', 'v_b_gene', 'j_b_gene', 'subject','count']], 
			organism = "human", 
			chains = ['beta'], 
			compute_distances = True)


X = np.load(file =os.path.join(project_path, 'tr_rw_beta.npy'))
tr.rw_beta = X

_, new_method_weighted    = distance_ecdf(pwrect= tr.rw_beta, weights = [0.1]*tr.rw_beta.shape[1] , thresholds = range(0,30,2), absolute_weight = False)
_, new_method_weighted_ab = distance_ecdf(pwrect= tr.rw_beta, weights = [0.1]*tr.rw_beta.shape[1],  thresholds = range(0,30,2), absolute_weight = True)
assert np.all(np.isclose(new_method_weighted, 10*new_method_weighted_ab))
old_method2_unweighted = np.array([compute_population_estimate_ecdf(data = tr.rw_beta[i,:], thresholds = np.array(range(0,30,2))) for i in range(tr.rw_beta.shape[0])] )
old_method2_weighted = np.array([compute_population_estimate_ecdf(data = tr.rw_beta[i,:], weights = [0.1]*tr.rw_beta.shape[1], thresholds = np.array(range(0,30,2))) for i in range(tr.rw_beta.shape[0])] )
assert np.all(np.isclose(old_method2_unweighted , 10*old_method2_weighted))

df_bkgd = pd.read_csv(os.path.join(project_path, f"{antigen_enriched_background_file}.olga100K_brit100K_bkgd_2.csv"), sep = ",")
	# Load the background to a TCRrep without computing pairwise distances (i.e., compute_distances = False)
tr_bkgd = TCRrep(cell_df = df_bkgd, organism = "human", chains = ['beta'], compute_distances = False)
tr_bkgd.clone_df.weights

_, new_method_weighted_ab = distance_ecdf(pwrect= tr.rw_beta, weights = tr_bkgd.clone_df.weights,  thresholds = range(0,30,2), absolute_weight = True)
old_method2_weighted = np.array([compute_population_estimate_ecdf(data = tr.rw_beta[i,:], weights = tr_bkgd.clone_df.weights, thresholds = np.array(range(0,30,2))) for i in range(tr.rw_beta.shape[0])] )
assert np.all(np.isclose(new_method_weighted_ab , old_method2_weighted))
# Next try sparse
import scipy.sparse
tr.rw_beta == 0 

rw_beta = tr.rw_beta.copy()
rw_beta[rw_beta == 0] = 1
sparse_rw_beta = scipy.sparse.csr_matrix(rw_beta)
tr_bkgd.clone_df.weights

_, new_method_weighted_ab = distance_ecdf(pwrect= rw_beta,weights = tr_bkgd.clone_df.weights,  thresholds = np.array(range(1,30,5)), absolute_weight = True)
_, new_method_weighted_ab_on_sparse = distance_ecdf(pwrect= sparse_rw_beta, weights = tr_bkgd.clone_df.weights,  thresholds = np.array(range(1,30,5)), absolute_weight = True)
assert (np.isclose(new_method_weighted_ab_on_sparse , new_method_weighted_ab )).sum()/ new_method_weighted_ab.size == 1.0

rw_beta = tr.rw_beta.copy()
rw_beta[rw_beta == 0] = 1
rw_beta[rw_beta >= 50] = 0
sparse_rw_beta2 = scipy.sparse.csr_matrix(rw_beta)
_, new_method_weighted_ab_on_sparse2 = distance_ecdf(pwrect= sparse_rw_beta2, weights = tr_bkgd.clone_df.weights,  thresholds = np.array(range(1,30,5)), absolute_weight = True)

assert (np.isclose(new_method_weighted_ab_on_sparse2 , new_method_weighted_ab_on_sparse  )).sum()/ new_method_weighted_ab_on_sparse.size == 1.0











source_path = os.path.join('tcrdist','data','covid19')
antigen_enriched_background_file = 'mira_epitope_55_524_ALRKVPTDNYITTY_KVPTDNYITTY.tcrdist3.csv'
assert os.path.isfile(os.path.join(source_path, antigen_enriched_background_file))
	# Read file into a Pandas DataFrame <df>
df = pd.read_csv(os.path.join(source_path, antigen_enriched_background_file))
	# Drop cells without any gene usage information
df = df.query("v_b_gene.notna() & j_b_gene.notna()")
	# Provide a counts column if non is present
df['count'] = 1
	# Initialize a TCRrep class, using ONLY columns that are complete and unique define a a clone.
	# Counts of identical 'clones' will be aggregated into a TCRrep.clone_df.
tr = TCRrep(cell_df = df[['cdr3_b_aa', 'v_b_gene', 'j_b_gene', 'subject','count']], 
			organism = "human", 
			chains = ['beta'], 
			compute_distances = True)
X = np.load(file =os.path.join(project_path, 'tr_rw_beta.npy'))





















def distance_ecdf(pwrect, thresholds=None, weights=None, pseudo_count=0, skip_diag=False):
    """Computes the empirical cumulative distribution function (ECDF) for
    each TCR in a set of target TCRs [rows of pwrect] as the proportion
    of reference TCRs [columns of pwrect] within a distance radius less
    than or equal to a threhold d_i, over a range of
    D = [d_1, d_2, ..., d_i]. The distances between pairs of TCRs in the
    target and reference set are contained in the elements of pwrect.

    Optionally, relative weights can be supplied for each reference TCR.
    These can be TCR counts or other weights andthe ECDF will still
    be a probability on [0, 1].

    Parameters
    ----------
    pwrect : np.ndarray or scipy.sparse.csr_matrix, (clone_df.shape[0], n_ref)
    thresholds : np.ndarray
        Vector of thresholds at which the ECDF should be evaluated.
        By default will use all unique values in pwrect.
    weights : np.ndarray or list, (clone_df.shape[0], )
        Relative weight of each TCR in the reference (column dimension of pwrect)
    pseudo_count : int
        Added to the numerator and denominator at each threshold
        to avoid zero. Useful if end goal is a log-scale plot.
    skip_diag : bool
        Skip counting the diagonal for computing ECDF of seqs against same seqs.
