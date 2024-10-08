# Linear Pile Force Theory
**The Theoretical Background Behind Pile Force Calculation**

## Two Dimensional Single Pile
The two dimensional pile analysis is conducted using OpenPile that gives displacement result for a given force. By varying the lateral and moment force, ones can obtain inverted stiffness value, that is:

$$
\begin{align}
u_x &= \left(m_{uxfx}\right) \cdot F_x + \left(m_{uxmy}\right) \cdot M_y \\
r_y &= \left(m_{ryfx}\right) \cdot F_x + \left(m_{rymy}\right) \cdot M_y\\
\end{align}
$$

This form is useful to be used in the next step, constructing 3d individual pile stiffness matrix.

## Three Dimensional Single Pile
To continue the force calculation at the third dimension, ones only have to include the effect of lateral force x, y and moment x, y. The force z and moment z is not restrained by any individual pile. Thus following equation holds:

$$
\begin{bmatrix}
u_x\\
u_y\\
r_x\\
r_y
\end{bmatrix}
=
\begin{bmatrix}
m_{uxfx} & 0 & 0 & m_{uxmy}\\
0 & m_{uyfy} & -m_{uymx} & 0\\
0 & -m_{rxfy} & m_{rxmx} & 0\\
m_{ryfx} & 0 & 0 & m_{rymy}
\end{bmatrix}
\begin{bmatrix}
f_x\\
f_y\\
m_x\\
m_y
\end{bmatrix}
$$

or if we simplify the notation:

$$
\begin{equation}
\vec{u} = \textbf{m}\vec{f}
\end{equation}
$$

We know the expression for stiffness:

$$
\begin{equation}
\vec{f} = \textbf{k}\vec{u}
\end{equation}
$$

Thus we can get stiffness matrix by:

$$
\begin{align}
\vec{u}           &= \textbf{m}\textbf{k}\vec{u} \notag\\
\textbf{m}\textbf{k}  &= \textbf{I} \notag\\
\textbf{k}          &= \textbf{m}^{-1}
\end{align}
$$


## Multi-Pile System
After the 3D stiffness matrix is obtained, we then can proceed to calculate the total effect of the multi-pile system. There are two steps in calculating the pile force:

1. Calcualte Pile Displacement

The first step that is finding the dispalcement in each of pile reaction location is needed to get individiual pile force. The displacement is obtained through 3D rigid body transformation:

$$
\begin{equation}
\vec{u}_{pile,i} (t) = \textbf{R}_{pontoon}(t)\vec{r}_{pile,i} + \vec{u}_{pontoon}(t) - \vec{r}_{pile,i}
\end{equation}
$$

Where:

 - $\vec{r}_{pile,i}$ is undispalced pile coordinate

 - $\vec{u}_{pile,i}(t)$ is pile displacement at time $t$

 - $\vec{u}_{pontoon}(t)$ is pontoon displacement at time $t$

 - $\textbf{R}_{pontoon}(t)$ is the rotation matrix of the ponton at time $t$


2. Calculate Pile Reaction

Pile reaction is calculated based on the total of force vectors from individual pile and from the moment components. The moments arise from the nature of the force that is of non-coplanar and non-concurrent. The moment is calculated assuming center of rotation the same as the center rotation used to calculate pontoon mass and moment of inertia.

$$
\begin{align}
\vec{f}_{pile,i}(t) &= \textbf{k}\vec{u}_{pile,i}(t)\\
\vec{f}_{pile}(t) &= \sum_{i=1}^{n_{pile}} \left(\vec{f}_{pile,i}(t)  + \right(\vec{r}_{pile,i} + \vec{u}_{pile,i}(t)\left) \times \vec{f}_{pile,i}(t)\right)
\end{align}
$$


Thus with the function $\vec{f}_{pile}(t)$ as pile reaction, we finally can use it in the pontoon equation of motion.

$$
\begin{equation}
\left(\textbf{M} + \textbf{A}_{\infty}\right)\vec{a}_{pontoon}(t) = -\textbf{k}_{hydrostatic} \vec{u}_{pontoon}(t) + \vec{f}_{pile}(t) + \vec{f}_{radiation}(t) + \vec{f}_{exciatation}(t)
\end{equation}
$$