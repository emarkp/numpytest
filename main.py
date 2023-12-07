import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import matplotlib.animation as animation
matplotlib.use('TkAgg')
#from scipy import interpolate

# Constants
material_y_width = 100
material_x_z_width = 10
number_of_electrons_wide = 5
number_of_layers = 7
charge_electron = 1 / number_of_electrons_wide ** 2  # this is to ensure the amount of charge per layer is constant
TIME_END = 100
TIME_STEPS = 1000
DT = TIME_END / TIME_STEPS
number_of_evaluation_points = 1000  # make this larger for more resolution in the x axis
c = 5  # speed of light
hookes_constant = 0.1
mass_electron = 1
damping_constant = 0
sigma = 5
resonant_angular_frequency = np.sqrt(hookes_constant / mass_electron)
angular_frequency = resonant_angular_frequency * 0.99

fig, ax = plt.subplots()
ax.set_ylim(-1,1)
x_f = np.linspace(0, TIME_END, number_of_evaluation_points)
line, = ax.plot(x_f, np.zeros(x_f.shape))

def gaussian(t, y):
    coefficient = 5 / (sigma * np.sqrt(2 * np.pi))
    exponential_term = np.exp(-0.5 * ((c * t - y) / sigma) ** 2)
    # exponential_term = np.exp(-0.5 * ((y + c * t - material_y_width / 4) / sigma) ** 2)
    return coefficient * exponential_term

def single_pulse():
    pulse = np.sin(np.linspace(0,100, 200)*(-2)*(np.pi/100))
    pulse[0]=pulse[-1]=0
    return pulse


def animate(t):
    line.set_ydata(pulse[t,:])
    return line,

if __name__ == '__main__':
    # xvals = np.array([ 166, 167, 168, 170, 171, 173, 181, 183, 190, 196, 208, 230, 244, 274, 289, 312, 346, 367, 382, 398, 412, 417, 426, 432, 437, 443, 447, 453, 459, 464, 468, 471, 472, 475, 477, 482, 486, 488, 490])
    # yvals = np.array([ 0, 0.17, 0.35, 0.5, 0.58, 0.81, 1.34, 1.43, 1.62, 1.72, 1.82, 1.96, 2.06, 2.28, 2.41, 2.62, 2.99, 3.28, 3.54, 3.84, 4.17, 4.3, 4.58, 4.8, 4.99, 5.24, 5.44, 5.76, 6.16, 6.57, 6.92, 7.18, 7.34, 7.7, 7.98, 9, 9.99, 10.92, 11.99])
    # f = interpolate.interp1d(xvals,yvals,kind='linear',fill_value='extrapolate')
    # for x in range(166,490,1):
    #   print (f'val[{x}] = {f(x):.2f};')

    # We are only going to evaluate the field along the line y = 0, z = 0. These are the y values for those points
    # Also, our convention will be to pack arrays so that the final index is the values associated w/ x
    # print(x_f)

    t_f = np.arange(stop=TIME_END, step=DT)

    x_mat = np.tile(x_f, (t_f.size, 1 ))
    t_mat = np.transpose(np.tile(t_f, (x_f.size, 1 )))

    pulse = gaussian(t_mat, x_mat)
    pul = single_pulse()

    ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
    plt.show()
    pass