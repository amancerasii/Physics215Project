# JIT parallel 2D Ising Model
This is a simple implementation of Numba's JIT compilation and Python's `multiprocessing` parallelization on a 2D Ising model that uses 

## Dependencies
Conda

## Installation

1. Create the environment from the environment.yml file:
    ```
    conda env create -f environment.yml
    ```
2. Activate the environmant
    ```
    conda activate 215Project
    ```

## Setting simulation parameters
To set the simulation parameters, modify the `config.ini` file in the root directory.

### trial number : integer

A number indicating the trial of the run. Each trial number is a unique random seed of the run. Do not change if you want to use the same seed.

### lattice size : integer, multiples of 2
The square lattice used in the simulation is of this value L. The resulting lattice is a L$\times$L lattice.

### start t, end t : float
The simulation will use temperature values from `start t` to `end t`. The number of points in between is defined by `number of t`.

### number of t : integer
The number of temperature points to be simulated

### ss points : integer
Number of steady state time steps to record. There is a 2000 time step equilibriation implemented before the `ss points` time steps.

### cores : integer
For parallel and njitparallel, the number of CPU cores to be used.

## Running the simulation
The simulation codes are stored in the `/src` folder. Run the specific python code you want. The simulation times are stored in `/data/times.txt` and the data files will be saved in the `/data` folder

### base
The base python code without any optimization
```
python base.py
```

### njit
Python code with the Numba JIT compilation
```
python njit.py
```
### parallel
Python code with `multiprocessing` parallelism. Make sure you set the proper `cores` value in the `config.ini` file.

```
python parallel.py
```

### njitparallel
Python code with both Numba JIT compilation and `multiprocessing` parallelism.
```
python njitparallel.py
```

---

### Testing Results
Testing results showed improvements in calculation time for all optimization schemes with no loss in accuracy. [detailed report](Testing documentation.md)
