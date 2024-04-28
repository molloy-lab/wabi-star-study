import os
import subprocess as sp
import re

import sys

def get_wall_clock_time(file_path:str):
    time_regex = re.compile(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (.*:.*(:.*)?)")

    with open(file_path, 'r') as file:
        content = file.read()
        time_match = re.search(time_regex, content)
        if time_match:
            time_str = time_match.group(1)
            time_parts = time_str.split(":")
            if len(time_parts) == 3:
                hrs, mins, secs = float(time_parts[0]), float(time_parts[1]), float(time_parts[2])
                return hrs * 3600 + mins * 60 + secs
            elif len(time_parts) == 2:
                mins, secs = float(time_parts[0]),  float(time_parts[1])
                return mins * 60 + secs
    return None

def main():
   

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result/star_cdp'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle-sim"

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
        reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]
        
        avg_time = 0
        num_reps = len(reps)
        
        for rep in reps:
            
            cur_res_rep_path = os.path.join(cur_res_path, rep)
            if not os.path.exists(cur_res_rep_path):
                os.mkdir(cur_res_rep_path)

            time_path = os.path.join(cur_res_rep_path, 'time.csv')

            data_prefix = folder + "/"+rep
            print(data_prefix)
            paup_usage = os.path.join(cur_res_rep_path, 'paup_usage.log')
            star_cdp_usage = os.path.join(cur_res_rep_path, 'star_cdp_usage.log')
            time = get_wall_clock_time(paup_usage)
            time += get_wall_clock_time(star_cdp_usage)

            avg_time += time
            with open(time_path, 'w', newline="") as tf:
                tf.write(f"{time}\n")
            #else:
                #os.remove(score_path)
        avg_time /= num_reps
        avg_time_file = os.path.join(cur_res_path, 'avg_time.csv')
        with open(avg_time_file, 'w', newline="") as avgf:
            avgf.write(f'{avg_time}\n')
            print((f'write {avg_time_file}'))
        

if __name__ == '__main__':

    main()