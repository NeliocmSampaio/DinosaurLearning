from generation import Generation
import generation
import sys

'''
    Run the genetic algorithm.
'''
def main():
    generation = Generation()
    i=0
    while True:
        print("Generation "+str(i)+":")
        i += 1
        generation.execute()
        generation.keep_best_genomes()
        generation.mutations()

'''
    Load a model from a file.
'''
def exe(file_n, ):
    while True:
        generation.execute(file_n)

if __name__ == '__main__':
    trainModel = False

    if len(sys.argv)>1:
        exe(sys.argv[1])
    else:
        main()