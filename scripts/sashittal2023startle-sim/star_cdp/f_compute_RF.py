import os
import subprocess as sp
import re
import dendropy
import sys

def main():
    sys.setrecursionlimit(4000)

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result/star_cdp'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle-sim"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/scripts/sashittal2023startle-sim"

    comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')


    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    folders = [f for f in folders if f.split("_")[1]=='50-ncas']


    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
        reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]
        
        num_reps = len(reps)

        for rep in reps:
            cur_res_rep_path = os.path.join(cur_res_path, rep)
            if not os.path.exists(cur_res_rep_path):
                os.mkdir(cur_res_rep_path)
            
            cmat_path = os.path.join(os.path.join(cur_data_path, rep), 'character_matrix.csv')
            priors_path = os.path.join(os.path.join(cur_data_path, rep), 'estimated_mutation_prior-with-c.csv')
            
            # score_path = os.path.join(cur_res_rep_path, 'RF.csv')
            # score_path = os.path.join(cur_res_rep_path, 'contract_RF-c1-1.csv')
            # score_path = os.path.join(cur_res_rep_path, 'consensus_RF.csv')
            score_path = os.path.join(cur_res_rep_path, 'contract_consensus_RF-c1-1.csv')
            true_tree_path = os.path.join(os.path.join(cur_data_path, rep), 'true_tree.nwk')
            star_cdp_tree_path = os.path.join(cur_res_rep_path, 'star_cdp_one_sol.tre')
            consensus_tree_path = os.path.join(cur_res_rep_path, 'consensus_star_cdp_strict_consensus.tre')
            data_prefix = folder + "/"+rep
            print(data_prefix)

            if not os.path.exists(score_path) or True:
                # score_res = sp.run(['python3', comp_exe
            # , '-t1', true_tree_path, '-t2', star_cdp_tree_path, '-c1','0', '-c2', '0', '-m', cmat_path ,'-r', '0'], capture_output=True, text=True)
            
                # score_res = sp.run(['python3', comp_exe
            # , '-t1', true_tree_path, '-t2', star_cdp_tree_path, '-c1','1', '-c2', '1', '-m', cmat_path ,'-r', '0'], capture_output=True, text=True)

                # score_res = sp.run(['python3', comp_exe
            # , '-t1', true_tree_path, '-t2', consensus_tree_path, '-c1','2', '-c2', '0', '-m', cmat_path ,'-r', '0'], capture_output=True, text=True)
                score_res = sp.run(['python3', comp_exe
            , '-t1', true_tree_path, '-t2', consensus_tree_path, '-c1','1', '-c2', '1', '-m', cmat_path ,'-r', '0'], capture_output=True, text=True)

                if score_res.returncode == 0:
                    score_res = score_res.stdout
                    print(score_res)
                    [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [float(x) for x in score_res.split(',')]
                    print(f'{fn}, {fp},{tp}')


                else:
                    print("%%")
                    print(score_res.stderr)
                    raise Exception("Failed to compute score for " + cur_res_rep_path)

            
                with open(score_path, 'w', newline="") as score_file:
                    score_file.write(f'{nl},{i1},{i2},{fn},{fp},{tp}, {fnrate},{fprate},{tprate}\n')
                    print(f'write {score_path}')
            #else:
                #os.remove(score_path)

if __name__ == '__main__':

    main()