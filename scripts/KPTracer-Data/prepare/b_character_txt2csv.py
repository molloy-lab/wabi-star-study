import csv
import argparse
import os

def txt2csv(input, output_file):
    #output_file = input[0:-3] + 'csv'
    with open(input, 'r') as txt_file, open(output_file, 'w', newline="") as csv_file :
        lines = txt_file.readlines()
        
        num_columns = len(lines[0].strip().split('\t')) - 1


        writer = csv.writer(csv_file)
        
        writer.writerow([''] + [f'c{i}' for i in range(num_columns)])
        
        #outgroup_states = ["0"] * num_columns
        
        ## write out group to character csv file

        #writer.writerow(["0"] + outgroup_states)
        
        #writer.writerow(["1"] + outgroup_states)

        for line in lines[1:]:
            content = line.strip().split('\t')
            cell = content[0]
            states = content[1:]
            states = ['-1' if v == '-' else v for v in states]
            row2write = [cell] + states

            writer.writerow(row2write)

            #print(f"Writing row: {row2write}")
            
def main():
    trees_dir = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'data')
    trees_dir = os.path.join(trees_dir, 'KPTracer-Trees')
    folders = [f for f in os.listdir(trees_dir) if os.path.isdir(os.path.join(trees_dir, f))]
    
    for folder in folders:
        
        if folder in ['3513_NT_Mets', '3513_NT_All']:
            continue

        target_dir = os.path.join(trees_dir, folder)
        cmat_name = folder + '_character_matrix.txt'
        cmat_file = os.path.join(target_dir, cmat_name)
        converted_cma_file = os.path.join(target_dir, folder + '_character_matrix.csv')
        txt2csv(cmat_file, converted_cma_file)

    print("Finished convert character matrix file to the format accepted by startle.")

if __name__ == '__main__':
    main();
