import random
import numpy as np

def algogen1(npop, population,nn,  f = lambda : 2 * np.random.random() - 1, mutrate = 10):
    k = 6
    npop = len(population)
    mut = int((mutrate * npop)/100)


    for i in range(5, npop//k):
        population[i] = crossover3(population[i], population[0])
    for i in range(npop//k, 2*npop//k):
        population[i] = mutation(population[i-npop//k], mut, f)
    for i in range(2*npop//k, 3*npop//k):
        population[i] = crossover3(nn.make_individu(-1, 1), population[i - 2*npop//k])
    for i in range(3*npop//k, 4*npop//k):
        population[i] = crossover(population[i-3*npop//k], population[np.random.randint(0,npop-1)])
    for i in range(4*npop//k, 5*npop//k):
        population[i] = mutation2(population[i - 4*npop//k], -2, 2)
    for i in range(5*npop//k, npop):
        population[i] = nn.make_individu(-1, 1)
    
    return population


# mean crossover
def crossover(individu1, individu2):
    ans = []
    for i in range(len(individu1)):
        ans.append((individu1[i] + individu2[i])/2)
    return ans

# random choice crossover
def crossover2(individu1, individu2):
    ans = []
    for i in range(len(individu1)):
        ans.append(random.choice([individu1[i],individu2[i]]))
    return ans


def mutation(individu, number, f = lambda  : 2*np.random.random()-1):
    res = individu[:]
    for _ in range(number):
        i = np.random.randint(0,len(individu)-1)
        res[i] = f()

    return res
    

def mutation2(individu, mini, maxi):
    res = individu[:]
    for i in range(len(res)):
        res[i] += np.random.random()*(mini-maxi)+mini
    return res

# crossover cut
def crossover3(i1, i2):
    i = random.randint(0, len(i1)-1)
    a = random.randint(0,1)
    if a == 0:
        return i1[:i] + i2[i:]
    else:
        return i2[:i] + i1[i:]
