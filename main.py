import numpy as np
import matplotlib
import itertools
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


def gaussian(t):
    exponential_term = np.exp(-0.5 * ((t/sigma) ** 2))
    return exponential_term

# Returns pulse from about -15 to 15. Or can sim from -20 to 20
# If propagating from right to left, I can calculate what the value would be for
#  value(t,x) = single_pulse(20 - t*DT - x/c)

def single_pulse(t):
    eq = gaussian(t)*np.sin(t)
    return eq

def animate(t):
    # pulse is the field at x=0 at time t=interp
    # So pulse at (t,xt) = xt - time to travel from x=0
    # yd = np.interp((-x_f/c)+t, px*pulse_time, py*pulse_amp)
    field = interp_times(x_f/c - t)
    line.set_ydata(field)
    # assert (x_f.size == np.shape(e_scaling)[2])
    esum = np.zeros(x_f.shape)
    # eminor = interp_times(t-time_x_mat[i, :, :])*e_scaling[i, :, :]
    for i in range(x_f.size):
        val = np.sum(np.multiply(interp_times(t-time_x_mat[i, :, :]), e_scaling[i,:,:]))
        esum[i] = val
    e_field_line.set_ydata(esum)

    return line,e_field_line

def interp_times(t):
    y = np.interp(t, tpts, y_pulse, left=0, right=0)
    return y

def square_y_component(pt):
    return np.square(pt[0])

def square_point(pt):
    return np.sum(np.square(pt))

if __name__ == '__main__':
    # t_f = np.arange(stop=TIME_END, step=DT)
    # new_pulse = multi_pulse(t_f, x_f)
    x_f = np.linspace(0, TIME_END, number_of_evaluation_points)
    tpts = np.linspace(-25, 25, 100)
    y_pulse = single_pulse(tpts)

    yspacing = 1
    ycount = 100
    y_arr = np.linspace(yspacing/2, (ycount-1)*yspacing + yspacing/2, ycount)

    zspacing = 1
    zcount = 100
    z_arr = np.linspace(zspacing/2, (zcount-1)*zspacing + zspacing/2, zcount)

    all_2d_points = list(itertools.product(set(y_arr), set(z_arr)))
    dist_squared_list = list(map(square_point, all_2d_points))
    y_squared_list = list(map(square_y_component, all_2d_points))

    # dist_squared_list.sort() # having the distances sorted may speed up interpolation
    #
    # dist_x_mat = np.ndarray((x_f.size, dist_squared_list.count()))
    attenuation = [None]*x_f.size
    time_delay = [None]*x_f.size
    for i in range(x_f.size):
        x = x_f[i]
        x2 = np.square(x)
        points = list(all_2d_points)
        dist_squared_list = list(map(np.add, dist_squared_list, [x2]* len(dist_squared_list)))

        atten_list = np.divide(y_squared_list, dist_squared_list) - 1.0
        time_delay_list = np.divide(list(map(np.sqrt, dist_squared_list)), c)
        at = list(zip(time_delay_list, atten_list))
        at.sort()
        attenuation[i] = np.array([x for x,y in at])
        time_delay[i] = np.array([y for x,y in at])

    # time_x_mat = np.divide(dist_x_mat, c)
    # # e_scaling = np.tile(y_mat, (1, 1, x_f.size))
    # y_temp = np.repeat(y_mat[np.newaxis, :, :], x_f.size, axis=0)
    #
    # # e_scaling = (y^2/l^2-1)
    # e_scaling = np.divide(np.square(y_temp),np.square(dist_x_mat) + np.square(y_temp))-1

    # ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
    # plt.show()

    # fig, ax = plt.subplots(sharex=True, sharey=True, nrows=1, ncols=1)
    # ax.set_ylim(-1, 1)
    # line, = ax.plot(x_f, np.zeros(x_f.shape))
    # e_field = ax.twinx()
    # e_field_line, = e_field.plot(x_f, np.zeros(x_f.shape), color="#FF0000", label="aggregate")

    points = [-50, -45, -30, -20, -10]
    print (interp_times(points))
    pass
