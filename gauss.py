import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

hookes_constant = 0.1
mass_electron = 1
damping_constant = 0
sigma = 5
c = 1

def gaussian(t):
    exponential_term = np.exp(-0.5 * ((t/sigma) ** 2))
    return exponential_term

if __name__ == '__main__':
    t = np.linspace(-25, 25, 1000)
    y = gaussian(t)
    sy = np.sin(t)
    y = y  * sy

    plt.plot(t, y)
    plt.xlabel('t')
    plt.ylabel('y')
    plt.title('Gaussian Function')
    plt.show()
    print(np)
    pass