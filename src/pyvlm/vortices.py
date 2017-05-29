import numpy as np

from .geometry import (cross_prod, vect_dot, norm_dir_vect,
                       vect_perpendicular, dist_point2line)


def vortex_position_in_panel(P1, P2, P3, P4):
    """
    For a given panel defined by points P1, P2, P3 and P4
    returns the position of the horseshoe vortex defined
    by points A, B, C and D and its control point P.

            ^
          y |                Points defining the panel are
            |                named clockwise.
     P3--C--|--D--P4         Points defining the horseshoe
      |  |  |  |  |          are named clockwise as well.
      |  |  |  |  |
      |  |  +--P--|---->
      |  |     |  |     x
      |  |     |  |
     P2--B-----A--P1

    Parameters
    ----------
    P1, P2, P3, P4 : array_like
                     Points that define the panel

    Returns
    -------
    results : dict
        P - control point where the boundary condition V*n = 0
            is applied according to the Vortice Lattice Method.
        A, B, C, D - points that define the horseshoe position
    """

    P1P2 = P2 - P1
    P3P4 = P4 - P3
    P1P4 = P4 - P1

    A = P1 + P1P2 / 4
    B = A + P1P2 / 2
    C = P3 + P3P4 / 4
    D = C + P3P4 / 2

    AD = D - A
    P = A + AD / 2

    results = [P, A, B, C, D]

    return results


def v_induced_by_horseshoe_vortex(P, A, B, C, D, gamma=1):
    """
    Induced velocity at point P due to a horseshoe vortex
    spatially positioned by points A, B, C and D, extended
    to x_Inf(+) in a 2D euclidean space. Circulation
    direction: x_Inf(+) -> A -> B -> C -> D -> x_Inf(+)

                ^
              y |                Points defining the horseshoe
    V_inf       | i_3            are named clockwise.
    ->     C----|->--D  ...>...  A direction vector is
    ->     |    |    |           calculated for each vortex.
    -> i_2 ^    +----|------>
    ->	   |         |       x
    ->	   B----<----A  ...<...
                i_1

    Parameters
    ----------
    P, A, B, C, D : array_like
                    P - point of reference
                    A, B, C, D - points of the horseshoe vortex
    gamma : circulation

    Returns
    -------
    v : float
    """

    pi = np.pi
    epsilon = 1e-3

    i_1 = np.array([-1, 0])  # trailing vortex(1) dir. vector
    i_2 = norm_dir_vect(B, C)  # bound vortex(2) dir. vector
    i_3 = np.array([1, 0])  # trailing vortex(3) dir. vector

    # First trailing vortex segment x_Inf(+) -> A -> B
    i_PB = norm_dir_vect(P, B)  # PB direction vector
    h_1 = dist_point2line(P, A, B)  # distance to 1st tr. vortex
    if h_1 < epsilon:
        v_1 = 0
    else:
        sign_1 = np.sign(cross_prod(i_PB, i_1))
        cos_2 = vect_dot(-i_PB, i_1)
        v_1 = sign_1 * (gamma/(4 * pi * h_1)) * (1 - cos_2)

    # Bound vortex segment B -> C
    i_PC = norm_dir_vect(P, C)  # PC direction vector
    h_2 = dist_point2line(P, B, C)  # distance to bound vortex
    if h_2 < epsilon:
        v_2 = 0
    else:
        sign_2 = np.sign(cross_prod(i_PC, i_2))
        cos_1 = vect_dot(-i_PB, i_2)
        cos_2 = vect_dot(-i_PC, i_2)
        v_2 = sign_2 * (gamma/(4 * pi * h_2)) * (cos_1 - cos_2)

    # Second trailing vortex segment C -> D -> x_Inf(+)
    h_3 = dist_point2line(P, C, D)  # distance to 2nd tr. vortex
    if h_3 < epsilon:
        v_3 = 0
    else:
        sign_3 = np.sign(cross_prod(i_PC, i_3))
        cos_1 = vect_dot(-i_PC, i_3)
        v_3 = sign_3 * (gamma/(4 * pi * h_3)) * (cos_1 + 1)

    v1 = v_1 + v_2 + v_3  # Total induced velocity in P
    v2 = v_1 + v_3  # Induced velocity in P due to trailing vortices

    return v1, v2


def v_induced_by_finite_vortex_line(P, A, B, gamma=1):
    """

    Y^						Induced velocity at point P due
     |	  + P(x,y)			to a finite straight line vortex
     |						defined by points A and B.
     +=======+--------> X	Circulation from A --> B.
     A		 B

    Parameters
    ----------
    P, A, B : array_like
              P - point of reference
              A, B - points of the vortex
    gamma : circulation

    Returns
    -------
    v : float
    """

    i = norm_dir_vect(A, B)  # vortex_2 direction vector

    i_PA = norm_dir_vect(P, A)  # PB direction vector
    i_PB = norm_dir_vect(P, B)  # PC direction vector

    h = dist_point2line(P, A, B)  # distance to vortex_2
    sign = np.sign(cross_prod(i_PA, i))

    cos_1 = vect_dot(-i_PA, i)
    cos_2 = vect_dot(-i_PB, i)
    v = sign * (gamma/(4 * pi * h)) * (cos_1 - cos_2)

    return v
