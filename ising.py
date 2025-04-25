import numpy as np
import matplotlib.pyplot as plt
import numba
from numba import njit
from scipy.ndimage import convolve, generate_binary_structure

N = 20

# Create Random Negative Lattice
init_random = np.random.random((N,N))
lattice_n = np.zeros((N,N))
lattice_n[init_random >= 0.75] = 1
lattice_n[init_random < 0.75] = -1

# Create Random Positive Lattice
init_random = np.random.random((N,N))
lattice_p = np.zeros((N,N))
lattice_p[init_random >= 0.25] = 1
lattice_p[init_random < 0.25] = -1

def get_energy(lattice):
    kern = generate_binary_structure(2,2)
    kern[1][1] = False
    arr = -lattice * convolve(lattice, kern, mode='constant')
    return arr.sum()

@numba.njit("UniTuple(f8[:], 2)(f8[:,:], i8, f8, f8)", nopython=True, nogil=True)

def metropolis(spin_arr, times, BJ, energy):
    spin_arr = spin_arr.copy()
    net_spins = np.zeros(times-1)
    net_energy = np.zeros(times-1)

    for t in range(0,times-1):
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
    
spins, energies = metropolis(lattice_n, 100000, 0.7, get_energy(lattice_n))
plt.plot(energies)
plt.show()
