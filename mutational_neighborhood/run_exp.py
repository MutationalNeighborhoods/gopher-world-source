# python3 run_exp.py 10 single <low is fast, high is slow>
import os
from datetime import datetime
import pandas as pd
import sys 
import math
num_split, exp_name, nice = sys.argv[1:]

timestamp = datetime.today().strftime("%d-%m-%y-%H-%M-%S")
num_split = int(num_split)

f = open('inputs.csv','r').readlines()
n_row = len(f)
rows_per_split = max(n_row // num_split,1)
func_name = ''
func_name_to_runnable = {'single':'explore_single_mutation','double':'explore_double_mutation'}
try:
    func = func_name_to_runnable[exp_name]
except ValueError:
    print('incorrect exp name')

os.system(f'cp parents.csv parents-{timestamp}.csv')
os.system(f'cp inputs.csv inputs-{timestamp}.csv')

# TO DO: validate parents

for idx in range(int(math.ceil(n_row/rows_per_split))):
    start_row = idx * rows_per_split
    end_row = min((idx+1) * rows_per_split, n_row)
    sub_df = f[start_row:end_row]
    uid = f'{timestamp}--{idx}-{exp_name}.csv'
    sub_df_name = f'inputs-{uid}'
    with open(sub_df_name,'w') as write_f:
        for line in sub_df:
            write_f.write(line.strip()+'\n')
    output_file_name = f'outputs-{uid}'
    commands = f'python3 {func}.py {sub_df_name} {output_file_name}'
    screen_name = uid
    screen_commands = f'screen -dmS {screen_name} nice -n {nice} {commands}' # here is the screen command
    print(screen_commands)
    os.system(screen_commands)
os.system(f'rm inputs.csv')
print('complete')

