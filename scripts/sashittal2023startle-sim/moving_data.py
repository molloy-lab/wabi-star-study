import sys
import os
import shutil

data_path = '/fs/cbcb-lab/ekmolloy/jdai123/starhom-study/data/sashittal2023startle-sim'
res_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle-sim'

folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]


folders = [f for f in folders if f.split("_")[1]=='50-ncas']

for f in folders:
    cur_data_folders = os.path.join(data_path, f)
    cur_res_folder = os.path.join(res_path, f)
    
    # print(cur_res_folder)
    
    if not os.path.exists(cur_res_folder):
        os.mkdir(cur_res_folder)
    reps = [f for f in os.listdir(cur_data_folders) if os.path.isdir(os.path.join(cur_data_folders, f))]
    for rep in reps:
        if not os.path.exists(os.path.join(cur_res_folder, rep)):
            os.mkdir(os.path.join(cur_res_folder, rep))
        source_path = os.path.join(os.path.join(data_path, f), rep)
        cmat_path = os.path.join(source_path, 'character_matrix.csv')
       
        res_cmat_path = os.path.join(os.path.join(cur_res_folder, rep), 'character_matrix.csv')
            
        if not os.path.exists(res_cmat_path):
            shutil.copy(cmat_path, res_cmat_path)
            print(f"copy {cmat_path}")
        
        est_priors_path = os.path.join(source_path, 'estimated_mutation_prior.csv')
        res_priors_path = os.path.join(os.path.join(cur_res_folder, rep), 'estimated_mutation_prior.csv')
            
        if not os.path.exists(res_priors_path):
            shutil.copy(est_priors_path, res_priors_path)
            print(f"copy {est_priors_path}")
        
        est_priors_with_c_path = os.path.join(source_path, 'estimated_mutation_prior-with-c.csv')
        res_priors_with_c_path = os.path.join(os.path.join(cur_res_folder, rep), 'estimated_mutation_prior-with-c.csv')

        if not os.path.exists(res_priors_with_c_path):
            shutil.copy(est_priors_with_c_path, res_priors_with_c_path)
            print(f"copy {est_priors_with_c_path}")
            