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
c = 0.3  # speed of light
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
    eq = gaussian(t)*np.sin(t)
    eq[0] = eq[1] = eq[-1] = eq[-2] = 0
    return eq

def animate(t):
    # pulse is the field at x=0 at time t=interp
    # So pulse at (t,xt) = xt - time to travel from x=0
    # yd = np.interp((-x_f/c)+t, px*pulse_time, py*pulse_amp)
    field = interp_times(t)
    line.set_ydata(field)
    # line.set_ydata(pulse[t,:])
    # if (t < new_pulse[:,0].size):
    #     line.set_ydata(new_pulse[t,:])
    return line,

def interp_times(t):
    y = np.interp(t-x_f/c, tpts, y_pulse, left=0, right=0)
    return y

if __name__ == '__main__':
    # t_f = np.arange(stop=TIME_END, step=DT)
    # new_pulse = multi_pulse(t_f, x_f)
    tpts = np.linspace(-25, 25, 1000)
    y_pulse = single_pulse(tpts)

    # yyy = np.interp(tpts+20, tpts, y, left=0, right=0)
    #
    # spulse = interpolate.interp1d(pul_x*5, pul*pulse_amp, kind='linear',fill_value='extrapolate')

    ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
    plt.show()
    pass
