import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import pandas as pd


def main():
    
    
    
    table = {key:[] for key in ['nlin', 'ncas', 'clen', 'dout', 'rep','true-tree-score-under-est-prior']}
    nlins = ['50']
    ncass = ['10','20','30']
    clens = ['1', '3', '10']
    mutps = ['0.1']
    douts = ['0.0', '0.05', '0.15', '0.2']
    reps = [f"{i:02}" for i in range(1, 21)]

    folders = []
    for nlin in nlins:
        for ncas in ncass:
            for clen in clens:
                for mutp in mutps:
                    # table_dict['mutp'].append(mutp)
                    for dout in douts:
                        folders.append(f'nlin_{nlin}-ncas_{ncas}-clen_{clen}-mutp_{mutp}-dout_{dout}')
                        for rep in reps:
                            table['nlin'].append(nlin)
                            table['ncas'].append(ncas)
                            table['clen'].append(clen)
                            table['dout'].append(dout)
                            table['rep'].append(rep)
        
    
    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle-sim"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')
    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    # folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    
    score_pattern = r"small parsimony score = ([\d.]+)"

    for folder in folders:
        
        cur_data_path = os.path.join(data_dir, folder)
        

        for rep in reps:
            cur_data_rep_path = os.path.join(cur_data_path, rep)
            
            if not os.path.exists(cur_data_path):
                table['true-tree-score-under-est-prior'].append(pd.NA)
                continue

            cmat_path = os.path.join(os.path.join(cur_data_path, rep), 'character_matrix.csv')
            priors_path = os.path.join(os.path.join(cur_data_path, rep), 'estimated_mutation_prior-with-c.csv')
            score_path = os.path.join(cur_data_rep_path, 'score_under_estimated_mutation_prior.csv')
            ilp_tree_path = os.path.join(cur_data_rep_path, 'converted_true_tree.nwk')
            
            data_prefix = folder + "/"+rep
            print(data_prefix)

            if not os.path.exists(score_path) or True:
                score_prefix = os.path.join(cur_data_rep_path, 'true_tree_score')
                score_res = sp.run([startle_exe, 'small', cmat_path, priors_path, ilp_tree_path, '--output', score_prefix], capture_output=True, text=True)
            
                if score_res.returncode == 0:
                    score_res = score_res.stdout
                    print(score_res)
                
                    score_res_match = re.search(score_pattern, score_res)
                else:
                    print("%%")
                    print(score_res.stderr)
                    raise Exception("Failed to compute score for " + cur_data_rep_path)

                if score_res_match:
                    score = Decimal(score_res_match.group(1)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                    table['true-tree-score-under-est-prior'].append(score)
            
                with open(score_path, 'w', newline="") as score_file:
                    score_file.write(f'{score}\n')
                    print(f'write {score_path}')
                
            #else:
                #os.remove(score_path)
    print(table)
    table_df = pd.DataFrame(table)
    table_df = table_df.dropna(subset=['true-tree-score-under-est-prior'], how='all')
    table_df.to_csv(os.path.join(data_dir, 'true_trees_scores.csv'), index=False)

if __name__ == '__main__':

    main()