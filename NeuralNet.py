import random
import numpy as np


class NeuralNet:

    def __init__(self, size):
        self.size = size
        self.nb_input = size[0]
        self.nb_output = size[-1]
        self.nb_layers = len(size)
        # make neurons
        self.neurons = []
        for i in range(self.nb_layers):
            self.neurons.append(np.zeros(self.size[i]))
        
        # make weights
        self.weights = []
        self.nb_weights = self.nb_layers-1
        self.total_weights = 0
        for i in range(self.nb_weights):
            # random weights between -1 and 1
            self.weights.append(2 * np.random.rand(self.size[i], self.size[i+1]) -1)
            self.total_weights += self.size[i] * self.size[i+1]
        # make bias
        self.bias = []
        self.nb_bias = self.nb_weights
        self.total_bias = sum(self.size[1:])

    def compute(self, inputs , f = lambda x : x):
        # make sure input is in correct size
        assert len(inputs) == self.nb_input, "error dimension input"   
        self.neurons[0] = inputs[:]
        for i in range(1, len(self.neurons)):
            self.neurons[i] = self.bias[i-1]+f(np.transpose(self.weights[i-1]).dot(self.neurons[i-1]))
        # return output
        return self.neurons[-1]

    def new_weights(self, individu):
        assert len(individu) == self.total_bias + self.total_weights

        #print("individu = ", individu)
        
        cpt = 0
        # update weights 

        for M in self.weights:
            for i in range(len(M)):
                for j in range(len(M[i])):

                    M[i][j] = individu[cpt]
                    cpt += 1
        # update bias
        self.bias = []
        i = 0
        for b in range(1, len(self.size)):
            bias_size = self.size[b]
            self.bias.append([])
            for _ in range(bias_size):
                self.bias[i].append(individu[cpt])
                cpt += 1
            i += 1

    def make_individu(self, mini = -1, maxi = 1, rdfunction = lambda : 2*np.random.random() -1):
        res = []
        for _ in range(self.total_bias + self.total_weights):
            res.append(np.random.random()*(maxi-mini) + mini)
        return res

    def random_init(self, random_function = lambda : 2*np.random.random() -1):
        self.new_weights(self.make_individu(-1, 1, random_function))

