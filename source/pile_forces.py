from numpy.typing import NDArray
import numpy as np

def get_pile_disp(x_t: NDArray[np.float64], r: NDArray[np.float64]) -> NDArray[np.float64]:
    '''
    # Get the rigid body point displacement of pile's support location\n
    \n
    Displacement of point on rigid body, calculated using basic geometry.\n
    \n
    ## Input
    1. `x_t`: rigid body 6-dof generalized position at time t, [3 x (m), 3 x (rad)] \n
    2. `r`: vector from rigid body center of rotation to the point, (float 2) m\n
    \n
    ## Return\n
    Return the coordinate of the displaced point\n
    '''
    u = np.zeros(6)
    u[0] += x_t[0] -(1 - np.cos(x_t[4]))*r[0] -x_t[5]*r[1]
    u[1] += x_t[1] -(1 - np.cos(x_t[3]))*r[1] +x_t[5]*r[0]
    u[2] += x_t[2] +np.sin(x_t[4])*r[0] +np.sin(x_t[3])*r[1]
    u[3] += x_t[3]
    u[4] += x_t[4]
    u[5] += x_t[5]

    return u

def pile_react_force(x_t: NDArray[np.float64], Xbody: NDArray[np.float64], pile_xs: NDArray[np.float64], pile_k: NDArray[np.float64]) -> NDArray[np.float64]:
    '''
    # Get the total pile reaction\n
    \n
    Pile force is calculated from assumed linear properties of the pile and pile displacements. The total body force includes non-coplanar
    forces that cause moment the the rigid body.s\n
    \n
    ## Input\n
    1. `x_t`: rigid body 6-dof generalized position at time t, [3 x (m), 3 x (rad)]\n
    2. `Xbody`: rigid body center of rotation, (float 3) (m)\n
    3. `pile_xs`: pile locations array(x, y), [x y] x N_pile (m)\n
    4. `pile_k`: linearized pile stiffness matrix, (float 4 x 4)\n
    \n
    ## Return\n
    Return the total pile reaction in term of 6-dof generalized force\n
    '''
    reaction = np.zeros(6)
    for pile_x in pile_xs:
        r = pile_x - Xbody[:2]
        u = get_pile_disp(x_t, r)

        F_pile = pile_k@u[[0,1,3,4]]
        reaction[[0,1,3,4]] += F_pile # Pile Force
        reaction[3:] += np.cross(np.concatenate([r,[0]]) + u[:3], np.concatenate([F_pile[:2], [0]])) # Rigid Body Moment Force
    
    return reaction