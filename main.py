import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import interpolate

matplotlib.use('TkAgg')

# Constants
material_y_width = 100
material_x_z_width = 10
number_of_electrons_wide = 5
number_of_layers = 7
charge_electron = 1 / number_of_electrons_wide ** 2  # this is to ensure the amount of charge per layer is constant
TIME_END = 100
TIME_STEPS = 100
DT = TIME_END / TIME_STEPS
number_of_evaluation_points = 1000  # make this larger for more resolution in the x-axis
c = 1  # speed of light
hookes_constant = 0.1
mass_electron = 1
damping_constant = 0
sigma = 5
resonant_angular_frequency = np.sqrt(hookes_constant / mass_electron)
angular_frequency = resonant_angular_frequency * 0.99
pulse_time = 100
pulse_amp = 1

fig, ax = plt.subplots()
ax.set_ylim(-1, 1)
x_f = np.linspace(0, TIME_END, number_of_evaluation_points)
line, = ax.plot(x_f, np.zeros(x_f.shape))


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

def animate(t):
    # pulse is the field at x=0 at time t=interp
    # So pulse at (t,xt) = xt - time to travel from x=0
    # yd = np.interp((-x_f/c)+t, px*pulse_time, py*pulse_amp)
    yyy = np.interp(xpts/c+20-t, xpts, y, left=0, right=0)
    line.set_ydata(yyy)
    # line.set_ydata(pulse[t,:])
    # if (t < new_pulse[:,0].size):
    #     line.set_ydata(new_pulse[t,:])
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
    # py = single_pulse_sin()
    # px = np.linspace(0, 1, py.size)
    # intp = np.interp(x_f, px*pulse_time, py*pulse_amp)
    # pi = interpolate.interp1d(px * pulse_time, py * pulse_amp, kind='linear', fill_value='interpolate', assume_sorted=True)
    # poff = -pulse_time

    # t_f = np.arange(stop=TIME_END, step=DT)
    # new_pulse = multi_pulse(t_f, x_f)
    xpts = np.linspace(-25, 25, 1000)
    y = single_pulse(xpts)
    yy = interpolate.interp1d(xpts, y, kind='linear', fill_value='extrapolate')

    yyy = np.interp(xpts+20, xpts, y, left=0, right=0)
    #
    # spulse = interpolate.interp1d(pul_x*5, pul*pulse_amp, kind='linear',fill_value='extrapolate')

    ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
    plt.show()
    pass
