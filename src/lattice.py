import numpy as np

class Lattice:
    def __init__(self, N, T, h):
        assert N % 2 == 0
        assert T > 0

        self.N = N
        self.b = 1/T
        self.h = h


        self.spins = (2 * (np.random.randint(0, 2, (N, N)) - 0.5))


    def get_energy(self):
        return np.sum(-self.b * self.spins
            * (np.roll(self.spins, 1, 0) + np.roll(self.spins, 1, 1)) - self.h * self.spins)
