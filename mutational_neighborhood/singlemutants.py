#!/usr/bin/env python3
import geneticAlgorithm.library as library
import geneticAlgorithm.fitnessFunctions as fitnessFunctions
from classes.Encoding import Encoding
from classes.Trap import sampleRandomBoards
from classes.Trap import Trap
from classes.Board import Board 
import random
import geneticAlgorithm.constants as constants
import numpy as np
import copy
import matplotlib.pyplot as plt
from collections import Counter
import csv 
from mpl_toolkits.mplot3d import Axes3D
import math
import random


def superControlledSubstitution(location, encoding: Encoding, trap, mutation):
    """Perform a single mutation at a specific location where the replacement
        cell code is specified"""

    newTrap = copy.deepcopy(trap)
    newTrap[location] = mutation

    return newTrap

def generateAllMutantsAtCell(encoder, trap):
    """Return all possible mutations on a trap at a cellNumber"""
    listMutants = []
    for i in range(0, len(trap), 1):
        for k in range(2, len(constants.CELL_ALPHABET)):
            newTrap = superControlledSubstitution(i, encoder, trap, constants.CELL_ALPHABET[k])
            listMutants.append(newTrap)
            
    
    return listMutants


def getSingleMutationCL(encoder, trap):
    """Return all possible mutations on a trap at a cellNumber"""
    mutantCoherence, mutantLethality = [],[]
    for i in range(0, len(trap), 1):
        for k in range(2, len(constants.CELL_ALPHABET)):
            newTrap = superControlledSubstitution(i, encoder, trap, constants.CELL_ALPHABET[k])
            C, L = getCoherenceAndLethality(encoder, newTrap)
            mutantCoherence.append(C)
            mutantLethality.append(L)

            
    
    return mutantCoherence, mutantLethality


def getCoherentTraps(encoder):
    coh = random.uniform(0.05, 0.3)
    while True:
        trap = library.generateTrap()
        coherence, lethality = getCoherenceAndLethality(encoder, trap)
        if(coherence > coh and lethality > 0.3):
            print(coherence)
            return trap


def getCoherenceAndLethality(encoder, trap):
    """Returns both the coherence and lethality of a trap"""
    coherence = fitnessFunctions.getCoherence(trap,encoder)
    lethality = fitnessFunctions.getLethality(trap,encoder)
    return coherence,lethality

def generateLethalTrap(encoder):
    best_lethality = 0
    best_trap = None
    num = 1
    while num < 10 ** 2:
        trap = library.generateTrap()
        coherence, lethality = getCoherenceAndLethality(encoder, trap)
        if lethality > best_lethality:
            best_lethality = lethality
            best_trap = trap
        num += 1
    print(best_lethality)
    return best_trap



def scatterplot(ogCoherence, ogLethality, coherenceArr, lethalityArr):
    #plt.scatter(lethalityArr, coherenceArr,color='r')
    newCoherence, newLethality, size = convertCohLetArrToStat(lethalityArr, coherenceArr)
    plt.scatter(newCoherence, newLethality,color='r', s = size, label = 'mutations')
    plt.scatter(ogCoherence, ogLethality,color='b',label='original')

    plt.figure(1)
    plt.xlabel("coherence")
    plt.ylabel("lethality")
    plt.show()
    plt.savefig('./plot1.png')
    
def histogram(ogCoherence, ogLethality, coherenceArr, lethalityArr, title):

    numoriginal = int(len(lethalityArr)/100)

    plt.figure(2)
    fig = plt.figure()
    fig.suptitle("Lethality")
    arr = [[lethalityArr] ,[ogLethality]*numoriginal]
    arr = np.array(arr)
    ax = plt.gca()
    n, bins, patches = ax.hist(arr, density = True, bins=20,  histtype='bar', stacked = True)
    bar_value_to_label = ogLethality
    """print("ogLethality", ogLethality)
    min_distance = float("inf")  # initialize min_distance with infinity
    index_of_bar_to_label = 0
    for i, rectangle in enumerate(patches):  # iterate over every bar
        tmp = abs( (rectangle.get_x() +(rectangle.get_width() * (1 / 2))) - bar_value_to_label)
        if tmp < min_distance: 
            min_distance = tmp
            index_of_bar_to_label = i
    
    patches[index_of_bar_to_label].set_color('b')
    print("minDistance", min_distance)"""
    plt.show()
    plt.savefig('./plot2.png')


    plt.figure(3)
    fig = plt.figure()
    fig.suptitle("Coherence")
    arr = [[coherenceArr] ,[ogCoherence]*numoriginal]
    arr = np.array(arr)
    ax = plt.gca()
    n, bins, patches = ax.hist(arr, density = True, bins=20,  histtype='bar', stacked = True)  
    bar_value_to_label = ogCoherence
    print("ogCoherence", ogCoherence)
    """min_distance = float("inf")  # initialize min_distance with infinity
    index_of_bar_to_label = 0
    for i, rectangle in enumerate(patches):  # iterate over every bar
        tmp = abs( (rectangle.get_x() +(rectangle.get_width() * (1 / 2))) - bar_value_to_label)
        if tmp < min_distance: 
            min_distance = tmp
            index_of_bar_to_label = i
    
    patches[index_of_bar_to_label].set_color('b')
    print("minDistance", min_distance)"""

    plt.show()
    plt.savefig('./plot3.png')



def convertCohLetArrToStat(lethalityArr, coherenceArr):
    arrTuples = []
    for lethal, coherence in zip(lethalityArr, coherenceArr):
        arrTuples.append((lethal, coherence))
    distinctTuples = Counter(arrTuples)

    newCoherence = []
    newLethality = []
    size = []
    for (key0,key1),val in list(distinctTuples.items()):
        newCoherence.append(key0)
        newLethality.append(key1)
        size.append(val)
    
    return newCoherence, newLethality, size

def getDoubleMutationCL(encoder, trap):
    """Return all possible mutations on a trap at a cellNumber"""
    newTraps, mutantCoherence, mutantLethality = [], [],[]
    for i in range(0, len(trap), 1):
        for k in range(2, len(constants.CELL_ALPHABET)):
            for j in range(i+1, len(trap), 1):
                for r in range(k+1, len(constants.CELL_ALPHABET)):
                    newTrap = superControlledSubstitution(i, encoder, trap, constants.CELL_ALPHABET[k])
                    newTrap = superControlledSubstitution(j, encoder, newTrap, constants.CELL_ALPHABET[r])
                    C, L = getCoherenceAndLethality(encoder, newTrap)
                    newTraps.append(newTrap)
                    mutantCoherence.append(C)
                    mutantLethality.append(L)
    return mutantCoherence, mutantLethality
def getTripleMutationCL(encoder, trap, size):
    """Return all possible mutations on a trap at a cellNumber"""
    newTraps, mutantCoherence, mutantLethality = [], [],[]
    num = 0
    seen = set()
    while len(seen) < size:
        pos = [] 
        alphabet = []
        for _ in range(3):
            pos.append(random.choice(range(0, len(trap))))
            alphabet.append(random.choice(range(2, len(constants.CELL_ALPHABET))))
        hash = tuple(pos + alphabet)
        if hash in seen:
            continue 
        elif len(set(pos))!=3:
            continue 
        else:
            seen.add(hash)
        newTrap = copy.deepcopy(trap)
        for i, k in zip(pos,alphabet):
            newTrap = superControlledSubstitution(i, encoder, newTrap, constants.CELL_ALPHABET[k])
        
        C, L = getCoherenceAndLethality(encoder, newTrap)
        #newTraps.append(newTrap)
        mutantCoherence.append(C)
        mutantLethality.append(L)
    return mutantCoherence, mutantLethality




def plotSingleMutants(encoder, trap):
    print(trap)
    C,L = getSingleMutationCL(encoder, trap)
    trapC, trapL = getCoherenceAndLethality(encoder, trap)
    print(trapC, trapL)
    scatterplot(trapC, trapL, C, L)
    histogram(trapC, trapL, C, L, "Single Mutation")

def plotDoubleMutation(encoder, trap):
    print(trap)
    C,L = getDoubleMutationCL(encoder, trap)
    trapC, trapL = getCoherenceAndLethality(encoder, trap)
    print(trapC, trapL)
    scatterplot(trapC, trapL, C, L)
    histogram(trapC, trapL, C, L, "Double Mutation")

def plotTripleMutation(encoder, trap):
    print(trap)
    C,L = getTripleMutationCL(encoder, trap, 1000)
    trapC, trapL = getCoherenceAndLethality(encoder, trap)
    print(trapC, trapL)
    C = returnsDeltaChangeList(C, trapC)
    L = returnsDeltaChangeList(L, trapL)
    scatterplot(trapC, trapL, C, L)
    histogram(trapC, trapL, C, L, "Triple Mutation")


def plotMultiplePlots(num):
    encoder = Encoding() 
    CList = []
    LList = []
    originalC = []
    originalL = []
    for i in range(num):
        print(i)
        trap = getCoherentTraps(encoder)
        C,L = getTripleMutationCL(encoder, trap, 10000)
        trapC, trapL = getCoherenceAndLethality(encoder, trap)
        CList += C
        LList += L
        originalC += [trapC]
        originalL += [trapL]
    
    multHistogram(originalC, originalL, CList, LList, "hi")


def multHistogram(ogCoherence, ogLethality, coherenceArr, lethalityArr,  title):

    numoriginal = int(len(lethalityArr)/100)
    plt.figure(4)
    fig = plt.figure()
    fig.suptitle("Lethality")
    
    sizedUpLethality = []
    for i in range(len(ogLethality)):
        sizedUpLethality += [ogLethality[i]] * numoriginal
    arr = [lethalityArr, sizedUpLethality]
    arr = np.array(arr)
    ax = plt.gca()
    ax.hist(arr, density = True, bins=100,  histtype='bar')
    plt.show()
    plt.savefig('./plot4.png')

    numoriginal = int(len(coherenceArr)/100)
    plt.figure(5)
    fig = plt.figure()
    fig.suptitle("Coherence")
    
    sizedUpCoherence = []
    for i in range(len(ogCoherence)):
        sizedUpCoherence += [ogCoherence[i]] * numoriginal
    arr = [coherenceArr, sizedUpCoherence]
    arr = np.array(arr)
    ax = plt.gca()
    n, bins, patches = ax.hist(arr, density = True, bins=50,  histtype='bar', stacked = True)
    bar_value_to_label = ogCoherence
    plt.show()
    plt.savefig('./plot5.png')

def returnsDeltaChangeList(list, originalPoint):
    newList = []
    for item in list:
        newList += [(item-originalPoint)/originalPoint]
    
    return newList

def main():    
    encoder = Encoding() 
    trap = getCoherentTraps(encoder)
    #multimutatedtraps = getMultiMutatedDict(encoder, 3, 4)
    #X,Y,V = getPolar(multimutatedtraps,4, 0)
    #X,Y,V = getPolar(sampleDictionary, 1,1)
    #scatterplot(0, 0,X, Y)
    # trap = generateLethalTrap(encoder)
    #print(lethal_trap)

    # trap = getCoherentTraps(encoder)
    #C, L = getSingleMutationCL(encoder, trap)
    #plotSingleMutants(encoder, trap)

    plotTripleMutation(encoder, trap)
    #plotMultiplePlots(50)


  

if __name__ == "__main__":
    main()
