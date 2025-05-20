import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filename = "t2_base_l10ts2000r5"

N = 64*64

# Get spin and energy data
# edata = np.loadtxt("../data/"+filename+"_energy.txt")
sdata = np.loadtxt("../data/"+filename+"spin.txt")

Tvals = sdata[0,:]
# Eave = np.mean(edata[2:,:],axis=0)
# Esqave = np.mean(edata[2:,:]**2,axis=0)

Mave = np.mean(sdata[2:,:],axis=0)
Msqave = np.mean(sdata[2:,:]**2,axis=0)

# Cvals = np.divide(Esqave - Eave**2,N*Tvals**2)

Xvals = np.divide(Msqave - Mave**2, Tvals*N)

def lorentzian(T, Tc, A, B):
    return A/((T-Tc)**2 + B)
 
popt, pcov = curve_fit(lorentzian, Tvals, Xvals)

xdata = np.linspace(1,5,100)

print("T =",popt[0])

plt.scatter(Tvals,Xvals)
plt.plot(xdata,lorentzian(xdata, *popt))
plt.show()