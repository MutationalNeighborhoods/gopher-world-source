import numpy as np

def fmt_trap(trap):
    return np.array2string(trap,separator='-')[1:-1]
def parse_trap(trap):
    return np.array(list(map(lambda x:int(x),trap.split('-'))))
