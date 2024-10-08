# Vessel Motion Theory
Vessel movement, like any other classical movement follows newton's second law of motion. The most basic form of the equation together with Hooke's Law and a damping coefficient $b$:

$$
m\ddot{x} + b\dot{x} + kx = f
$$

If we expand the equation for 6 degree of freedom generalized motion $\vec{x}, \vec{\dot{x}}, \vec{\ddot{x}}$ and force $\vec{f}$, we then get mass matrix, damping matrix, and stiffness matrix $\textbf{m}, \textbf{b}, \textbf{k}$ respectively.

## Added Mass and Radiation Damping Force
For the specific application of this solver, we have to modify the damping term $b\dot{x}$. The damping of the vessel motion depends on the frequency and velocity. Thus we cannot just have independent damping matrix. We have to calculate damping force by inverse fourier transform and convolve it with past velocity of the vessel. This will effectively give the correct frequency dependant damping force. See the API Reference on the hydrodynamic force for more detail.

The other thing to metion is that because of the effect of radiation force, the system will act as it have some added mass. The added mass can be calculated using the same reference as the radiation damping force.

## Restoring Force
The Hooke's law is one of the example of a restoring force. Hooke's law itsel is a linear force. In the specific condition for this solver, the stiffness matrix is provided by the hydrostatic stiffness matrix. It arise from the fact that a stable floating structure resist heave, roll, and pitch displacement. The other restoring force in this solver is pile force. A vessel anchored to piles will resist surge, sway, roll, pitch, and yaw movement. The pile force is a nonlinear force, thus cannot be represented as Hooke's law. The form it will take is a velocity dependant force. See [Linear Pile Force Thoery](linear_pile_force_theory.md) for more detailed information of the linearized pile stiffness case. Nonlinear pile reaction will be created eventually.

## Excitation Force
The right hand side of the equation of motion is the excitation force. The exciatation force excites vessel into motion. Without the excitation force, the vessel would eventually be motionless due to the damping force. In this solver, the excitation force is calulated using vessels' excitation force response that is frequency dependant. For more detailed calculation see the API Reference for the hydrodynamic forces.

## Vessel Equation of Motion
After we state every component of the motion equation, we then can assemble the equation:

$$
\begin{equation}
\left(\textbf{M} + \textbf{A}_{\infty}\right)\vec{a}(t) = -\textbf{k}_{hydrostatic} \vec{u}(t) + \vec{f}_{pile}(t) + \vec{f}_{radiation}(t) + \vec{f}_{exciatation}(t)
\end{equation}
$$

with:

 - $\vec{a}$ as the vessel acceleration

 - $\vec{u}$ as the vessel displacement