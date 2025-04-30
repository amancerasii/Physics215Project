# Physics215Project
Git Repository of My Physics 215 Requirement

Future plans
- write monte carlo simulation code
- use multiprocessing package
- use numba for JIT compilation package
- compare performance of parallel code
    - accuracy and simulation time
        - find an apt simulation time measure


Citing `multiprocess` developers

M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
"Building a framework for predictive science", Proceedings of
the 10th Python in Science Conference, 2011;
http://arxiv.org/pdf/1202.1056

Michael McKerns and Michael Aivazis,
"pathos: a framework for heterogeneous computing", 2010- ;
https://uqfoundation.github.io/project/pathos

Ising model with numba integration tutorial
https://www.youtube.com/watch?v=K--1hlv9yv0&ab_channel=Mr.PSolver


Things to implement:

# Metropolis Runplan up to phase transition diagram
## Variables
N - lattice size
t - number of time steps per run
r - number of runs (to average over)
npoints - number of steady state points to average
B values - \(\beta = 1/k_Bt \)
## Steps


# Speed up schemes:
basic njit
`@ngit(nopython=True)`

# Standard Test Configuration
N = 50
t = 1000000
runs = 100
Bvals = 0.44
