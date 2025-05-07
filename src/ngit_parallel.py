import numpy as np
import matplotlib.pyplot as plt
from numba import njit
from scipy.ndimage import convolve, generate_binary_structure
import time
from multiprocessing import Pool

tstart = time.perf_counter()

def get_energy(lattice):
    kern = generate_binary_structure(2,2)
    kern[1][1] = False
    arr = -lattice * convolve(lattice, kern, mode='constant')
    return arr.sum()

@njit(nopython=True)
def metropolis(spin_arr, times, BJ, energy,N):
    spin_arr = spin_arr.copy()
    net_spins = np.zeros(times)
    net_energy = np.zeros(times)

    for t in range(0,times):
        # pick random point on array and flip spin
        x = np.random.randint(0,N)
        y = np.random.randint(0,N)
        spin_i = spin_arr[x,y] # initial spin
        spin_f = spin_i*-1 # proposed spin flip

        # compute change in energy
        E_i = 0
        E_f = 0
        if x > 0:
            E_i += -spin_i*spin_arr[x-1,y]
            E_f += -spin_f*spin_arr[x-1,y]
        if x < N-1:
            E_i += -spin_i*spin_arr[x+1,y]
            E_f += -spin_f*spin_arr[x+1,y]
        if y > 0:
            E_i += -spin_i*spin_arr[x,y-1]
            E_f += -spin_f*spin_arr[x,y-1]
        if y < N-1:
            E_i += -spin_i*spin_arr[x,y+1]
            E_f += -spin_f*spin_arr[x,y+1]

        dE = E_f - E_i
        if (dE > 0)*(np.random.random() < np.exp(-BJ*dE)) or dE <= 0:
            spin_arr[x,y] = spin_f
            energy += dE
       
        net_spins[t] = spin_arr.sum()
        net_energy[t] = energy

    return net_spins, net_energy

def isingRun(seed):


    np.random.seed(seed)

    # Create Random Negative Lattice
    init_random = np.random.random((N,N))
    lattice_n = np.zeros((N,N))
    lattice_n[init_random >= 0.5] = 1
    lattice_n[init_random < 0.5] = -1

    if mode == 'base' or mode == 'parallel':
        spins, energies = metropolis(lattice_n, t, B, get_energy(lattice_n),N)
    elif mode == 'njit' or mode == 'njitparallel':
        spins, energies = metropolisnjit(lattice_n, t, B, get_energy(lattice_n),N)

    return spins, energies

###############################################################################

t = 100000
runs = 120
N = 10
B = 1/2
cores = 5

if __name__ == '__main__':
    # tspins = np.zeros(t)
    # for r in range(runs):
    #     spins, energies = isingRun(r)
    #     tspins = tspins + spins

    with Pool(cores) as p:
        val = p.map(isingRun, np.arange(0,runs))

        
        tspins = np.zeros(t)
        tenergy = np.zeros(t)
        for i in range(runs):
            tspins = tspins + val[i][0]
            tenergy = tenergy + val[i][1]

        calctime = time.perf_counter() - tstart
        print('ngit_parallel',calctime)
        plt.plot(tspins)
        plt.plot(tenergy)
        plt.show()
