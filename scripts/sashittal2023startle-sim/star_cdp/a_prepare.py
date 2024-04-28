import os
import subprocess as sp
import shutil

def main():
    
    data_path = '/fs/cbcb-lab/ekmolloy/jdai123/starhom-study/data/sashittal2023startle-sim'
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result/star_cdp'
    paup_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result/paup'

    folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
    folders = [f for f in folders if f.split("_")[1]=='50-ncas']
    
    for folder in folders:
        cur_paup_path = os.path.join(paup_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
        reps = [rep for rep in os.listdir(cur_paup_path) if os.path.isdir(os.path.join(cur_paup_path, rep))]

        for rep in reps:
            cur_res_rep_path = os.path.join(cur_res_path, rep)
            if not os.path.exists(cur_res_rep_path):
                os.mkdir(cur_res_rep_path)
            
            paup_usage_path = os.path.join(os.path.join(cur_paup_path, rep), 'paup_usage.log')
            paup_search_space_path = os.path.join(os.path.join(cur_paup_path, rep), 'paup_trees.trees')
            
            data_prefix = folder + "/"+rep
            print(data_prefix)
            
            shutil.copy(paup_search_space_path, os.path.join(cur_res_rep_path, 'search_space.trees'))
            shutil.copy(paup_usage_path, os.path.join(cur_res_rep_path, 'paup_usage.log'))

                
            

if __name__ == '__main__':

    main()