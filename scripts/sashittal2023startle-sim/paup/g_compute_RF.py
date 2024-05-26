import os
import subprocess as sp
import re
import sys

def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle-sim"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/scripts/sashittal2023startle-sim"

    comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    folders = [f for f in folders if f.split("-")[0]=='nlin_50' and f.split("-")[1]!='ncas_20']

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
        reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]
        
        avg_fn,avg_fp = 0,0
        num_reps = len(reps)

        for rep in reps:
            cur_res_rep_path = os.path.join(cur_res_path, rep)
            if not os.path.exists(cur_res_rep_path):
                os.mkdir(cur_res_rep_path)
            
            cmat_path = os.path.join(os.path.join(cur_data_path, rep), 'character_matrix.csv')
            priors_path = os.path.join(os.path.join(cur_data_path, rep), 'estimated_mutation_prior-with-c.csv')
            # score_path = os.path.join(cur_res_rep_path, 'RF.csv')
            # score_path = os.path.join(cur_res_rep_path, 'contract_RF-c1-1.csv')
            score_path = os.path.join(cur_res_rep_path, 'contract_strict_consensus_RF-c1-1.csv')
            true_tree_path = os.path.join(os.path.join(cur_data_path, rep), 'true_tree.nwk')
            all_paup_trees_path = os.path.join(cur_res_rep_path, 'paup_trees.trees')
            strict_consensus_tree_path = os.path.join(cur_res_rep_path, 'strict_consensus.tre')

            

            data_prefix = folder + "/"+rep
            print(data_prefix)

            if not os.path.exists(all_paup_trees_path):
                print(f'missing: {all_paup_trees_path}')
            else:
                one_nwk_file = os.path.join(cur_res_rep_path, 'one_nwk.newick')
                if not os.path.exists(one_nwk_file):
                    one_nwk = ""
                    with open(all_paup_trees_path, 'r') as aptp:
                        for line in aptp:
                            one_nwk += line.strip()

                            if one_nwk.endswith(';'):
                                break
                    with open(one_nwk_file, 'w') as onf:
                        onf.write(one_nwk)

                if not os.path.exists(score_path) or True:
                    # score_prefix = os.path.join(cur_res_rep_path, 'paup_score')
                    # score_res = sp.run(['python3', comp_exe
            # , '-t1', true_tree_path, '-t2', one_nwk_file, '-c1','0', '-c2', '0', '-m', cmat_path ,'-r', '0'], capture_output=True, text=True)
                    # score_res = sp.run(['python3', comp_exe
            # , '-t1', true_tree_path, '-t2', one_nwk_file, '-c1','1', '-c2', '1', '-m', cmat_path ,'-r', '0'], capture_output=True, text=True)
                    score_res = sp.run(['python3', comp_exe
            , '-t1', true_tree_path, '-t2', strict_consensus_tree_path, '-c1','1', '-c2', '1', '-m', cmat_path ,'-r', '0'], capture_output=True, text=True)

                    if score_res.returncode == 0:
                        score_res = score_res.stdout
                        print(score_res)
                        [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [float(x) for x in score_res.split(',')]
                        print(f'{fn}, {fp},{tp}')

                    else:
                        print("%%")
                        print(score_res.stderr)
            
                    with open(score_path, 'w', newline="") as score_file:
                        score_file.write(f'{nl},{i1},{i2},{fn},{fp},{tp}, {fnrate},{fprate},{tprate}\n')
                        print(f'write {score_path}')

                # os.remove(one_nwk_file)
                
            #else:
                #os.remove(score_path)


if __name__ == '__main__':

    main()