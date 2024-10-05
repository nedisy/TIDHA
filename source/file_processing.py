import os
from numpy.typing import NDArray
import numpy as np

# Read the file, skipping the header lines and parsing data
def parse_file(file_path: str) -> NDArray[np.float64]:
    """
    Read text file in the format of space-separated value and return numpy array
    """
    with open(file_path, 'r') as file:
        # Skip the first lines with metadata and headers
        lines = file.readlines()
        start_idx = 0
        for idx, line in enumerate(lines):
            if line.strip().startswith("Time"):  # Detect when the actual data starts
                start_idx = idx + 2
                break

        # Load the numerical data, skipping non-numeric rows
        data = np.genfromtxt(lines[start_idx:], delimiter=None)
    return data

def split_path_name_extension(file_path: str):
    '''
    Split path to directory, name, and extension
    '''
    # Get the directory path
    directory = os.path.dirname(file_path)
    # Get the base name (file name with extension)
    base_name = os.path.basename(file_path)
    # Find the last dot to split the name and extension
    last_dot_index = base_name.rfind('.')
    
    if last_dot_index != -1:
        name = base_name[:last_dot_index]  # Name without extension
        ext = base_name[last_dot_index:]    # Extension with dot
    else:
        name = base_name
        ext = ''  # No extension

    return directory, name, ext

def import_wamit(path: str):
    '''
    # Import WAMIT File from path of any of the file with the name\n
    \n
    All formulas used refer to the Wamit specification at [Wamit Manual](https://www.wamit.com/manualv7.4/wamit_v74manualch3.html)\n
    \n
    ## Input\n
    `path`, expected .hst, .frc, .1, .3, .pot file from the same path with the same name\n
    \n
    ## Returns\n
    1. rho_water: Water density, (kg/m3)\n
    2. Mass: Mass Matrix, (6 x 6) (kg)\n
    3. Hstiff: Hydrostatic stiffness matrix, (6 x 6)\n
    4. Hw: Water Depth, (m)\n
    5. beta: wave angle, (deg)\n
    6. Xbody: Body's center coordinate center relative to global, [x y z ry] (m)\n
    7. CGbody: Body's center of gravity accroding to body's coordinate system, [x y z] (m)\n
    8. omega_i: Periods (float N) (rad/s)\n
    9. A_0: Added mass at zero frequency (float 6 x 6) (kg)\n
    10. A_inf: Added mass at infinite frequency (float 6 x 6) (kg)\n
    11. A_i: Added mass at period of T_i (float 6 x 6 x N_period) (kg)\n
    12. B_i: Radiation damping at period of T_i (float 6 x 6 x N_period) (N/(m/s)$^2$)\n
    13. Fex_i: Exciting force from incoming and diffraction wave (complex 6 x N_period x N_heading) (N/m)\n
    \n
    ## Example usage:\n
    `rho_water, Mass, Hstiff, Hw, beta, Xbody, CGbody, omega_i, A_0, A_inf, A_i, B_i, Fex_i = import_wamit(".\ship.1")`
    '''
    # Split path to dir, name, ext
    dir, name, ext = split_path_name_extension(path)



    # Read potential control file
    with open(f"{dir}\{name}.pot", 'r') as dotpot:
        # Read the lines to list of strings
        dotpotlines = dotpot.readlines()


    # Water Depth
    Hw = float(dotpotlines[1].split()[0])

    # Number of frequencies
    Ni = int(dotpotlines[3].split()[0])

    # Periods
    omega_i = 2*np.pi/np.array(dotpotlines[4].split()[:Ni]).astype(np.float64)
    omega_i.sort()

    # Number of incident angles
    Nbeta = int(dotpotlines[5].split()[0])

    # incident angles
    beta = np.array(dotpotlines[6].split()[:Nbeta]).astype(float)
    
    # body reference point
    Xbody = np.array(dotpotlines[9].split()[:4]).astype(float)



    # Read force control file
    with open(f"{dir}\{name}.frc", 'r') as dotfrc:
        # Read the lines to list of strings
        dotfrclines = dotfrc.readlines()

    # Water Density
    rho_water = float(dotfrclines[2].split()[0])

    # Mass Matrix
    Mass = np.zeros((6,6))
    for i, line in enumerate(dotfrclines[5:11]):
        Mass[i] = np.array(line.split()[:6]).astype(float)


    # Body's center of gravity according to body's coordinate system
    CGbody = np.array(dotfrclines[3].split()[:3]).astype(float)


    

    # Read hydrostatic stiffness file
    with open(f"{dir}\{name}.hst", 'r') as dothst:
        # Read the lines to list of strings
        dothstlines = dothst.readlines()

    # Hydrostatic stiffness matrix
    Hstiff = np.zeros((6,6))
    for line in dothstlines:
        splitted = line.split()
        i = int(splitted[0]) - 1
        j = int(splitted[1]) - 1
        Hstiff[i,j] = splitted[2]

    Hstiff *= rho_water * 9.8066


    # Read Added Mass and Radiation Damping 
    dot1data1 = np.loadtxt(f"{dir}\{name}.1", max_rows=72)
    dot1data2 = np.loadtxt(f"{dir}\{name}.1", skiprows=72)

    # Define initial arrays
    A_0 = np.zeros((6,6))
    A_inf = np.zeros((6,6))
    A_i = np.zeros((6,6,Ni))
    B_i = np.zeros((6,6,Ni))
    
    # Process the infinite frequency damping
    for line in dot1data1[:36]:
        # Extract i, j, and value
        i = int(line[1]) - 1  # Convert to 0-based index
        j = int(line[2]) - 1  # Convert to 0-based index
        value = float(line[3])
        
        # Assign the value to the corresponding position in the array
        A_0[i, j] = value*rho_water
        
    # Process the zero frequency damping
    for line in dot1data1[36:]:
        # Extract i, j, and value
        i = int(line[1]) - 1  # Convert to 0-based index
        j = int(line[2]) - 1  # Convert to 0-based index
        value = float(line[3])
        
        # Assign the value to the corresponding position in the array
        A_inf[i, j] = value*rho_water

    # Process frequencies damping
    for line in dot1data2:
        # Extract i, j, and value
        i = int(line[1]) - 1  # Convert to 0-based index
        j = int(line[2]) - 1  # Convert to 0-based index
        A_value = float(line[3])
        B_value = float(line[4])
        k = np.where(np.abs(omega_i - 2*np.pi/line[0]) < 1e-3)
        
        # Assign the value to the corresponding position in the array
        A_i[i, j, k] = A_value*rho_water
        B_i[i, j, k] = B_value*rho_water*2*np.pi/line[0]

    # Read exciting force from diffraction
    dot3data = np.loadtxt(f"{dir}\{name}.3")

    # Define initial arrays
    Fex_i = np.zeros((6,Ni,Nbeta)).astype(np.complex128)

    # Process the exciting force into array
    for line in dot3data:
        # Extract i, j, and value
        i = int(line[2]) - 1  # Convert to 0-based index
        Re_value = float(line[5])
        Im_value = float(line[6])
        
        # angle index
        j = np.where(np.abs(omega_i - 2*np.pi/line[0]) < 1e-3)
        k = np.where(np.abs(beta - line[1]) < 1e-3)
        # Assign the value to the corresponding position in the array
        Fex_i[i, j, k] = (Re_value + Im_value*1j)*rho_water*9.8066

    return rho_water, Mass, Hstiff, Hw, beta, Xbody, CGbody, omega_i, A_0, A_inf, A_i, B_i, Fex_i




