import pandas
import treeswift as ts
import os
import shutil
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
            
        cmat_path = os.path.join(cur_data_path, folder + '_pruned_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')

        pmap_file = os.path.join(cur_data_path, folder + '_eqclass.json')
        pruned_tree = os.path.join(cur_res_path, 'original_cmat_to_nj_nni_tree.newick')

        if not os.path.exists(pruned_tree):
            print(f'missing: {[pruned_tree]}')
            continue

        with open(pmap_file, 'r') as pf:
            pmap = json.load(pf)
        
        data_prefix = folder 
        print(data_prefix)
        
        replaced_tree_path = os.path.join(cur_res_path, 'replaced_original_cmat_to_nj_nni_tree.newick')

        pruned_tree = from_newick_get_nx_tree(pruned_tree)

        replaced_tree = tree_to_newick_eq_classes(pruned_tree, pmap)

        with open(replaced_tree_path, 'w') as rf:
            rf.write(f"{replaced_tree};")
            

if __name__ == '__main__':

    main()