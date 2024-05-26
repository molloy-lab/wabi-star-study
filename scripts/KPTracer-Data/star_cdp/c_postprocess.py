import pandas
import treeswift as ts
import os
import shutil
import sys
import json

sys.path.append('../prepare')

from utilities import *
#assume only one outgroup 0 
def remove_outg(tree_path: str, output:str):
    with open(tree_path, 'r') as infile, open(output, 'w') as outfile:
        for line in infile:
             newick_trimmed = line.strip()[:-1]
             newick_trimmed = newick_trimmed[3:-1]
             outfile.write(newick_trimmed + ';\n')

def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/star_cdp'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
    

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
            
        pmap_file = os.path.join(cur_data_path, folder + '_eqclass.json')
        #pruned_tree = os.path.join(cur_res_path, 'star_cdp_one_sol.tre')
        pruned_tree = os.path.join(cur_res_path, 'consensus_star_cdp_strict_consensus.tre')
        if not os.path.exists(pruned_tree):
            print(f"Missing {pruned_tree}")
            continue

        with open(pmap_file, 'r') as pf:
            pmap = json.load(pf)

        data_prefix = folder 
        print(data_prefix)
        
        # no_outg_tree_path = os.path.join(cur_res_path, 'removed_outg_star_cdp_one_sol.tre')
        no_outg_tree_path = os.path.join(cur_res_path, 'removed_outg_consensus_star_cdp_strict_consensus.tre')
        if not os.path.exists(no_outg_tree_path):
            remove_outg(pruned_tree, no_outg_tree_path)

        # replaced_tree_path = os.path.join(cur_res_path, 'replaced_star_cdp_one_sol.tre')
        replaced_tree_path = os.path.join(cur_res_path, 'replaced_consensus_star_cdp_strict_consensus.tre')

        pruned_tree = from_newick_get_nx_tree(no_outg_tree_path)

        replaced_tree = tree_to_newick_eq_classes(pruned_tree, pmap)

        with open(replaced_tree_path, 'w') as rf:
            rf.write(f"{replaced_tree};")
            

if __name__ == '__main__':

    main()