
from Snakew import *
from Pong import *
from GeneticAlgo import *
import numpy as np
import random
from NeuralNet import *
from dodge import *



sigmoid = lambda x : 1/(1+np.exp(-x))
tanh = lambda x : 2 * sigmoid(2*x)-1

def randfloat(mini, maxi):
    return lambda : mini + (maxi - mini)*np.random.random()

def readScore(file):
    file.seek(0)
    a = file.readline()
    if a == '':
        a = 0
    print("score lu = ", a)
    return float(a)

def writeFile(file, score, data):
    file.seek(0)
    file.write(str(score) + "\n" + str(data))
    file.truncate()

def readIndividual(file):
    file.seek(0)
    s = file.readline()
    s = file.readline()
    if s != '':
        l = eval(s)
        return l
    return []

  

