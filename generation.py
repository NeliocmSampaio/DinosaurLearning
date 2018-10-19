from vision import Vision
from network import Network
from time import sleep, time
import numpy as np
import pykeyboard
from pynput.keyboard import Key, Controller
import random
import copy
import datetime

import pyautogui

def jump():
    pyautogui.keyDown('space')
    pyautogui.keyUp('space')

def down():
    pyautogui.keyDown('down')
    pyautogui.keyUp('down')

'''
    Execute the game with a model saved in a file.
    restartButton is the coordinates of the restart button.
'''
def execute( file_name, restartButton=(528,410)):
    genome = Network(file_n=file_name)

    pyautogui.click(restartButton)
    vision = Vision()
    vision.find_game()

    vision.reset()
    sleep(1)
    jump()
    while True:
        try:
            obs = vision.find_next_obstacle()
            inputs = [obs['distance']/1000, obs['lenght']/70000, obs['height']/1000, obs['speed']/15]
            outputs = genome.forward(np.array(inputs, dtype=float))
            if outputs[0] > 0.55:
                jump()
        except Exception as e:
            break

'''
    Genetic Algorithm definition.
'''
class Generation:
    def __init__(self):
        self.__genomes = [ Network() for i in range(12) ]
        self.__best_genomes = []
        self.mut = 0.5
        self.fileName = 'best'
        self.count = 0
        random.seed( datetime.datetime.now())

    '''
        Execute the Learning process.
    '''
    def execute( self, restartButton=(528,410) ):
        print("executing!")
        pyautogui.click(restartButton)
        vision = Vision()
        vision.find_game()
        print(len(self.__genomes))
        gen = 0

        for genome in self.__genomes:
            print("genome "+str(gen), end="")
            gen += 1
            vision.reset()
            sleep(1)
            jump()
            dec = 0
            while True:
                try:
                    obs = vision.find_next_obstacle()
                    inputs = [obs['distance']/1000, obs['lenght']/70000, obs['height']/1000, obs['speed']/10]
                    outputs = genome.forward(np.array(inputs, dtype=float))
                    if outputs[0] > 0.55:
                        jump()
                        dec-=1
                except Exception as e:
                    break
            genome.fitness = vision.get_fitness()
            print(", fitness: "+str(genome.fitness))

    def keep_best_genomes(self):
        print("best genomes!")
        self.__genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.__genomes = self.__genomes[:4]
        self.__best_genomes = self.__genomes[:]
        self.save(self.__best_genomes[0])

    '''
        Save model in a file. file name: "best<model_fitness>.bcp"
    '''
    def save(self, gene):
        f = open(self.fileName+str(gene.fitness)+".bcp", 'w')
        f.write(str(gene.input_size)+" "+str(gene.hidden_size)+" "+str(gene.output_size))
        f.write(" "+str(gene.fitness)+"\n")
        #input
        for line in gene.W1:
            for w in line:
                f.write(str(w)+" ")
            f.write("\n")
        f.write("\n")

        #hidden
        for line in gene.W2:
            for w in line:
                f.write(str(w)+" ")
            f.write("\n")

        f.close()

    '''
        Mutation operation.
    '''
    def mutations(self):
        print("mutating!")
        while len(self.__genomes)<10:
            genome1 = random.choice(self.__best_genomes)
            genome2 = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(self.cross_over(genome1, genome2)))
        while len(self.__genomes) < 12:
            genome = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(genome))

    '''
        Cross Over operation.
    '''
    def cross_over(self, genome1, genome2):
        new_genome = copy.deepcopy(genome1)
        other_genome = copy.deepcopy(genome2)
        cut_location = int(len(new_genome.W1) * random.uniform(0,1))
        for i in range(cut_location):
            new_genome.W1[i], other_genome.W1[i] = other_genome.W1[i], new_genome.W1[i]
        cut_location = int(len(new_genome.W2) * random.uniform(0,1))
        for i in range(cut_location):
            new_genome.W2[i], other_genome.W2[i] = other_genome.W2[i], new_genome.W2[i]
        return new_genome

    '''
        Individual mutation.
    '''
    def __mutate_weights(self, weights):
        if random.uniform(0,1) < 0.2:
            return weights*(random.uniform(0,1) - 0.5) * 3 + (random.uniform(0,1) - 0.5 )
        else:
            return 0

    def mutate(self, genome):
        new_genome = copy.deepcopy(genome)
        new_genome.W1 += self.__mutate_weights(new_genome.W1)
        new_genome.W2 += self.__mutate_weights(new_genome.W2)
        return new_genome