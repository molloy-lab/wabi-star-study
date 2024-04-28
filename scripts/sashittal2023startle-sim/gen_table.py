import os
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
pd.set_option('future.no_silent_downcasting', True)
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result'
data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle-sim"
# folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]


reps = [f"{i:02}" for i in range(1, 21)]

os.mkdir(os.path.join(result_dir, 'tables'))


methods = ['startle_nni', 'startle_ilp', 'paup', 'star_cdp']
data_parameters = ['nlin', 'ncas', 'clen', 'dout']
keys = data_parameters + methods
nlins = ['50']
ncass = ['10','20','30']
clens = ['1', '3', '10']
mutps = ['0.1']
douts = ['0.0', '0.05', '0.15', '0.2']

table_dict = {key:[] for key in keys}
time_table = {key:[] for key in keys}
folders = []

for nlin in nlins:
    for ncas in ncass:
        for clen in clens:
            for mutp in mutps:
                # table_dict['mutp'].append(mutp)
                for dout in douts:
                    table_dict['nlin'].append(nlin)
                    time_table['nlin'].append(nlin)
                    table_dict['ncas'].append(ncas)
                    time_table['ncas'].append(ncas)
                    table_dict['clen'].append(clen)
                    time_table['clen'].append(clen)
                    table_dict['dout'].append(dout)
                    time_table['dout'].append(dout)
                    folders.append(f'nlin_{nlin}-ncas_{ncas}-clen_{clen}-mutp_{mutp}-dout_{dout}')
                    

for folder in folders:
    
    for method in methods:
        cur_method_path = os.path.join(result_dir, method)
        score = pd.NA
        time = pd.NA
        score_path = (os.path.join(os.path.join(cur_method_path,folder), 'avg_score.csv'))
        time_path = (os.path.join(os.path.join(cur_method_path,folder), 'avg_time.csv'))
        if os.path.exists(score_path):
            with open(os.path.join(os.path.join(cur_method_path,folder), 'avg_score.csv'), 'r') as sf:
                score = Decimal(sf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            
        table_dict[method].append(score)

        if os.path.exists(time_path):
             with open(os.path.join(os.path.join(cur_method_path,folder), 'avg_time.csv'), 'r') as sf:
                time = Decimal(sf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

        time_table[method].append(time)


table_file = os.path.join(result_dir, 'scores_table.csv')
table_df = pd.DataFrame(table_dict)
columns_to_check = ['startle_ilp', 'paup', 'star_cdp', 'startle_nni']
table_df = table_df.dropna(subset=columns_to_check, how='all')

table_df.to_csv(table_file, index=False)

time_table_file = os.path.join(result_dir, 'time_table.csv')
time_table_df = pd.DataFrame(time_table)
time_table_df = time_table_df.dropna(subset=columns_to_check, how='all')
time_table_df.to_csv(time_table_file, index=False)


def compare_star_cdp_with(method: str, metric_to_comp:str):
    comp_keys = data_parameters + [method, 'star_cdp', f"star_cdp_vs_{method}(b/w/s)"]
    comp_tab =  {key:[] for key in comp_keys}
    comp_tab_path = os.path.join(result_dir, f'{metric_to_comp}_star_cdp_vs_{method}.csv')

    for nlin in nlins:
        for ncas in ncass:
            for clen in clens:
                for mutp in mutps:
                    # table_dict['mutp'].append(mutp)
                    for dout in douts:
                        comp_tab['nlin'].append(nlin)              
                        comp_tab['ncas'].append(ncas)
                        comp_tab['clen'].append(clen)
                        comp_tab['dout'].append(dout)

    for folder in folders:
        print(folder)
        num_of_b,num_of_w,num_of_s = 0,0,0
        for rep in reps:
            memo = {'star_cdp':pd.NA, method:pd.NA}
            for met in [method]+['star_cdp']:

                if rep == '01':
                    cur_method_path = os.path.join(os.path.join(result_dir, met), folder)
                    avg_metirc_path = os.path.join(cur_method_path, f'avg_{metric_to_comp}.csv')
                    avg_metric = pd.NA
                    if os.path.exists(avg_metirc_path):
                        with open(avg_metirc_path, 'r') as amp:
                            avg_metric = Decimal(amp.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                    comp_tab[met].append(avg_metric)
                
                metric_path = os.path.join(os.path.join(cur_method_path,rep), f'{metric_to_comp}.csv')
                if os.path.exists(metric_path):
                    with open(metric_path, 'r') as mp:
                        memo[met] = Decimal(mp.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            
            if not pd.isna(memo[method]) and not pd.isna(memo['star_cdp']):
                print(memo[method])
                print(memo['star_cdp'])
                
                num_of_b += 1 if memo[method] > memo['star_cdp'] else 0
                num_of_w += 1 if memo[method] < memo['star_cdp'] else 0
                num_of_s += 1 if memo[method] == memo['star_cdp'] else 0
                print(f'{num_of_b}/{num_of_w}/{num_of_s}')
                print('')
        
        print(f'appending: {num_of_b}/{num_of_w}/{num_of_s}')
        comp_tab[f"star_cdp_vs_{method}(b/w/s)"].append(f'{num_of_b}/{num_of_w}/{num_of_s}')
        print(comp_tab[f"star_cdp_vs_{method}(b/w/s)"])
    comp_tab = pd.DataFrame(comp_tab)
    
    comp_tab = comp_tab.dropna(subset=[method, 'star_cdp'], how='all')
    comp_tab.to_csv(comp_tab_path, index=False)


for method in methods:
    if method != 'star_cdp':
        for metric in ['score', 'time']:
            compare_star_cdp_with(method, metric)