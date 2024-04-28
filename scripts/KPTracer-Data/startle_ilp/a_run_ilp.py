import os
import subprocess as sp


def write_ilp_sbatch(curr_dir: str, ilp_exe: str, cmat: str, priors: str,sbatch_file: str):
    # sbatch_file_name = 'run_nj.sbatch'

    # sbatch_file = os.path.join(curr_dir, sbatch_file_name)

    # ilp_tree_file_name = 'ilp_tree.newick'
    usage_log_file = os.path.join(curr_dir, 'ilp_usage.log')
    log_file = os.path.join(curr_dir, 'ilp.log')
    # ilp_tree_file = os.path.join(curr_dir, ilp_tree_file_name)
    output_dir = os.path.join(curr_dir, 'output')
    ilp_dir = '/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software/startle'
    time="/usr/bin/time"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    perl = '/nfshomes/jdai123/perl5/perlbrew/perls/perl-5.36.0/bin/perl'
    rows_to_wrtie = ['#!/bin/bash', 
                     '#SBATCH --time=24:00:00', 
                     '#SBATCH --cpus-per-task=1', 
                     '#SBATCH --ntasks=1',
                    '#SBATCH --mem=48G',
                    '#SBATCH --qos=highmem',
                    '#SBATCH --partition=cbcb',
                    '#SBATCH --account=cbcb',
                    '#SBATCH --constraint=EPYC-7313',
                    '#SBATCH --exclusive',
                    'module load Python3/3.8.15',
                    'cd ' + ilp_dir,
                    # 'alias python=\'python3\'',
                    time + ' -v -o ' + usage_log_file + ' '+ perl + ' '+ ilp_exe + ' ' +\
                     '-o ' + output_dir + ' ' + '-m' + ' ' + priors + ' -c ' + cmat + ' --time-limit ' + '86400 '\
                      + ' &> ' +  log_file + ' 2>&1 '
                    ]
    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))



def submit_ilp_sbatch(ilp_sbatch: str, data_prefix: str, res_dir: str):
    job_name = "--job-name=" + "a.ilp." + data_prefix
    output =  "--output="+ "a.ilp." + data_prefix + ".%j.out"
    err = "--error=" + "a.ilp." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    startle_tree_path = os.path.join(os.path.join(res_dir, 'output'), 'startle_tree.newick') ## yep you cannot change ilp tree name...
    if not os.path.exists(startle_tree_path):
        sp.run(['sbatch', job_name, output, err, ilp_sbatch])



def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/startle_ilp'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_ilp_dir = os.path.join(startle_dir, 'scripts')
    startle_ilp_path = os.path.join(startle_ilp_dir, 'startle_ilp.pl')


    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
    

            
        cmat_path = os.path.join(cur_data_path, folder + '_pruned_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')    
            
        ilp_sbatch = os.path.join(cur_res_path, 'run_ilp.sbatch')
        data_prefix = folder + "/"
        print(data_prefix)
        startle_tree_path = os.path.join(os.path.join(cur_res_path, 'output'), 'startle_tree.newick') ## yep you cannot change ilp tree name...

        if not os.path.exists(startle_tree_path):
            write_ilp_sbatch(cur_res_path, startle_ilp_path, cmat_path, priors_path, ilp_sbatch)
            print('Writing sbatch file for ' + cur_res_path)
            submit_ilp_sbatch(ilp_sbatch, data_prefix, cur_res_path)
            print('Submiting ilp job for ' + cur_res_path)
            
                
            

if __name__ == '__main__':

    main()