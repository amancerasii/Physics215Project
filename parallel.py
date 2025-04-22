from multiprocessing import Pool
import random as random
import time as time

def f(x):
    for i in range(10):
        x += random.random()*i*x
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3, 4, 6, 7, 8, 9]))