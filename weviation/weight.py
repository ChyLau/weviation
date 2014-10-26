"""
The three methods: Torenbeek, Raymer and General dynamics.

references:
"Synthesis of Subsonic Airplane Design", Egbert Torenbeek
"Weight estimation techniques for composite airplanes in general aviation industry", T. Paramasivam, Walter J. Horn, and James Ritter
"""

import numpy as np
import math
from __future__ import division


"""
1) torenbeek wing weight estimation w_w
"""
# k_w = 0.00125, w_g = MTOW (lb), b (ft), s (ft^2), w_w (lb)
# k_w = 0.00490, w_g = MTOW (kg), b (m), s (m^2), w_w (kg)
def w_w(k_w, w_g, b_ref, Lambda, b, n_ult, s, t_r):
    return k_w*w_g*(b_ref/math.cos(Lambda))**0.75*(1 + (b_ref*math.cos(Lambda)/b)**0.5)*n_ult**0.55*(b*s/(w_g*t_r*math.cos(Lambda)))**0.3

"""
2) torenbeek tail (empennage) weight estimation w_tail
"""

# k_wt = 0.04, w_tail (lb), s_tail (ft^2)
# k_wt = 0.64, w_tail (kg), s_tail (m^2)
def w_tail(k_wt, n_ult, s_tail):
    return k_wt*(n_ult*s_tail**2)**0.75

# k_h = 1.0 (fixed incidence stabilizers)
# k_h = 1.1 (variable incidence stabilizers)
def w_htail(k_h, s_h, f, v_d, Lambda_h):
    return k_h*s_h*f*(s_h**0.2*v_d/(math.cos(Lambda_h))**0.5)

# k_v = 1.0 (fuselage mounted horizontal tails)
# k_v = (1 + 0.15*(s_h*z_h/(s_v*b_v)))  (fin mounted horizontal tails)
def w_vtail(k_v, s_v, f, v_d, Lambda_v):
    return k_v*s_v*f*(s_v**0.2*v_d/(math.cos(Lambda_v))**0.5)

"""
3) torenbeek body (fuselage) weight estimation w_f
"""

# k_wf = 0.021 (lb), v_d (kts), s_g (ft^2)
# k_wf = 0.23 (kg), v_d (m/s), s_g (m^2)
# k_f = 1.08 (pressurized fuselage), 1.07 (main gear attached to fuselage), 1.10 (cargo airplane with cargo floor)
def w_f(k_wf, k_f, v_d, l_t, b_f, h_f, s_g):
    return k_wf*k_f*(v_d*l_t/(b_f + h_f))**0.5*s_g**1.2

"""
4) torenbeek nacelle (engine) weight estimation w_n
"""
# k_n = 2.5 (lb), k_n = 1.134 (kg)
def w_n(k_n, p_to):
    return k_n*p_to**0.5

# k_nh  = 0.32 (lb), k_nh = 0.145 (kg)
def w_nh(k_nh, p_to):
    return k_nh*p_to

# k_nr = 0.045 (lb), k_nr = 0.0204 (kg)
def w_nr(k_nr, p_to):
    return k_nr*p_to**(5/4)

# k_ntp = 0.14 (lb), k_ntp = 0.0635 (kg)
def w_ntp(k_ntp, p_to):
    return k_ntp*p_to

def w_ntj(t_to):
    return 0.055*t_to

def w_ntf(t_to):
    return 0.065*t_to

"""
5) torenbeek alighting (landing) gear weight estimation
"""
# k_uc = 1.0 (low-wing airplanes), k_uc = 1.08 (high-wing airplanes)
# multiply k_uc by 0.768 when w_sc and w_to are in kg
def w_uc(k_uc, a, b, c, d, w_to):
    return k_uc*(a + b*w_to**(3/4) + c*w_to + d*w_to**(3/2))

"""
6) surface controls weight estimation
"""
# k_sc = 0.23 (light airplanes w/o duplicated system controls)
# k_sc = 0.44 (transport airplanes and trainers, manually controlled)
# k_sc = 0.64 (transport airplanes, with powered controls and trailing-edge high-lift devices only)
def w_sc():
    return k_sc*w_to**(2/3)



