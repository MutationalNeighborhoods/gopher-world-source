import sys
import os
from utils import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KernelDensity
from scipy.stats import gaussian_kde
import seaborn as sns
import math


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
all_files = os.listdir()
dict_data = []
total_len = len(all_files)
for idx, filee in enumerate(all_files):
    if int(idx/total_len*100)%10 <1:
        print(f'progress: {idx/total_len}')
    if 'outputs' in filee and 'csv' in filee:
        read_file_as_dict(filee,dict_data)
    if(idx/total_len > 0.1):
        break

dictionary = {}

def convertToDictionary():
    for i in range(len(dict_data)):
        trap = dict_data[i]
        dictionary[tuple(trap['trap'])] = i

convertToDictionary()
print(dictionary[tuple(dict_data[0]['trap'])])

def visualizeData():
    dict_let = len(dict_data)
    numItems = 40
    sectionWidth = 1.0/numItems
    print(sectionWidth)
    normalCoh = []
    normalLet = []
    for i in range(numItems):
        normalCoh += [[]]
        normalLet += [[]]
    for trap in dict_data:
        coh = trap['coh']
        let = trap['let']
        
        if(trap['parent'] is not None and tuple(trap['parent']) in dictionary):
            index = dictionary[tuple(trap['parent'])]
            orgCoh = dict_data[index]['coh']
            orgLet = dict_data[index]['let']
            #preventing division by 0
            """if(orgLet == 0 or orgCoh == 0):
                continue"""
            
            letIndex = math.floor(orgLet/sectionWidth)
            cohIndex = math.floor(orgCoh/sectionWidth)
            
            if(orgCoh == 0): orgCoh = 0.00001
            if(orgLet == 0): orgLet = 0.00001
            normalCoh[cohIndex] += [(coh-orgCoh)/orgCoh]
            normalLet[letIndex] += [(let-orgLet)/orgLet]
    
    #plotting the data in historgrams
    arr = normalLet


    for i in range(numItems):
        if(len(arr[i]) == 0):
            continue
        print("index",i)
        data = arr[i]
        density = gaussian_kde(data)
        x = np.linspace(-5,5,200)
        density.covariance_factor = lambda : 0.5
        density._compute_covariance()
        y = density(x)
        print(max(y))
        label = round(i*sectionWidth,2)
        print(label)
        plt.plot(x,y, label = str(label))



    plt.show()
    plt.legend()
    plt.savefig('./plot4.png')

 






visualizeData()
