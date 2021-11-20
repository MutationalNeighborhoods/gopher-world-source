# given a df, compute scores for every single mutatio
# write to both parents.csv and results.csv
import pandas as pd
from classes.Encoding import Encoding
from compute_scores import *
from utils import *
import sys
import geneticAlgorithm.constants as constants
import numpy as np
import os
encoder = Encoding()
#python3 expl....py inputs.csv outputs.csv
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
                for location2 in range(0, len(trap), 1):
                    org_val2 = trap[location2]
                    if location == location2: continue 
                    for j in range(2, len(constants.CELL_ALPHABET)):
                        for j2 in range(2, len(constants.CELL_ALPHABET)):
                            if org_val == j and org_val2 == j2: continue 
                            trap[location] = constants.CELL_ALPHABET[j]
                            trap[location2] = constants.CELL_ALPHABET[j2]
                            coh, let = getCoherenceAndLethality(encoder, trap)
                            write_f.write(','.join([fmt_trap(trap),str(coh),str(let),org_trap_str])+'\n')
                    trap[location2] = org_val2
                trap[location] = org_val
os.system(f'rm {input_df_name}')
