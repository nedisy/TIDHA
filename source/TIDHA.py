import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp, simpson
from source.file_processing import *
from source.hydrodynamic_forces import *
from source.pile_forces import *
from source.ocean_spectra import *


def solve_time_series_hydrodynamics(directory: str,
                                    dT: float,
                                    dTeval: float,
                                    Tmax: float,
                                    Hs: float,
                                    Tp: float,
                                    pile_xs: NDArray[np.float64],
                                    pile_k: NDArray[np.float64],
                                    pile_m: NDArray[np.float64],
                                    damp_high_freq = False,
                                    high_freq_cutoff = 10,
                                    ) -> None:
    """
    # Solve time series analysis for hydrodynamics problem.\n
    It will save output file into `[directory]\\Pontoon_TIDHA_Out.txt`. The file contains, in the form of space
    separated values: Time, Wave Height, Positions array(6), Velocities array(6)\n
    \n
    ## Inputs\n
    1. `directory`\n
    The main directory for processing. It expect there to be `[directory]\\Wamit_format\\Pontoon.1` folder containing
    preprocessed hydrodynamic data of the floating structure/Pontoon in Wamit format.\n
    2. `dT` and `dTeval`\n
    The interval for various calculations. For internal calculations, specified as `dT` and it should be less
    than the highest natural frequency of the system divided by ten. Evaluation for values to be saved is based on `dTeval`.\n
    3. `Hs` and `Tp`\n
    Both parameters represent the sea state for the analysis.\n
    4. `pile_xs`, `pile_k`, and `pile_m`\n
    Respectively: pile positions array[x, y], pile stiffness matrix with shape(4, 4) that ignores u_z and r_z,
    and pile mass matrix also with shape(4, 4). The stiffness and mass matrix refers to the contact point of the pile.\n
    5. `damp_high_freq` and `high_freq_cutoff`\n
    Optionaly damp high frequency vibrations above `high_freq_cutoff` in Hz (10 Hz by default). This functionality is 
    disabled by default, might be required for stiff problem.
    """
    # start timer to time the whole operation
    tstart = time.time()

    rho_water, Mass, Hstiff, Hw, beta, Xbody, CGbody, omega_i, A_0, A_inf, A_i, B_i, Fex_i = import_wamit(directory + r"\Wamit_format\Pontoon.1")

    # Prepare constant variables
    g = 9.8066

    # times at which excitation forces are calculated
    exctnTime = np.arange(0, Tmax + dT, dT)

    # times at which wave height, position, and acceleration is calculated
    evalTime = np.arange(0, Tmax + dTeval, dTeval)

    # Radiation Variables, see [Vessel theory: Impulse response and convolution](https://www.orcina.com/webhelp/OrcaFlex/Content/html/Vesseltheory,Impulseresponseandconvolution.htm)

    ## Number of frequency samplings
    N = len(omega_i)

    ## Radiation Force Coefficients
    Trdtn = np.pi/(omega_i[-1] - omega_i[0]) * (N - 1)
    TrdtnEval = np.arange(0, Trdtn + dT, dT)

    ## Add high damping coefficient for high frequencies if specified
    if damp_high_freq:
        B_i += np.einsum('k,ij->ijk', (omega_i/(2*np.pi*high_freq_cutoff))**2, np.max(B_i,axis=2))

    ## Calculate IRF using inverse fourier transform
    IRF = simpson(np.einsum('lkj,ij->lkij', 4*B_i, np.cos(np.outer(TrdtnEval, omega_i))), x = omega_i) / (2*np.pi)

    ## Calculate Added Mass at infinite frequency
    A_i_inf = A_i + simpson(np.einsum('lkj,ij->lkij', IRF, np.sin(np.outer(omega_i,TrdtnEval))), x = TrdtnEval) / omega_i
    A_inf_new = np.average(A_i_inf,axis=2)

    # Exciataion Variables
    WvHeadingIdx = 0
    WvHeading = beta[WvHeadingIdx]
    WvOmegaNum = 31
    WvOmega = 2*np.pi/Tp * 2**np.linspace(-1, 2, WvOmegaNum)
    Wv1Seed = 912472194
    np.random.seed(Wv1Seed)
    phase_rand = np.random.rand(WvOmegaNum)*2*np.pi

    # Pile Mass is approximated as additional mass to the pontoon    
    Mass[0,0] += pile_m[0,0]*len(pile_xs)
    Mass[1,1] += pile_m[1,1]*len(pile_xs)

    # Excitation Force Calculations
    wave_spectrum = pierson_moskowitz_spectrum(WvOmega, Hs, Tp)
    wave_height = WvHeight(WvOmega, wave_spectrum, evalTime, phase_rand)
    F_exct = exct_force(WvHeadingIdx, omega_i, WvOmega, phase_rand, wave_spectrum, Fex_i, exctnTime)

    # Preparing Time, Position, and Velocity History for convolution calculation
    t_pos_vel_history = np.zeros((int(Trdtn/dT/2),13))
    solve_ivp_dur = []
    last_step_t_idx = [0]

    def eom(t, state):
        solve_ivp_dur.append(time.time())
        t0 = time.time()
        t1 = time.time()

        # Extract position and velocity from state
        pos = state[:6]   # first 6 elements
        vel = state[6:]   # next 6 elements (velocities)
     
        # Log Time, Position, and Velocity into history if time have passed interval dT
        if last_step_t_idx[0] < t/dT and t_pos_vel_history[-1,0] < t:
            last_step_t_idx[0] += 1
            new_t_pos_vel = np.concatenate([[t], state.copy()])
            new_t_pos_vel_history = np.roll(t_pos_vel_history,-1,axis=0)
            new_t_pos_vel_history[-1] = new_t_pos_vel
            t_pos_vel_history[:] = new_t_pos_vel_history

        # Get Radiation Force
        F_rdtn = rdtn_force(t, dT, Trdtn, IRF, t_pos_vel_history[:,np.r_[0,7:13]])

        # Get Excitation Force
        ti_0 = np.floor(t/dT)
        ti_1 = np.ceil(t/dT)
        F_exct_current = (F_exct[:, int(ti_1)] - F_exct[:, int(ti_0)])*(t%dT)/dT + F_exct[:, int(ti_0)]

        # Get Pile Force
        F_pile = pile_react_force(pos, Xbody, pile_xs, pile_k)

        # Define equation of motion (Mass * acc = Forces - Hstiff * pos) to get the acceleration
        acc = np.linalg.solve(Mass + A_inf_new, F_rdtn + F_exct_current - F_pile - Hstiff @ pos)
        
        return np.concatenate([vel, acc])

    # Solve the equation of motion using scipy's solve_ivp
    sol = solve_ivp(eom, (0, Tmax), np.array([0,0,0,0,0,0,0,0,0,0,0,0]), method='RK45', t_eval = evalTime)#, rtol=1e-3, atol=1e-3)

    np.savetxt(directory + '\Pontoon_TIDHA_Out.txt', np.concatenate([[sol.t], [np.real(wave_height)], sol.y]).T)

    tend = time.time()
    print(f"Total Time : {(tend - tstart ):.6f} s")
