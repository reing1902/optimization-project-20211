import random as rd
import os

def gen_data(N, K, filename=None):
    '''
    Create a txt data file in data folder.

    Parameters
    ----------
    filename : str
        The name of the file to be generated
    N : int
        The number of nodes in the graph
    K : int
        The number of vehicles in the fleet
    '''
    if not filename:
        filename = f'N{N}-K{K}.txt'

    os.chdir('data')
    with open(filename, 'w') as f:
        f.write(f'{N} {K}\n')
        for _ in range(N):
            f.write(f'{rd.randint(1, 100)} ')
        f.write('\n')
        for i in range(N+1):
            for j in range(N+1):
                if i == j:
                    f.write('0 ')
                else:
                    f.write(f'{rd.randint(1, 100)} ')
            f.write('\n')

    os.chdir('..')

def main():
    gen_data(3, 6)

if __name__ == '__main__':
    main()
