import os
import subprocess as sp
import sys
import json

sys.path.append('../prepare')

from utilities import *


def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/startle_nni'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
    
    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
            
        cmat_path = os.path.join(cur_data_path, folder + '_character_matrix.csv')

        nj_tree_path = os.path.join(cur_res_path, 'unpruned_nj.newick')
        pmap_file = os.path.join(cur_data_path, folder + '_eqclass.json')
        
        if not os.path.exists(nj_tree_path):
            continue

        with open(pmap_file, 'r') as pf:
            pmap = json.load(pf)

        data_prefix = folder 
        print(data_prefix)
        pruned_nj_tree_path = os.path.join(cur_res_path, "pruned_nj.newick")
        # if not os.path.exists(os.path.join(cur_res_path, "nj.newick")) or True:
        if not os.path.exists(pruned_nj_tree_path):
            unpruned_tree = from_newick_get_nx_tree(nj_tree_path)
            pruned_tree = prune_tree(unpruned_tree, pmap)
            nwk = tree_to_newick(pruned_tree)

            with open(pruned_nj_tree_path, 'w') as f:
                f.write(f"{nwk};")
            print(f'finished: {pruned_nj_tree_path}')
if __name__ == '__main__':

    main()