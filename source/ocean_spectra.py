from numpy.typing import NDArray
import numpy as np

def pierson_moskowitz_spectrum(omega: NDArray[np.float64],
                               Hs: float,
                               Tp: float
                               ) -> NDArray[np.float64]:
    """
    # Compute Pierson-Moskowitz spectrum S(omega)\n
    \n
    The formula adopted from [Ocen Wave Specctra by WikiWaves](https://wikiwaves.org/Ocean-Wave_Spectra).\n
    \n
    ## Input\n
    1. `omega`: Frequency sampling, (float N_omega) (rad/s)\n
    2. `Hs`: Significan wave height, (m)\n
    3. `Tp`: Peak wave period, (s)
    \n
    ## Returns\n
    spectrum: (float N_omega)
    """
    omega_p = 2 * np.pi / Tp
    alpha = 5 / 16 * Hs**2 * omega_p**4
    spectrum = alpha * omega ** (-5) * np.exp(-5 / 4 * (omega / omega_p) ** (-4))

    return spectrum

def WvHeight(omega: NDArray[np.float64],
             spectrum: NDArray[np.float64],
             evalTime: NDArray[np.float64],
             phase_rand: NDArray[np.float64]
             ) -> NDArray[np.complex128]:
    """
    # Compute wave height based on frequency sampling and summation (basically inverse fourier transform)\n
    \n
    The wave
    height calculated based on [Tabesphour (2023)](https://www.tandfonline.com/doi/full/10.1080/20464177.2023.2197280).\n
    \n
    ## Inputs\n
    1. `omega`: frequency sampling, (float N_omega) (rad/s)\n
    2. `spectrum`: spectrum to be used, (float N_omega) (m$^2$/s)\n
    3. `evalTime`: times at which the wave height is evaluated, (float N_evalTime) (s)\n
    4. `phase_rand`: random phases to get ocean spectra corresponding to each of `omega`, (float N_omega) (rad/s)\n
    \n
    ## Returns\n
    WvHeightResult: array(len(evalTime))
    """
    WvHeightResult = np.zeros(len(evalTime), dtype=np.complex128)
    d_omega = omega[1] - omega[0]
    for i, om in enumerate(omega):
        if i > 1:
            d_omega = om - omega[i-1]
        WvHeightResult += np.sqrt(2 * spectrum[i] * d_omega) * np.exp(1j * (om * evalTime + phase_rand[i]))
        
    return WvHeightResult