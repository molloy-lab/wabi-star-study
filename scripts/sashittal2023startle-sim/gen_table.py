import os
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
pd.set_option('future.no_silent_downcasting', True)
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result'
data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle-sim"
# folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]


reps = [f"{i:02}" for i in range(1, 21)]
table_dir = os.path.join(result_dir, 'tables')
if not os.path.exists(table_dir):
    os.mkdir(table_dir)


methods = ['startle_nni', 'startle_ilp', 'paup', 'star_cdp']
data_parameters = ['nlin', 'ncas', 'clen', 'dout']
keys = data_parameters + methods
nlins = ['50']
# ncass = ['10','20','30']
ncass = ['10', '30']
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
                    

# for folder in folders:
    
#     for method in methods:
#         cur_method_path = os.path.join(result_dir, method)
#         score = pd.NA
#         time = pd.NA
#         score_path = (os.path.join(os.path.join(cur_method_path,folder), 'avg_score.csv'))
#         time_path = (os.path.join(os.path.join(cur_method_path,folder), 'avg_time.csv'))
#         if os.path.exists(score_path):
#             with open(os.path.join(os.path.join(cur_method_path,folder), 'avg_score.csv'), 'r') as sf:
#                 score = Decimal(sf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            
#         table_dict[method].append(score)

#         if os.path.exists(time_path):
#              with open(os.path.join(os.path.join(cur_method_path,folder), 'avg_time.csv'), 'r') as sf:
#                 time = Decimal(sf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

#         time_table[method].append(time)


# table_file = os.path.join(result_dir, 'scores_table.csv')
# table_df = pd.DataFrame(table_dict)
# columns_to_check = ['startle_ilp', 'paup', 'star_cdp', 'startle_nni']
# table_df = table_df.dropna(subset=columns_to_check, how='all')

# table_df.to_csv(table_file, index=False)

# time_table_file = os.path.join(result_dir, 'time_table.csv')
# time_table_df = pd.DataFrame(time_table)
# time_table_df = time_table_df.dropna(subset=columns_to_check, how='all')
# time_table_df.to_csv(time_table_file, index=False)


def compare_star_cdp_with(method: str, metric_to_comp:str):
    comp_keys = data_parameters + [method, 'star_cdp', f"star_cdp_vs_{method}(b/w/s)"]
    comp_tab =  {key:[] for key in comp_keys}
    comp_tab_path = os.path.join(os.path.join(result_dir,'tables'), f'{metric_to_comp}_star_cdp_vs_{method}.csv')

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
                cur_method_path = os.path.join(os.path.join(result_dir, met), folder)
                
                if rep == '01':
                    avg_metirc_path = os.path.join(cur_method_path, f'avg_{metric_to_comp}.csv')
                    avg_metric = pd.NA
                    if os.path.exists(avg_metirc_path):
                        with open(avg_metirc_path, 'r') as amp:
                            avg_metric = Decimal(amp.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                    comp_tab[met].append(avg_metric)
                    print(f'avg_score:{avg_metric}')
                
                metric_path = os.path.join(os.path.join(cur_method_path,rep), f'{metric_to_comp}.csv')
                
                if os.path.exists(metric_path):
                    with open(metric_path, 'r') as mp:
                        memo[met] = Decimal(mp.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        
            
            if not pd.isna(memo[method]) and not pd.isna(memo['star_cdp']):
                print(memo[method])
                print(memo['star_cdp'])
                
                print(f'{method}:{memo[method]}')
                
                num_of_b = num_of_b + 1 if memo[method] > memo['star_cdp'] else num_of_b
                num_of_w =  num_of_w + 1 if memo[method] < memo['star_cdp'] else num_of_w
                num_of_s =  num_of_s + 1 if memo[method] == memo['star_cdp'] else  num_of_s

                print(f'{num_of_b}/{num_of_w}/{num_of_s}')
                print('')
                # if method == 'startle_ilp' and folder == 'nlin_50-ncas_30-clen_10-mutp_0.1-dout_0.2':
                #     exit(0)

        print(f'appending: {num_of_b}/{num_of_w}/{num_of_s}')
        comp_tab[f"star_cdp_vs_{method}(b/w/s)"].append(f'{num_of_b}/{num_of_w}/{num_of_s}')
        print(comp_tab[f"star_cdp_vs_{method}(b/w/s)"])
    comp_tab = pd.DataFrame(comp_tab)
    
    comp_tab = comp_tab.dropna(subset=[method, 'star_cdp'], how='all')
    comp_tab.to_csv(comp_tab_path, index=False)

# for method in methods:
#     if method != 'star_cdp':
#         for metric in ['score', 'time']:
#             compare_star_cdp_with(method, metric)



def check(i1,i2,fn,fp,tp):
    if fp + tp != i2:
        raise Exception(f"fp:{fp} + tp:{tp} != i2:{i2}")
    elif i1 != fn + tp:
        raise Exception(f"fp:{fn} + tp:{tp} != i1:{i1}")



def all_table():
    # table = {key: [] for key in ['nlin', 'ncas', 'clen', 'dout', 'rep','method', 'FN', 'FP', 'contract-FN', 'contract-FP', 'parsimony-score', 'time', '#branches']}
    table = {key: [] for key in ['nlin', 'ncas', 'clen', 'dout', 'rep','method','#branches_in_true_tree','#branches','#FN', '#FP', '#TP','FN_rate','FP_rate','TP_rate','parsimony-score', 'time']}
    for nlin in nlins:
        for ncas in ncass:
            for clen in clens:
                for mutp in mutps:
                    # table_dict['mutp'].append(mutp)
                    for dout in douts:
                        for rep in reps:
                            for met in ['Cassiopeia-Greedy','startle_nni','startle_ilp', 'paup','star_cdp', 'paup-Consensus(Contraction)', 'StarCDP-Consensus(Contraction)','Ground-Truth']:
                                table['nlin'].append(nlin)              
                                table['ncas'].append(ncas)
                                table['clen'].append(clen)
                                table['dout'].append(dout)
                                table['rep'].append(rep)
                                table['method'].append(met)
    print(folders)
    for folder in folders:
        for rep in reps:
            for met in ['Cassiopeia-Greedy','startle_nni','startle_ilp', 'paup','star_cdp', 'paup-Consensus(Contraction)', 'StarCDP-Consensus(Contraction)','Ground-Truth']:
                if met == 'paup-Consensus(Contraction)':
                    cur_path = os.path.join(os.path.join(os.path.join(result_dir, 'paup'), folder),rep)
                    score_file = os.path.join(cur_path, 'score.csv')
                    time_file = os.path.join(cur_path, 'time.csv')
                    
                    rf_file = os.path.join(cur_path, 'contract_strict_consensus_RF-c1-1.csv')
                    if os.path.exists(rf_file):
                        with open(rf_file, 'r') as rf:
                            content = rf.readline().strip().split(',')
                            [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [float(x) for x in content]
                            check(i1,i2,fn,fp,tp)
                            table['#FN'].append(int(fn))
                            table['#FP'].append(int(fp))
                            table['#TP'].append(int(tp))
                            table['#branches'].append(int(i2))
                            table['#branches_in_true_tree'].append(int(i1))
                            table['FN_rate'].append(fnrate)
                            table['FP_rate'].append(fprate)
                            table['TP_rate'].append(tprate)

                    else:
                        # table['FN'].append(pd.NA)
                        table['#FN'].append(pd.NA)
                        # table['FP'].append(pd.NA)
                        table['#FP'].append(pd.NA)
                        table['#branches'].append(pd.NA)
                        table['#TP'].append(pd.NA)
                        table['#branches'].append(pd.NA)
                        table['#branches_in_true_tree'].append(pd.NA)
                        table['FN_rate'].append(pd.NA)
                        table['FP_rate'].append(pd.NA)
                        table['TP_rate'].append(pd.NA)


                    if os.path.exists(score_file):
                        with open(score_file, 'r') as sf:
                            score = Decimal(sf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                            table['parsimony-score'].append(score)
                    else:
                        table['parsimony-score'].append(pd.NA)
                    
                    if os.path.exists(time_file):

                        with open(time_file, 'r') as tf:
                            time = Decimal(tf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                            table['time'].append(time)    
                    else:
                        table['time'].append(pd.NA)   
                elif met == 'StarCDP-Consensus(Contraction)':
                    cur_path = os.path.join(os.path.join(os.path.join(result_dir, 'star_cdp'), folder),rep)
                    score_file = os.path.join(cur_path, 'score.csv')
                    time_file = os.path.join(cur_path, 'time.csv')
                    
                    rf_file = os.path.join(cur_path, 'contract_consensus_RF-c1-1.csv')
                    if os.path.exists(rf_file):
                        with open(rf_file, 'r') as rf:
                            [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [float(x) for x in rf.readline().strip().split(',')]
                            check(i1,i2,fn,fp,tp)
                            table['#FN'].append(int(fn))
                            table['#FP'].append(int(fp))
                            table['#TP'].append(int(tp))
                            table['#branches'].append(int(i2))
                            table['#branches_in_true_tree'].append(int(i1))
                            table['FN_rate'].append(fnrate)
                            table['FP_rate'].append(fprate)
                            table['TP_rate'].append(tprate)
                    else:
                        # table['FN'].append(pd.NA)
                        table['#FN'].append(pd.NA)
                        # table['FP'].append(pd.NA)
                        table['#FP'].append(pd.NA)
                        table['#branches'].append(pd.NA)
                        table['#TP'].append(pd.NA)
                        table['#branches'].append(pd.NA)
                        table['#branches_in_true_tree'].append(pd.NA)
                        table['FN_rate'].append(pd.NA)
                        table['FP_rate'].append(pd.NA)
                        table['TP_rate'].append(pd.NA)

                    if os.path.exists(score_file):
                        with open(score_file, 'r') as sf:
                            score = Decimal(sf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                            table['parsimony-score'].append(score)
                    else:
                        table['parsimony-score'].append(pd.NA)
                    
                    if os.path.exists(time_file):

                        with open(time_file, 'r') as tf:
                            time = Decimal(tf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                            table['time'].append(time)    
                    else:
                        table['time'].append(pd.NA)   
                elif met == 'Ground-Truth':
                    cur_path = os.path.join(os.path.join(os.path.join(result_dir, 'star_cdp'), folder),rep)
                    score_file = os.path.join(cur_path, 'score.csv')
                    time_file = os.path.join(cur_path, 'time.csv')
                    
                    rf_file = os.path.join(cur_path, 'contract_consensus_RF-c1-1.csv')
                    if os.path.exists(rf_file):
                        with open(rf_file, 'r') as rf:
                            [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [float(x) for x in rf.readline().strip().split(',')]
                            # check(i1,i2,fn,fp,tp)
                            table['#FN'].append(0)
                            table['#FP'].append(0)
                            table['#TP'].append(i1)
                            table['#branches'].append(int(i1))
                            table['#branches_in_true_tree'].append(int(i1))
                            table['FN_rate'].append(0.0)
                            table['FP_rate'].append(0.0)
                            table['TP_rate'].append(1)
                    else:
                        # table['FN'].append(pd.NA)
                        table['#FN'].append(pd.NA)
                        # table['FP'].append(pd.NA)
                        table['#FP'].append(pd.NA)
                        table['#branches'].append(pd.NA)
                        table['#TP'].append(pd.NA)
                        table['#branches'].append(pd.NA)
                        table['#branches_in_true_tree'].append(pd.NA)
                        table['FN_rate'].append(pd.NA)
                        table['FP_rate'].append(pd.NA)
                        table['TP_rate'].append(pd.NA)

                    if os.path.exists(score_file):
                        with open(score_file, 'r') as sf:
                            score = Decimal(sf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                            table['parsimony-score'].append(score)
                    else:
                        table['parsimony-score'].append(pd.NA)
                    
                    if os.path.exists(time_file):

                        with open(time_file, 'r') as tf:
                            time = Decimal(tf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                            table['time'].append(time)    
                    else:
                        table['time'].append(pd.NA)


                else:
                    cur_path = os.path.join(os.path.join(os.path.join(result_dir, met), folder),rep)
                    rf_file = os.path.join(cur_path, 'RF.csv')
                    contract_rf_file = os.path.join(cur_path, 'contract_RF-c1-1.csv')
                    score_file = os.path.join(cur_path, 'score.csv')
                    time_file = os.path.join(cur_path, 'time.csv')

                    # if os.path.exists(rf_file):
                    #     with open(rf_file, 'r') as rf:
                    #         content = rf.readline().strip().split(',')
                    #         fn = Decimal(content[5]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                    #         fp = Decimal(content[6]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                    #         table['FN'].append(fn)
                    #         table['FP'].append(fp)
                    # else:
                    #     table['FN'].append(pd.NA)
                    #     table['FP'].append(pd.NA)
                    
                    if os.path.exists(contract_rf_file):
                        with open(contract_rf_file, 'r') as crf:
                            [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [float(x) for x in crf.readline().strip().split(',')]
                            check(i1,i2,fn,fp,tp)
                            table['#FN'].append(int(fn))
                            table['#FP'].append(int(fp))
                            table['#TP'].append(int(tp))
                            table['#branches'].append(int(i2))
                            table['#branches_in_true_tree'].append(int(i1))
                            table['FN_rate'].append(fnrate)
                            table['FP_rate'].append(fprate)
                            table['TP_rate'].append(tprate)
                    else:
                        # table['FN'].append(pd.NA)
                        table['#FN'].append(pd.NA)
                        # table['FP'].append(pd.NA)
                        table['#FP'].append(pd.NA)
                        table['#branches'].append(pd.NA)
                        table['#TP'].append(pd.NA)
                        table['#branches'].append(pd.NA)
                        table['#branches_in_true_tree'].append(pd.NA)
                        table['FN_rate'].append(pd.NA)
                        table['FP_rate'].append(pd.NA)
                        table['TP_rate'].append(pd.NA)
                    if os.path.exists(score_file):
                        with open(score_file, 'r') as sf:
                            score = Decimal(sf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                            table['parsimony-score'].append(score)
                    else:
                        table['parsimony-score'].append(pd.NA)
                    if os.path.exists(time_file):
                        with open(time_file, 'r') as tf:
                            time = Decimal(tf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                            table['time'].append(time)
                    else:
                        table['time'].append(pd.NA)
    for k,v in table.items():
        print(f'k:{k}, len(v):{len(v)}')
    df = pd.DataFrame(table)
    df = df.dropna(subset=['#branches_in_true_tree','#branches','#FN', '#FP', '#TP','FN_rate','FP_rate','TP_rate','parsimony-score', 'time'], how='all')
    df.to_csv(os.path.join(table_dir, 'sim-results-c1-1.csv'), index=False)
                    





all_table()







def num_sol_table():
    table = {key:[] for key in ['nlin', 'ncas', 'clen', 'dout', 'rep','number_of_opt_trees']}
    for nlin in nlins:
        for ncas in ncass:
            for clen in clens:
                for mutp in mutps:
                    # table_dict['mutp'].append(mutp)
                    for dout in douts:
                        for rep in reps:
                            table['nlin'].append(nlin)              
                            table['ncas'].append(ncas)
                            table['clen'].append(clen)
                            table['dout'].append(dout)
                            table['rep'].append(rep)
    
    star_cdp_res_path = os.path.join(result_dir,'star_cdp')
    for folder in folders:
        for rep in reps:
            cur_path = os.path.join(os.path.join(star_cdp_res_path, folder),rep)
            num_of_opt = pd.NA
            
            if os.path.exists(os.path.join(cur_path,'consensus_star_cdp_number_of_sol.csv')):
                with open(os.path.join(cur_path,'consensus_star_cdp_number_of_sol.csv'), 'r') as cp:
                    num_of_opt = int(cp.readline().strip())
            table['number_of_opt_trees'].append(num_of_opt)
    df = pd.DataFrame(table)
    df = df.dropna(subset=['number_of_opt_trees'], how='all')
    table_path = os.path.join(table_dir, 'number_of_sol.csv')
    df.to_csv(table_path,index=False)
    

# num_sol_table()

def rf_table(contract=False):
    methods = ['startle_ilp(FN/FP)','startle_nni(FN/FP)', 'paup(FN/FP)', 'star_cdp(FN/FP)']
    columns = ['nlin', 'ncas', 'clen', 'dout']
    csv_file_name = 'avg_RF.csv'
    if contract:
        methods.append('star-cdp-strict-consensus(FN/FP)')
        csv_file_name = 'contract_avg_RF.csv'
    
    columns += methods

    methods = [s[0:-7] for s in methods]

    folders = []
    table = {key:[] for key in columns}
    for nlin in nlins:
        for ncas in ncass:
            for clen in clens:
                for mutp in mutps:
                    # table_dict['mutp'].append(mutp)
                    for dout in douts:
                       
                        table['nlin'].append(nlin)              
                        table['ncas'].append(ncas)
                        table['clen'].append(clen)
                        table['dout'].append(dout)
                        folders.append(f'nlin_{nlin}-ncas_{ncas}-clen_{clen}-mutp_{mutp}-dout_{dout}')
    
    for method in methods:

        for folder in folders:
            avg_fn,avg_fp = pd.NA,pd.NA
            cur_res_path = os.path.join(os.path.join(os.path.join(result_dir, method),folder), csv_file_name)
            
         
            if method != 'star-cdp-strict-consensus':
                if os.path.exists(cur_res_path):
                    print(cur_res_path)
                    with open(cur_res_path, 'r') as crp:
                        content = crp.readline().strip().split(',')
                        avg_fn = Decimal(content[0]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        avg_fp = Decimal(content[1]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        table[method+'(FN/FP)'].append(f'{avg_fn}|{avg_fp}')
                    print(f'{avg_fn},{avg_fp}')
                else:
                    table[method+'(FN/FP)'].append("")
            if contract and method == 'star-cdp-strict-consensus':
                cur_consens_path = os.path.join(os.path.join(os.path.join(result_dir, 'star_cdp'),folder), "consensus_avg_RF.csv")
                if os.path.exists(cur_consens_path):
                    with open(cur_consens_path, 'r') as ccp:
                        content = ccp.readline().strip().split(',')
                        avg_fn = Decimal(content[0]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        avg_fp = Decimal(content[1]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        table[method+'(FN/FP)'].append(f'{avg_fn}|{avg_fp}')
                else:
                    table[method+'(FN/FP)'].append("")

    table_df = pd.DataFrame(table)
    subset_cols = [method + '(FN/FP)' for method in methods]
    mask = table_df[subset_cols].apply(lambda x: x.str.strip().eq('')).all(axis=1)
    # table_df.dropna(subset=[method + '(FN/FP)' for method in methods], how='any',inplace=False)
    table_df = table_df[~mask]
    table_file_name = ''
    if not contract:
        table_file_name = os.path.join(os.path.join(result_dir,'tables'), 'RF-error-table.csv')
    else:
        table_file_name = os.path.join(os.path.join(result_dir,'tables'), 'contract-RF-error-table.csv')
    
    table_df.to_csv(table_file_name, index=False)
    
# rf_table(contract=False)
# rf_table(contract=True)