# python3 generate_traps random 30 -> 30 random traps to inputs.csv
# python3 generate_traps fil-.3-.5 30 -> 30 .3 coh and .5 let traps into csv, or the best it can
# generate traps
# 1. random
# 2. filter 
# write to input.csv
import sys
import geneticAlgorithm.library as library
from classes.Encoding import Encoding
from compute_scores import *
import numpy as np
from utils import *
if len(sys.argv)==3:
    typ, num = sys.argv[1:]
    debug = False
else:
    typ, num, debug = sys.argv[1:]
    debug = True
    debug_f = open('debug_input.csv','w')
num = int(num)
encoder = Encoding()
with open('inputs.csv','w') as f:

    if typ == 'random':
        for _ in range(num):
            trap = library.generateTrap()
            # TO DO: check if the set generated exists already using a pickle file or a file
            f.write(fmt_trap(trap)+'\n')
    # will give up after num*1000 times. 
    elif 'fil' in typ:
        iteration = 0
        cnt = 0
        _,exp_coh,exp_let = typ.split('-')
        exp_coh, exp_let = float(exp_coh),float(exp_let)
        while cnt<num and iteration<num*1000:
            trap = library.generateTrap()
            coh, let = getCoherenceAndLethality(encoder, trap)
            if(coh > exp_coh and let > exp_let):
                f.write(fmt_trap(trap)+'\n')
                if debug:
                    debug_f.write(fmt_trap(trap)+f',{coh},{let}\n')
                cnt += 1
            iteration += 1
        print(f'tried {iteration} iterations, and got {cnt} traps')
    else:
        print('random <num>, or fil-<coh val>-<let val> <num>')
if debug:
    debug_f.close()
