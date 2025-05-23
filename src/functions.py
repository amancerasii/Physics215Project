import numpy as np
from lattice import Lattice
from njitwolff import *

def isingrun(N,T,h):
    lattice = Lattice(N, T, h)
    M = []

    for i in range(1000):
        lattice.spins = wolff(lattice.spins, lattice.N, lattice.b)

    for i in range(1000):
        lattice.spins = wolff(lattice.spins, lattice.N, lattice.b)
        M.append(np.abs(lattice.spins.mean()))

    plt.plot(M)
    print(np.mean(M))

