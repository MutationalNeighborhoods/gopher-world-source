# given a df, compute scores for every single mutatio
# write to both parents.csv and results.csv
import pandas as pd
from classes.Encoding import Encoding
from mutational_neighborhood.compute_scores import *
from mutational_neighborhood.utils import *
import sys
import geneticAlgorithm.constants as constants
import numpy as np
import os

def explore_single_mutation(input_df_name, output_file_name):
    encoder = Encoding()
    with open(input_df_name,'r') as read_f:
        with open(output_file_name,'w') as write_f:
            for line in read_f:
                org_trap_str = line.strip()
                trap = parse_trap(org_trap_str)
                print(trap)
                print(len(trap))
                coh, let = getCoherenceAndLethality(encoder, trap)
                write_f.write(','.join([org_trap_str,str(coh),str(let),'None'])+'\n')
                for location in range(0, len(trap), 1):
                    org_val = trap[location]
                    for j in range(2, len(constants.CELL_ALPHABET)):
                        if org_val == j: continue 
                        trap[location] = constants.CELL_ALPHABET[j]
                        coh, let = getCoherenceAndLethality(encoder, trap)
                        write_f.write(','.join([fmt_trap(trap),str(coh),str(let),org_trap_str])+'\n')
                    trap[location] = org_val
                write_f.flush()
                os.fsync(write_f.fileno())
    os.system(f'rm {input_df_name}')

"""
encoder = Encoding()

input_df_name, output_file_name = sys.argv[1:]

with open(input_df_name,'r') as read_f:
    with open(output_file_name,'w') as write_f:
        for line in read_f:
            org_trap_str = line.strip()
            trap = parse_trap(org_trap_str) 
            coh, let = getCoherenceAndLethality(encoder, trap)
            write_f.write(','.join([org_trap_str,str(coh),str(let),'None'])+'\n')
            for location in range(0, len(trap), 1):
                org_val = trap[location]
                for j in range(2, len(constants.CELL_ALPHABET)):
                    if org_val == j: continue 
                    trap[location] = constants.CELL_ALPHABET[j]
                    coh, let = getCoherenceAndLethality(encoder, trap)
                    write_f.write(','.join([fmt_trap(trap),str(coh),str(let),org_trap_str])+'\n')
                trap[location] = org_val
            write_f.flush()
            os.fsync(write_f.fileno())
os.system(f'rm {input_df_name}')
"""