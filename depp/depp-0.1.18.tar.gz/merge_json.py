#!/usr/bin/python

import json
import argparse

parser = argparse.ArgumentParser(description='test')
parser.add_argument('--asv', type=str)
parser.add_argument('--out-dir', type=str)
args = parser.parse_args()

output_dir = f'{args.out_dir}/summary/{args.asv}'

with open(f'{output_dir}/summary/{args.asv}_placement.jplace', 'r') as f:
    tree1 = json.load(f)

with open(f'{output_dir}/summary/marker_genes_placement.jplace', 'r') as f:
    tree2 = json.load(f)

tree1['placements'] += tree2['placement2']

with open(f'mags_{args.asv}.jplace', 'w') as f:
    json.dump(tree1, f)