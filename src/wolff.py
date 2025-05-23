import numpy as np
from numba import njit

def wolff(spins, N, b):
        i, j = np.random.randint(0, N), np.random.randint(0, N)
        S = spins[i,j]
        C = [[i,j]]
        F_old = [[i,j]]
        p = 1. - np.exp(-2 * b)

        while len(F_old) > 0:
            F_new = []

            for i,j in F_old:
                neighbours = [[(i+1) % N,j], [(i-1+N) % N,j], [i,(j+1) % N], [i,(j-1+N) % N]]

                for neighbour in neighbours:
                    if spins[neighbour[0],neighbour[1]] == S and neighbour not in C:
                        if np.random.rand() < p:
                            F_new.append(neighbour)
                            C.append(neighbour)

            F_old = F_new

        for i,j in C:
            spins[i,j] *= -1

        M = np.abs(spins.mean())

        return spins, M
