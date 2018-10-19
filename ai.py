from generation import Generation
import generation
import sys

def main():
    generation = Generation()
    i=0
    while True:
        print("Generation "+str(i)+":")
        i += 1
        generation.execute()
        generation.keep_best_genomes()
        generation.mutations()

def exe(file_n):
    while True:
        generation.execute(file_n)

if __name__ == '__main__':
    if len(sys.argv)<=1:
        main()
    else:
        exe(sys.argv[1])