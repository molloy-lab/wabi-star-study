import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction




def write_to_nexus(paup_file, opt_trees_file, consensus_tree_file):
    # Note - 
    # irreversible (Camin-Sokal); up means higher numbers are derived
    # you can use weight set of integers...
    # I can probably do round to second decimal and take base 100 weights
    with open(paup_file, 'w') as fp:
        fp.write("#NEXUS\n")
        fp.write("BEGIN PAUP;\n")
        fp.write("set maxtrees=510;\n")
        fp.write("set autoclose=yes warntree=no warnreset=no;\n")
        fp.write(f"gettrees file={opt_trees_file};\n")
        fp.write(f"contree all/strict=yes treefile={consensus_tree_file}")
        fp.write(" format=newick;\n")
        fp.write("END;\n")





def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle-sim"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    folders = [f for f in folders if f.split("-")[0]=='nlin_50' and f.split("-")[1]!='ncas_20']

    # score_pattern = r"small parsimony score = ([\d.]+)"


    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
        reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]
        
        num_reps = len(reps)

        for rep in reps:
            
            cur_res_rep_path = os.path.join(cur_res_path, rep)

            
            opt_trees_dir = os.path.join(cur_res_rep_path, 'optimal_trees')
            
            all_opt_trees_file = os.path.join(cur_res_rep_path, 'all_paup_opt_trees.newicks')
            data_prefix = folder + "/"+rep
            print(data_prefix)
            write_to_nexus(os.path.join(cur_res_rep_path, 'paup_consensus.nex'), all_opt_trees_file, os.path.join(cur_res_rep_path, 'strict_consensus.tre'))
            
            
               
if __name__ == '__main__':

    main()