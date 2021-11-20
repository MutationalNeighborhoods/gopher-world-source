import sys
import os
from utils import *
all_files = os.listdir()
dict_data = []
for filee in all_files:
    if 'outputs' in filee and 'csv' in filee:
        read_file(filee,dict_data)
def get_result_as_dict():
    return dict_data

def read_file_as_dict(filee,data):
    with open(filee,'r') as f:
        for line in f:
            trap, coh, let, parent = line.strip().split(',')
            trap = parse_trap(trap)
            if parent != 'None':
                parent = parse_trap(parent)
            else:
                parent = None
            coh, let = float(coh), float(let)
            trap_data = {'trap':trap,'coh':coh,'let':let,'parent':parent}
            data.append(trap_data)
