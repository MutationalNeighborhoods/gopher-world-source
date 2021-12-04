from scipy.stats import gaussian_kde
import math
import matplotlib.pyplot as plt
import pickle
import sys 

pickle_file_name = sys.argv[1:]
with open(pickle_file_name,'rb') as f:
    dict_data = pickle.load(f)
    dictionary = pickle.load(f)

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