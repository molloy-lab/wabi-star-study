import os
import subprocess as sp
import re
import dendropy
import sys

def main():
    sys.setrecursionlimit(4000)

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/startle_nni'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/scripts/KPTracer-Data"

    comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')

    consensus_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/star_cdp'

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    # folders = [f for f in folders if f.split("_")[1]=='50-ncas']

    print(folders)

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        

            
        cmat_path = os.path.join(cur_data_path, folder + '_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')
        # score_path = os.path.join(cur_res_rep_path, 'RF.csv')
        score_path = os.path.join(cur_res_path, 'contract_RF.csv')
        # score_path = os.path.join(cur_res_rep_path, 'consensus_RF.csv')
            
        true_tree_path = os.path.join(os.path.join(consensus_dir, folder), 'replaced_consensus_star_cdp_strict_consensus.tre')

        star_cdp_tree_path = tree_path = os.path.join(cur_res_path, 'replaced_nni_tree.newick')
        # consensus_tree_path = os.path.join(cur_res_rep_path, 'consensus_star_cdp_strict_consensus.tre')
        data_prefix = folder
        print(data_prefix)

        if not os.path.exists(star_cdp_tree_path):
            print(f"missing: {star_cdp_tree_path}")
            continue

        if not os.path.exists(score_path):
            score_res = sp.run(['python3', comp_exe, '-t1', true_tree_path, '-t2', star_cdp_tree_path, '-c1','1', '-c2', '1', '-m', cmat_path], capture_output=True, text=True)

            if score_res.returncode == 0:
                score_res = score_res.stdout
                print(score_res)
                [nl, i1, i2, fn, fp, fn_rate, fp_rate] = [float(x) for x in score_res.split(',')]
                print(f'{fn_rate}, {fp_rate}')

            else:
                print("%%")
                print(score_res.stderr)
                raise Exception("Failed to compute score for " + cur_res_path)

            
            with open(score_path, 'w', newline="") as score_file:
                score_file.write(f'{nl},{i1},{i2},{fn},{fp},{fn_rate},{fp_rate}\n')
                print(f'write {score_path}')
            #else:
                #os.remove(score_path)

if __name__ == '__main__':

    main()