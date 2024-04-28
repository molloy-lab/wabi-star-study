import os
import subprocess as sp
import re
import sys

def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    
    score_pattern = r"small parsimony score = ([\d.]+)"

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        

            
        cmat_path = os.path.join(cur_data_path, folder + '_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')
        score_path = os.path.join(cur_res_path, 'score.csv')

        all_paup_trees_path = os.path.join(cur_res_path, 'replaced_paup.trees')

            

        data_prefix = folder
        print(data_prefix)

        if not os.path.exists(all_paup_trees_path):
            print(f'missing: {all_paup_trees_path}')
        else:
            one_nwk = ""
            with open(all_paup_trees_path, 'r') as aptp:
                for line in aptp:
                    one_nwk += line.strip()

                    if one_nwk.endswith(';'):
                        break

            
            one_nwk_file = os.path.join(cur_res_path, 'one_nwk.newick')

            with open(one_nwk_file, 'w') as onf:
                onf.write(one_nwk)

            if not os.path.exists(score_path):
                score_prefix = os.path.join(cur_res_path, 'paup_score')
                score_res = sp.run([startle_exe, 'small', cmat_path, priors_path, one_nwk_file, '--output', score_prefix], capture_output=True, text=True)
            
                if score_res.returncode == 0:
                    score_res = score_res.stdout
                    print(score_res)
                
                    score_res_match = re.search(score_pattern, score_res)
                else:
                    print("%%")
                    print(score_res.stderr)
                    raise Exception("Failed to compute score for " + cur_res_path)

                if score_res_match:
                    score = float(score_res_match.group(1))
            
                with open(score_path, 'w', newline="") as score_file:
                    score_file.write(f'{score}\n')
                    print(f'write {score_path}')

            # os.remove(one_nwk_file)
                
            #else:
                #os.remove(score_path)
if __name__ == '__main__':

    main()