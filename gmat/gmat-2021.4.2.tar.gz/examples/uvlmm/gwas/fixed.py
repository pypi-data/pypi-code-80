import logging
from gmat.gmatrix import agmat
from gmat.uvlmm.gwas import fixed, fixed_min
logging.basicConfig(level=logging.INFO)
pheno_file = 'pheno'
bed_file = 'plink'
# id-id-value form
agmat_file = 'test'
#agmat2 = agmat(bed_file, out_file=agmat_file, inv=False, small_val=0.001, out_fmt='id_id_val')
fixed(pheno_file, bed_file, agmat_file, out_file='res0.txt', npart=20, maxiter0=100, maxiter1=10)
fixed(pheno_file, bed_file, agmat_file, out_file='res1.txt', npart=20, maxiter0=100, maxiter1=0)
#fixed_min(pheno_file, bed_file, agmat_file, out_file='res2.txt', npart=20)
