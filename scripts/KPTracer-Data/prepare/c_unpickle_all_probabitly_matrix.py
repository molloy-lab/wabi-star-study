import os
import pandas
import treeswift
import sys
import cassiopeia
import pickle
import argparse
import csv

def pickle2csv(input_file, output_file):
    with open(input_file, 'rb') as fp:
        dic = pickle.load(fp)

    with open(output_file, 'w') as fp:
        fp.write("character,state,probability\n")

        for char, inner_dict in  dic.items():

            states_set = list(inner_dict.keys())
            states_set = sorted(states_set)

            for state in states_set:
                prob = inner_dict[state]
                fp.write("c%s,%s,%f\n" % (char, state, prob))


def main():
    trees_dir = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'data')
    trees_dir = os.path.join(trees_dir, 'KPTracer-Trees')

    folders = [f for f in os.listdir(trees_dir) if os.path.isdir(os.path.join(trees_dir, f))]

    for folder in folders: 
        if folder in ['3513_NT_Mets', '3513_NT_All'] :
            continue
        target_dir = os.path.join(trees_dir, folder)
        probability_name = folder + '_priors.pkl'
        prob_file = os.path.join(target_dir, probability_name)
        output_file = os.path.join(target_dir, folder + '_priors.csv')
        pickle2csv(prob_file, output_file)
    print("Finished unpickle all probablity matrix pickle files")

if __name__ == '__main__':
    main()