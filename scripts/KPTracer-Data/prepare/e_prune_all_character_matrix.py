import os
import numpy as np
import pandas as pd
import json
import sys

from utilities import *


def main():

    trees_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))), 'data')
    trees_dir = os.path.join(trees_dir, 'KPTracer-Data')

    folders = [f for f in os.listdir(trees_dir) if os.path.isdir(os.path.join(trees_dir, f))]
    for folder in folders:

        if folder in ['3513_NT_Mets', '3513_NT_All'] :
            continue

        target_dir = os.path.join(trees_dir, folder)

        pruned_matrix = os.path.join(target_dir, folder + '_pruned_character_matrix.csv')
        pruned_tree_file = os.path.join(target_dir, folder + '_pruned_tree.nwk')
        eqclass = os.path.join(target_dir, folder + '_eqclass.json')
        # eq_upto_miss = os.path.join(target_dir, folder + '_eqclass_upto_miss.csv')
        # pruned_upto_miss_character_matrix = os.path.join(target_dir, folder + '_pruned_upto_miss_character_matrix.txt')
        # pruned_upto_miss_tree = os.path.join(target_dir, folder + '_pruned_upto_miss_tree.nwk')
        
        cmat_name = folder + '_character_matrix.csv'
        tree_name = folder + '_tree.nwk'
        tree = os.path.join(target_dir, tree_name)
        cmat = os.path.join(target_dir, cmat_name)
        cmat = pd.read_csv(cmat,index_col=[0], sep=',', dtype=str)
        
        eq_class, cmat = compute_equivalence_classes(cmat)
        
        # tree = from_newick_get_nx_tree(tree)
       
        # tree = prune_tree(tree, set(eq_class.keys()))
        
        with open(eqclass, 'w') as ef:
            json.dump(eq_class, ef)

        cmat.to_csv(pruned_matrix, sep=',')

        # newick_tree = tree_to_newick(tree)

        # with open(pruned_tree_file, 'w') as pf:
        #     pf.write(f"{newick_tree};")

        # print("Finished pruning " + folder)
        
    print("Finished pruning for all character matirx and cassiopeia trees")
    
    


if __name__ == "__main__":
    main()