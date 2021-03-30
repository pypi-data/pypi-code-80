import os
import pandas as pd
import re

__all__ = ['tabulate_gliph_group','get_gliph_df','tabulate_gliph_in_bulk','prep_bulk_df','tabulate_one_sample']

def tabulate_gliph_group(bulk_df,
	v_name = 'v_b_gene',
	j_name = 'j_b_gene',
	cdr3_name = 'cdr3_b_aa', 
	TRBV_list = ["TRBV28","TRBV19-1"],
	TRBJ_list = ["TRBJ2-7"],
	gliph = ".TDSY"):
	"""
	Unit function - tabulates a gliph group 
	in tcrdist formatted dataframe. The gliph group
	is definted as a set of feasible V and J genes with IMGT 
	nomenclature. 

	Parameters
	----------
	bulk_df : pd.DataFrame
		tcrdist3 formatted dataframe
	v_name : str
		V-Gene name for beta e.g., 'v_b_gene'
	j_name : str
		J-Gene name for beta e.g., j_b_gene',
	cdr3_name : str
		CDR3 names for beta, e.g., 'cdr3_b_aa', 
	TRBV_list : list
		List of all V-Gene names in the gliph group 
	TRBJ_list : list
		List of all J-Gene names in the gliph group 
	gliph : str
		Regular expression string such as ".TDSY"

	Returns
	-------
		pd.Series 
	
	Named after the gliph string and with indices matching the bulk_df 
	"""
	bulk_df_vj = bulk_df[ (bulk_df[v_name].isin(TRBV_list)) & (bulk_df[j_name].isin(TRBJ_list))].copy()
	bulk_df_vj[gliph] = bulk_df_vj[cdr3_name].apply(lambda x: int(re.search(string = x, pattern = gliph) != None))
	return bulk_df_vj[gliph].copy()

def get_gliph_df(gliph_file = "G55.tsv"):
	"""
	Creater a gliph df from the .tsv files output by GLIPH2
	"""
	gdf = pd.read_csv(gliph_file, sep = "\t")
	gdf = gdf[gdf['pattern'] != 'single']

	trvs   = list()
	trjs   = list()
	gliphs = list()
	sizes  = list()
	fscores  = list()

	for i,g in gdf.groupby(['pattern']):
		trvs.append(list(g.V.unique()))
		trjs.append(list(g.J.unique()))
		gliphs.append(i.replace('%', '.'))
		sizes.append(g.shape[0])
		fscores.append( g['Fisher_score'].to_list()[0])

	gliph_df = pd.DataFrame(
		{'trv' : trvs,
		'trj'  : trjs,
		'gliph': gliphs, 
		'size' : sizes, 
		'fscore': fscores})

	return(gliph_df.sort_values('fscore'))

def tabulate_gliph_in_bulk(gliph_df, bulk_df, sample_name):
	tabl = list()
	#eqivalent to for trv, trj, gliph in zip(trbvs, trbjs, gliphs):
	for i,r in gliph_df.iterrows():
		s = tabulate_gliph_group(bulk_df = bulk_df,
			TRBV_list = r['trv'],
			TRBJ_list = r['trj'],
			gliph     = r['gliph'])
		tabl.append(s)
	tabl_bulk_df = pd.concat([bulk_df, pd.concat(tabl, axis = 1)], axis = 1).fillna(0).copy()
	tabl_bulk_df_sum = tabl_bulk_df[gliph_df['gliph'].to_list()].transpose().dot(tabl_bulk_df[['templates','productive_frequency']])
	tabl_bulk_df_breadth = (tabl_bulk_df[gliph_df['gliph'].to_list()] > 0).sum()
	output_df = pd.concat([tabl_bulk_df_sum,tabl_bulk_df_breadth],axis = 1).reset_index()
	output_df.columns = ['gliph', 'templates', 'productive_frequency', 'breadth']
	output_df['sample'] = sample_name
	return(output_df)

def prep_bulk_df(bulk_fn):
	sample_name = os.path.basename(bulk_fn).replace('.tsv.tcrdist3.v_max.tsv', '')

	bulk_df = pd.read_csv(bulk_fn, sep = "\t")
	# clean to match gliph gene names without alelle
	bulk_df = bulk_df[['cdr3_b_aa','v_b_gene', 'j_b_gene', 'subject','productive_frequency','templates']]
	bulk_df = bulk_df[bulk_df['v_b_gene'].apply(lambda x : isinstance(x, str))]
	bulk_df = bulk_df[bulk_df['j_b_gene'].apply(lambda x : isinstance(x, str))]
	bulk_df['v_b_gene'] = bulk_df['v_b_gene'].apply(lambda x : x.split("*")[0])
	bulk_df['j_b_gene'] = bulk_df['j_b_gene'].apply(lambda x : x.split("*")[0])
	return bulk_df, sample_name

def tabulate_one_sample(bulk_fn, gliph_df):
	bulk_df, sample_name = prep_bulk_df(bulk_fn)
	res = tabulate_gliph_in_bulk(gliph_df = gliph_df, bulk_df = bulk_df, sample_name = sample_name)
	return res




def make_a_gliph_input(
	infile,
	outfile,
	cols= ['cdr3_b_aa','v_b_gene', 'j_b_gene', 'subject'],
	rename_dict = {'cdr3_b_aa':'#CDR3b', 'v_b_gene':'TRBV','j_b_gene' : 'TRBJ','subject': 'subject'}):
	"""
	Example
	-------
	import os
	import pandas
	resources = '/Volumes/Samsung_T5/kmayerbl/tcr_data/ImmuneCODE-MIRA-Release002/adpt_mira_r2_tcr_by_epitope'
	outsources = '/Volumes/Samsung_T5/kmayerbl/tcr_data/ImmuneCODE-MIRA-Release002/adpt_mira_r2_tcr_by_epitope/gliph/'
	fs = [f for f in os.listdir(resources) if f.endswith('.tcrdist3.csv')]
	for file in fs:
		make_a_gliph_input(
			infile = os.path.join(resources, file),
			outfile = os.path.join(outsources, f"{file}.gliph.tsv"))
	"""

	df = pd.read_csv(infile)[cols].rename(columns = rename_dict)
	df['count'] = 1 
	df.to_csv(outfile, sep = "\t", index =False)




	# MAKE A GLIPH INPUT	
	# f = os.path.join('tcrdist', 'data', 'covid19','mira_epitope_55_524_ALRKVPTDNYITTY_KVPTDNYITTY.tcrdist3.csv')
	# df = pd.read_csv(f)[['cdr3_b_aa','v_b_gene', 'j_b_gene', 'subject']]
	# df['count'] = 1 
	# df = df.rename(columns = {'cdr3_b_aa':'#CDR3b', 
	# 			'v_b_gene':'TRBV',
	# 			'j_b_gene' : 'TRBJ',
	# 			'subject': 'subject',
	# 			'count': 'count'})
	# df.to_csv('M55_gliph2_input.tsv', sep = "\t", index =False)


