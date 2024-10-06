from numpy.typing import NDArray
import numpy as np

# Radiation Force
def rdtn_force(t: float,
               dT: float,
               Trdtn: NDArray[np.float64],
               IRF: NDArray[np.float64],
               t_vel_history: NDArray[np.float64]
               ) -> NDArray[np.float64]:
    """
    # Compute Radiation force\n
    \n
    The formula used based on [Vessel theory: Impulse response and convolution](https://www.orcina.com/webhelp/OrcaFlex/Content/html/Vesseltheory,Impulseresponseandconvolution.htm)\n
    \n
    ## Input\n
    `t`: current time, (s)\n
    `dT`: radiation time interval, (s)\n
    `Trdtn`: maximum radiation time by inverse fourier transform, (s)\n
    `IRF`: Impulse Response Function, inverse fourier transform of B, [3 x (N/m), 3 x (Nm/m)] x `Trdtn/dT`\n
    `t_vel_history`: times and velocities up to min(`t`, `Trdtn/2`), [(s), (m/s) x 3] x N_history\n
    \n
    # Returns\n
    result: array(6)
    """

    # Taking Cutoff time as half of the maximum IRF, and scale IRF by c to prevent negative
    Tc = Trdtn/2
    i_past = int(min(t, Trdtn/2)/dT)
    time = np.arange(0, Tc, dT)
    c = np.exp(-(3*time/Tc)**2)

    # Interpolated velocity history
    v = np.array([np.interp(t - time, t_vel_history[:,0], t_vel_history[:,1 + i]) for i in range(6)])[:,:i_past + 1] if len(t_vel_history) > 1 else t_vel_history[0,1:].T
    
    # Convolution
    result = -np.einsum('ijk,jk->i',c[:i_past+1]*IRF[:,:,:i_past+1],v)*dT
    
    return result

# excitation force
def exct_force(WvHeadingIdx: int,
               omega_i: NDArray[np.float64],
               omega: NDArray[np.float64],
               phase_rand: NDArray[np.float64],
               spectrum: NDArray[np.float64],
               Fex: NDArray[np.complex128],
               exctnTime: NDArray[np.complex128]) -> NDArray[np.float64]:
    """
    # Compute total excitation force at time t\n
    \n
    The excitation force doesn't consider vessel dispalcement and only considers wave height. The formula for the force 
    follows reference format from [Wamit Manual](https://www.wamit.com/manualv7.4/wamit_v74manualch3.html). The wave
    height calculated based on [Tabesphour (2023)](https://www.tandfonline.com/doi/full/10.1080/20464177.2023.2197280).\n
    \n
    ## Input\n
    `WvHeadingIdx`: Correspond to the index of wave heading of `Fex`.\n
    `omega_i`: Angular frequencies from Wamit file, (float N_omega_i) (rad/s)\n
    `omega`: Angular frequencies to be evaluated, (float N_omega) (rad/s)\n
    `phase_rand`: random phase for each corresponding `omega`, (float N_omega) (rad/s)\n
    `spectrum`: Wave spectrum, (float N_omega) (m^2 s)\n
    `Fex`: Complex hydrodynamic excitation coefficient, (float N_omega_i) (N/m)\n
    `exctnTime`: Time at which exciation time is calculated,(float N_exctnTime) (s)
    ## Returns
    Excitation force over time
    """
    # Total force as the sum of forces over all frequencies
    total_forces = np.zeros((6,len(exctnTime)), dtype=np.complex128)

    d_omega = omega[1] - omega[0]
    
    for j, total_force in enumerate(total_forces):
        for i, om in enumerate(omega):
            if i > 1:
                d_omega = om - omega[i-1]
            # Interpolated Fex on excitation omega
            Fex_intrp = np.interp(om, omega_i, Fex[j,:,WvHeadingIdx])
            
            # Time-domain excitation force contribution for frequency omega[i]
            total_forces[j] += Fex_intrp * np.sqrt(2 * spectrum[i] * d_omega) * np.exp(1j * (om * exctnTime + phase_rand[i]))

    return np.real(total_forces)  # Return the real part for the physical force