import matplotlib.pyplot as plt
from source.TIDHA import *

# Get this file's directory
directory, _, _ = split_path_name_extension(__file__)

# Define pile locations
mm = 1e-3
pile_xs = np.array([
    [-6755*mm, 750*mm],
    [-5250*mm, -2255*mm],
    [5250*mm, -2255*mm],
    [6755*mm, 750*mm]
])

# Define pile stiffness [ux, uy, rx, ry]
pile_k = np.array([[  172823.0896, 0, 0, 0], [ 0, 172823.0896, 0, 0], [ 0, 0 ,  0, 0] , [ 0, 0, 0, 0]])

# Pile fixity to approximate mass contribution of the pile, taken from pile's lateral force analysis
pile_L_fixity = 8

# Define pile mass [mux muy mrx mry]
pile_m = np.array([[  277, 0, 0, 0], [ 0, 277, 0, 0], [ 0, 0 ,  0, 0] , [ 0, 0, 0, 0]])*7850*pile_L_fixity*np.pi*(0.4**2 - (0.4 - 0.008)**2)/420

# Solve the system
solve_time_series_hydrodynamics(
    directory = directory,
    dT = 0.02,
    dTeval = 0.1,
    Tmax = 100,
    Hs = 1.64,
    Tp = 10.33,
    pile_xs = pile_xs,
    pile_k = pile_k,
    pile_m = pile_m
)

# Read output file
output_file = parse_file(directory + '\Pontoon_TIDHA_Out.txt').T

# Plot the output file
plt.plot(output_file[0], output_file[1], label = "Wave Height")
plt.plot(output_file[0], output_file[4], label = "Heave")
plt.legend(loc = 'best')
plt.show()