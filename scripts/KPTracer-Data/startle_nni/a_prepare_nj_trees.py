import os
import subprocess as sp

def write_nj_sbatch(curr_dir: str, nj_exe: str, cmat: str, sbatch_file: str):
    # sbatch_file_name = 'run_nj.sbatch'

    # sbatch_file = os.path.join(curr_dir, sbatch_file_name)

    # nj_tree_file = os.path.join(curr_dir, "nj.newick")
    nj_tree_file = os.path.join(curr_dir, "unpruned_nj.newick")
    time="/usr/bin/time"

    rows_to_wrtie = ['#!/bin/bash', 
                     '#SBATCH --time=48:00:00', 
                     '#SBATCH --cpus-per-task=1', 
                     '#SBATCH --ntasks=1',
                    '#SBATCH --mem=48G',
                    '#SBATCH --qos=highmem',
                    '#SBATCH --partition=cbcb',
                    '#SBATCH --account=cbcb',
                    '#SBATCH --constraint=EPYC-7313',
                    '#SBATCH --exclusive',
                    'module load Python3/3.8.15',
                    
                    time+ ' -v -o unpruned_nj_usage.log' + ' python3 ' + nj_exe + ' ' + cmat + ' ' + '--output' + ' '+ nj_tree_file +\
                    " &> " + " unpruned_nj.log " + " 2>&1 "
                    ]
    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))

def submit_nj_sbatch(data_prefix: str, nj_sbatch: str, res_dir: str):
    job_name = "--job-name=" + "a.unpruned_nj." + data_prefix
    output =  "--output="+ "a.unpruned_nj." + data_prefix + ".%j.out"
    err = "--error=" + "a.unpruned_nj." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir, 'unpruned_nj.newick')):
        sp.run(['sbatch', job_name, output, err, nj_sbatch])

def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/startle_nni'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nj_dir = os.path.join(startle_dir, 'scripts')

    startle_nj_exe = os.path.join(startle_nj_dir, 'nj.py')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
            
        # cmat_path = os.path.join(cur_data_path, folder + '_pruned_character_matrix.csv')
        cmat_path = os.path.join(cur_data_path, folder + '_character_matrix.csv')
        # nj_tree_path = os.path.join(cur_res_path, 'nj.newick')
        nj_tree_path = os.path.join(cur_res_path, 'unpruned_nj.newick')
        # nj_sbatch = os.path.join(cur_res_path, 'run_nj.sbatch')
        nj_sbatch = os.path.join(cur_res_path, 'run_unpruned_nj.sbatch')
        data_prefix = folder 
        print(data_prefix)
        # if not os.path.exists(os.path.join(cur_res_path, "nj.newick")) or True:
        if not os.path.exists(os.path.join(cur_res_path, "unpruned_nj.newick")):
            write_nj_sbatch(cur_res_path, startle_nj_exe, cmat_path, nj_sbatch)
            print('Writing sbatch file for ' + cur_res_path)
            submit_nj_sbatch(data_prefix, nj_sbatch,cur_res_path)
            print('Submiting nj job for ' + cur_res_path)
            

if __name__ == '__main__':

    main()