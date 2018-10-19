import numpy as np
import sys

'''
    Artificial Neural Network Definition.
'''
class Network:
    def __init__(self, file_n=""):
        if file_n=="":
            '''
                Random weights.
            '''
            self.input_size = 4
            self.hidden_size = 4
            self.output_size = 1
            self.W1 = np.random.randn(self.input_size, self.hidden_size)
            self.W2 = np.random.randn(self.hidden_size, self.output_size)
            self.fitness = 0
        else:
            '''
                Load a network from file.
            '''
            f = open(file_n, 'r')

            line = f.readline().split(" ")
            self.input_size = int(line[0])
            self.hidden_size = int(line[1])
            self.output_size = int(line[2])
            self.fitness = float(line[3])
            
            temp = [ [] for i in range(self.input_size) ]

            for i in range(self.input_size):
                l = f.readline().split(" ")
                for ind, j in enumerate(l[:-1]):
                    temp[i].append(float(j))
            self.W1 = np.asarray(temp)
            garbage = f.readline()

            temp = [ [] for i in range(self.hidden_size) ]

            for i in range(self.hidden_size):
                l = f.readline().split(" ")
                for ind, j in enumerate(l[:-1]):
                    temp[i].append(float(j))
            self.W2 = np.asarray(temp)

    '''
        ANN output.
    '''
    def forward(self, inputs):
        self.z2 = np.dot(inputs, self.W1)
        self.a2 = np.tanh(self.z2)
        self.z3 = np.dot(self.a2, self.W2)
        yHat = np.tanh(self.z3)
        return yHat

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))