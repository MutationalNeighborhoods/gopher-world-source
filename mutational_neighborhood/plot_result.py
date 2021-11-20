import numpy as np

def plot_results():
    data = get_result_as_dict()
    coh, let = get_delta_coherence_lethality(data)
    print(coh)

def get_delta_coherence_lethality(data):
    delta_coherence = []
    delta_lethality = []
    for trap in data:
        if(type(trap['parent']) != type(np.array([]))):
            # we know that this is a mutated trap
            trapCoherence = trap['coh']
            trapLethality = trap['let']
            ogCoherence = trap['parent']['coh']
            ogLethality = trap['parent']['let']

            delta_coherence += trapCoherence/ogCoherence
            delta_lethality += trapLethality/ogLethality
    
    return delta_coherence, delta_lethality


