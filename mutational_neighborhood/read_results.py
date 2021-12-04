import sys
import os
from utils import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import math
import pickle
import datetime

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

pickle_file_name = sys.argv[1:]
all_files = os.listdir()
dict_data = []
total_len = len(all_files)
for idx, filee in enumerate(all_files):
    if int(idx/total_len*100)%10 <1:
        print(f'progress: {idx/total_len}')
    if 'outputs' in filee and 'csv' in filee:
        read_file_as_dict(filee,c)
    if(idx/total_len > 0.1):
        break


dictionary = {}

def convertToDictionary():
    for i in range(len(dict_data)):
        trap = dict_data[i]
        dictionary[tuple(trap['trap'])] = i

convertToDictionary()

with open(pickle_file_name,'wb') as f:
    pickle.dump(dict_data,f)
    pickle.dump(dictionary,f)