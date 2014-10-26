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


"""
1) raymer wing weight estimation w_w
"""

def w_w(w_dg, n_z, s_w, a, t, c, _lambda, Lambda, s_csw):
    return 0.0051*(w_dg*n_z)**0.557*s_w**0.649*a**0.5*(t/c)**-0.4*(1 + _lambda)**0.1*(math.cos(Lambda))**-1.0*s_csw**0.1

"""
2) raymer tail weight estimation
"""
# horizontal tail
def w_htail(k_uht, f_w, b_h, w_dg, n_z, s_ht, l_t, k_y, Lambda_ht, a_h, s_e, s_ht):
    return 0.0379*k_uht*(1 + f_w/b_h)**-0.25*w_dg**0.639*n_z**0.10*s_ht**0.75*l_t**-1.0*k_y**0.704*(math.cos(Lambda_ht))**-1.0*a_h**0.166*(1 + s_e/s_ht)**0.1

# vertical tail
def w_vtail(h_t, h_v, w_dg, n_z, l_t, s_vt, k_z, Lambda_vt, a_v, t, c):
    return 0.0026*(1 + h_t/h_v)**0.225*w_dg**0.556*n_z**0.536*l_t**-0.5*s_vt**0.5*k_z**0.875*(math.cos(Lambda_vt))**-1*a_v**0.35*(t/c)**-0.5

"""
3) raymer fuselage weight estimation
"""

def w_f(k_door, k_lg, w_dg, n_z, l, s_f, k_ws, d):
    return 0.3280*k_door*k_lg*(w_dg*n_z)**0.5*l**0.25*s_f**0.302*(1 + k_ws)**0.04*(l/d)**0.10

"""
4) raymer landing gear weight estimation
"""
# main landing gear
def w_ucm(k_mp, w_l, n_l, l_m, n_mw, n_mss, v_stall):
    return 0.0106*k_mp*w_l**0.888*n_l**0.25*l_m**0.4*n_mw**0.321*n_mss**-0.5*v_stall**0.1

# nose landing gear
def w_ucn(k_np, w_l, n_l, l_n, n_nw):
    return 0.032*k_np*w_l**0.646*n_l**0.2*l_n**0.5*n_nw**0.45

"""
5) raymer nacelle (engine) weight estimation
"""

def w_n(k_ng, n_lt, n_w, n_z, w_ec, n_en, s_n):
    return 0.6724*k_ng*n_lt**0.10*n_w**0.294*n_z**0.119*w_ec**0.611*n_en**0.984*s_n**0.224

"""
6) raymer engine controls weight estimation
"""

def w_enc(n_en, l_ec):
    return 5.0*n_en + 0.80*l_ec

"""
7) raymer started (pneumatic) weight estimation
"""

def w_s(n_en, w_en):
    return 49.19*(n_en*w_en/1000)**0.541

"""
8) raymer fuel system weight estimation
"""

def w_fs(v_t, v_i, v_p, n_t):
    return 2.405*v_t**0.606*(1 + v_i/v_t)**-1.0*(1 + v_p/v_t)*n_t**0.5

"""
9) raymer flight controls weight estimation
"""

def w_fc(n_f, n_m, s_cs, i_y):
    return 145.9*n_f**0.554*(1 + n_m/n_f)**-1.0*s_cs**0.20*(i_y*1e-6)**0.07

"""
10) raymer APU installed weight estimation
"""

def w_apui(w_apuu):
    return 2.2*w_apuu

"""
11) raymer instruments weight estimation
"""

def w_instr(k_r, k_tp, n_c, n_en, l_f, b_w):
    return 4.509*k_r*k_tp*n_c**0.541*n_en*(l_f + b_w)**0.5

"""
12) raymer hydraulics weight estimation
"""

def w_hydr(n_f, l_f, b_w):
    return 0.2673*n_f*(l_f + b_w)**0.937

"""
13) raymer electrical weight estimation
"""

def w_el(r_kva, l_a, n_gen):
    return 7.291*r_kva**0.782*l_a**0.346*n_gen**0.10

"""
14) raymer avionics weight estimation
"""

def w_av(w_uav):
    return 1.73*w_uav**0.983

"""
15) raymer furnishings weight estimation
"""

def w_furn(n_c, w_c, s_f):
    return 0.0577*n_c**0.1*w_c**0.393*s_f**0.75

"""
16) raymer air conditioning weight estimation
"""

def w_ac(n_p, v_pr, w_uav):
    return 62.36*n_p**0.25*(v_pr/1000)**0.604*w_uav**0.10

"""
17) raymer anti-ice weight estimation
"""

def w_ai(w_dg):
    return 0.002*w_dg

"""
18) raymer handling gear weight estimation
"""

def w_hand(w_dg):
    return 3.0e-4*w_dg

"""
19) raymer military cargo handling system
"""
#s_cf (cargo floot area, ft^2)
def w_mil(s_cf):
    2.4*s_cf


