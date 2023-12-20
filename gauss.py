import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate
matplotlib.use('TkAgg')

hookes_constant = 0.1
mass_electron = 1
damping_constant = 0
sigma = 5
c = 1

def gaussian(t):
    exponential_term = np.exp(-0.5 * ((t/sigma) ** 2))
    return exponential_term

# Returns pulse from about -15 to 15. Or can sim from -20 to 20
# If propagating from right to left, I can calculate what the value would be for
#  value(t,x) = single_pulse(20 - t*DT - x/c)

def single_pulse(t):
    eq =gaussian(t)*np.sin(t)
    eq[0] = eq[1] = eq[-1] = eq[-2] = 0
    return eq

if __name__ == '__main__':
    xpts = np.linspace(-25, 25, 1000)
    y = single_pulse(xpts)
    yy = interpolate.interp1d(xpts, y, kind='linear', fill_value='extrapolate')

    yyy = np.interp(xpts+20, xpts, y, left=0, right=0)

    plt.plot(xpts, yyy)
    plt.xlabel('t')
    plt.ylabel('y')
    plt.title('Gaussian Function')
    plt.show()
    print(np)
    pass