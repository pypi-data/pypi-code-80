# 888    888 888             d8888        8888888b.  8888888888 .d8888b. 88888888888 8888888b.  8888888 .d8888b. 88888888888 8888888 .d88888b.  888b    888 
# 888    888 888            d88888        888   Y88b 888       d88P  Y88b    888     888   Y88b   888  d88P  Y88b    888       888  d88P" "Y88b 8888b   888 
# 888    888 888           d88P888        888    888 888       Y88b.         888     888    888   888  888    888    888       888  888     888 88888b  888 
# 8888888888 888          d88P 888        888   d88P 8888888    "Y888b.      888     888   d88P   888  888           888       888  888     888 888Y88b 888 
# 888    888 888         d88P  888        8888888P"  888           "Y88b.    888     8888888P"    888  888           888       888  888     888 888 Y88b888 
# 888    888 888        d88P   888 888888 888 T88b   888             "888    888     888 T88b     888  888    888    888       888  888     888 888  Y88888 
# 888    888 888       d8888888888        888  T88b  888       Y88b  d88P    888     888  T88b    888  Y88b  d88P    888       888  Y88b. .d88P 888   Y8888 
# 888    888 88888888 d88P     888        888   T88b 8888888888 "Y8888P"     888     888   T88b 8888888 "Y8888P"     888     8888888 "Y88888P"  888    Y888 
#
# December 18, 2020 
# Seattle, WA
from collections import defaultdict 
import os 
import pandas as pd
import re
# <path> where files reside
path = os.path.join('data-raw','2020-08-31-mira_tcr_by_epitope/')
# <all_files> list of all files
all_files = [f for f in os.listdir(path) if f.endswith('.tcrdist3.csv')]
# <restriction> list of tuples from Supporting Table S5: https://docs.google.com/spreadsheets/d/1WAmze6lir-v11odO-nYYbCiYVh8WhQh_vy2d1UPPKb0/edit#gid=942295061
restriction = 
[('m_55_524_ALR','A*01'),
('m_1_8260_HTT','A*01'),
('m_45_689_SYF','A*01'),
('m_10_2274_LSP','B*07'),
('m_155_59_RAR','B*07'),
('m_133_102_NQK','B*15'),
('m_48_610_YLQ','A*02'),
('m_111_146_AEI','A*11'),
('m_53_532_NYL','A*24'),
('m_90_216_GYQ','C*07'),
('m_140_92_NSS','A*01'),
('m_55_524_ALR','B*08'),
('m_183_39_RIR','A*03'),
('m_10_2274_LSP','C*07'),
('m_99_191_QEC','B*40'),
('m_155_59_RAR','C*07'),
('m_185_39_ASQ','B*15'),
('m_147_73_DLF','B*08'),
('m_110_148_ELI','B*44'),
('m_51_546_AYK','A*03'),
('m_44_697_FPP','B*35'),
('m_118_136_ALN','A*11'),
('m_176_44_SST','A*11'),
('m_30_1064_KAY','B*57'),
('m_192_31_FQP','B*15'),
('m_70_345_DTD','A*01')]
# <restrictions_dict> convert list to dictionary
restrictions_dict = defaultdict(list)
for k,v in restriction:
	restrictions_dict[k].append(v)
# Loop through all files to construct a Dataframe of only those with strongest evidence of HLA-restriction
cache = list()
for f in all_files:
	rgs = re.search(pattern ='(mira_epitope)_([0-9]{1,3})_([0-9]{1,6})_([A-Z]{1,3})', 
		string = f).groups()
	rgs4 = re.search(pattern ='(mira_epitope)_([0-9]{1,3})_([0-9]{1,6})_([A-Z]{1,4})', 
		string = f).groups()
	key3 = f'm_{rgs[1]}_{rgs[2]}_{rgs[3]}'
	key4 = f'm_{rgs4[1]}_{rgs4[2]}_{rgs4[3]}'
	setkey = f"M_{rgs[1]}"
	print(include := key3 in restrictions_dict.keys())
	alleles = restrictions_dict.get(key3)
	cache.append((setkey, key3, key4, f, int(rgs[1]), int(rgs[2]), include, alleles))
#    d88P      888      888                       888  .d888      Y88b    
#   d88P       888      888                       888 d88P"        Y88b   
#  d88P        888      888                       888 888           Y88b  
# d88P         88888b.  888  8888b.           .d88888 888888         Y88b 
# Y88b         888 "88b 888     "88b         d88" 888 888            d88P 
#  Y88b        888  888 888 .d888888         888  888 888           d88P  
#   Y88b       888  888 888 888  888         Y88b 888 888          d88P   
#    Y88b      888  888 888 "Y888888 88888888 "Y88888 888         d88P    
# <hla_df>
hla_df = pd.DataFrame(cache, columns = ['set', 'key3','key4','filename','set_rank','clones','hla_restricted','alleles']).\
	sort_values(['hla_restricted','clones'], ascending = True).\
	query('hla_restricted == True').reset_index(drop = True)
for ind,row in hla_df.iterrows():
	print(file := row['filename'])



