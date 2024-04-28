import treeswift as ts
from typing import List, Tuple, Dict
import json
import os
import io
import sys


sys.path.append('../prepare')
from utilities import *

def read_name_map(input:str, right2left=True) -> Dict[str,str]:
    nmap = {}

    with open(input, 'r') as fin:
        content = fin.read()
    lines = content.splitlines()

    for line in lines:
        [left, right] = line.split(',')
        if right2left:
            nmap[right] = left

        else:
            nmap[left] = right

    return nmap


def relabel_and_remove_outgroup(tre:ts.Tree, nmap:Dict[str, str]) -> ts.Tree:
    for leaf in tre.traverse_leaves():
        lab = leaf.label
        try:
            leaf.label = nmap[leaf.label]
        except KeyError:
            pass
   
    return tre.extract_tree_without(['ROOT0', 'ROOT1'])

def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    paup_exe = os.path.join(software_dir, 'paup4a168_centos64')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
        data_prefix = folder
        print(data_prefix)

        all_paup_res_path = os.path.join(cur_res_path, 'paup_trees.trees')
        replaced_back_all_tree_file = os.path.join(cur_res_path, 'replaced_paup.trees')
        eqclass_file = os.path.join(cur_data_path, folder + '_eqclass.json')
        
        with open(eqclass_file, 'r') as eqf:
            eqclass = json.load(eqf)

        if os.path.exists(all_paup_res_path):
                
            if not os.path.exists(replaced_back_all_tree_file) or True:
                with open(all_paup_res_path, 'r') as aprp, open(replaced_back_all_tree_file, 'w') as rbatf:
                    for line in aprp:
                        pruned_tre = from_newick_get_nx_tree(io.StringIO(line))
                        replaced_tre = tree_to_newick_eq_classes(pruned_tre, eqclass)
                        rbatf.write(f"{replaced_tre};\n")
                
                print(f'finised:{replaced_back_all_tree_file}')
        else:
            print(f'warnning: miss {all_paup_res_path}')
            
            
if __name__ == '__main__':

    main()