"""
The three methods: Torenbeek, Raymer and General dynamics.

references:
"Synthesis of Subsonic Airplane Design", Egbert Torenbeek
"Weight estimation techniques for composite airplanes in general aviation industry", T. Paramasivam, Walter J. Horn, and James Ritter
"""

import numpy as np
import math
from __future__ import division

class Torenbeek:

"""
TORENBEEK STRUCTURES GROUP
"""
## 1) torenbeek wing weight estimation w_w
# k_w = 0.00125, w_g = MTOW (lb), b (ft), s (ft^2), w_w (lb)
# k_w = 0.00490, w_g = MTOW (kg), b (m), s (m^2), w_w (kg)
    def w_w(self, w_g, b_ref, Lambda, b, n_ult, s, t_r, unit):
        if unit == 'im':
            k_w = 0.00125
        elif unit == 'si':
            k_w = 0.00490
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_w*w_g*(b_ref/math.cos(Lambda))**0.75*(1 + (b_ref*math.cos(Lambda)/b)**0.5)*n_ult**0.55*(b*s/(w_g*t_r*math.cos(Lambda)))**0.3

## 2) torenbeek tail (empennage) weight estimation w_tail
# k_wt = 0.04, w_tail (lb), s_tail (ft^2)
# k_wt = 0.64, w_tail (kg), s_tail (m^2)
    def w_tail(self, n_ult, s_tail, unit):
        if unit == 'im':
            k_wt = 0.04
        elif unit == 'si':
            k_wt = 0.64
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_wt*(n_ult*s_tail**2)**0.75

# k_h = 1.0 (fixed incidence stabilizers)
# k_h = 1.1 (variable incidence stabilizers)
    def w_htail(self, s_h, f, v_d, Lambda_h, stabilizers):
        if stabilizers == 'fixed':
            k_h = 1.0
        elif stabilizers == 'variable':
            k_h = 1.1
        else:
            print "USAGE: 'stabilizers' is 'fixed' or 'variable'."

        return k_h*s_h*f*(s_h**0.2*v_d/(math.cos(Lambda_h))**0.5)

# k_v = 1.0 (fuselage mounted horizontal tails)
# k_v = (1 + 0.15*(s_h*z_h/(s_v*b_v)))  (fin mounted horizontal tails)
    def w_vtail(self, s_v, f, v_d, Lambda_v, mounted, s_h=None, z_h=None, b_v=None):
        if mounted == 'fuselage':
            k_v = 1.0
        elif mounted == 'fin':
            k_v = 1 + 0.15*(s_h*z_h/(s_v*b_v))
        else:
            print "USAGE: 'mounted' is 'fuselage' or 'fin'."

        return k_v*s_v*f*(s_v**0.2*v_d/(math.cos(Lambda_v))**0.5)

## 3) torenbeek body (fuselage) weight estimation w_f
# k_wf = 0.021 (lb), v_d (kts), s_g (ft^2)
# k_wf = 0.23 (kg), v_d (m/s), s_g (m^2)
# k_f = 1.08 (pressurized fuselage), 1.07 (main gear attached to fuselage), 1.10 (cargo airplane with cargo floor)
    def w_f(self, v_d, l_t, b_f, h_f, s_g, unit, f_type):
        if unit == 'im':
            k_wf = 0.021
        elif unit == 'si':
            k_wf = 0.23
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        if f_type == 'presssurized':
            k_f = 1.08
        elif f_type == 'main':
            k_f = 1.07
        elif f_type = 'cargo'
            k_f = 1.10
        else:
            print "USAGE: 'f_type' is 'pressurized' or 'main' or 'cargo'."

        return k_wf*k_f*(v_d*l_t/(b_f + h_f))**0.5*s_g**1.2

## 4) torenbeek nacelle (engine) weight estimation w_n
# k_n = 2.5 (lb), k_n = 1.134 (kg)
    def w_n(self, p_to, unit):
        if unit == 'im':
            k_n = 2.5
        elif unit == 'si':
            k_n = 1.134
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_n*p_to**0.5

# k_nh  = 0.32 (lb), k_nh = 0.145 (kg)
    def w_nh(self, p_to, unit):
        if unit == 'im':
            k_nh = 0.32
        elif unit == 'si':
            k_nh = 0.145
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_nh*p_to

# k_nr = 0.045 (lb), k_nr = 0.0204 (kg)
    def w_nr(self, p_to, unit):
        if unit == 'im':
            k_nr = 0.045
        elif unit == 'si':
            k_nr = 0.0204
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_nr*p_to**(5/4)

# k_ntp = 0.14 (lb), k_ntp = 0.0635 (kg)
    def w_ntp(self, p_to, unit):
        if unit == 'im':
            k_ntp = 0.14
        elif unit == 'si':
            k_ntp = 0.0635
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_ntp*p_to

    def w_ntj(self, t_to):
        return 0.055*t_to

    def w_ntf(self, t_to):
        return 0.065*t_to

## 5) torenbeek alighting (landing) gear weight estimation
# k_uc = 1.0 (low-wing airplanes), k_uc = 1.08 (high-wing airplanes)
# multiply k_uc by 0.768 when w_sc and w_to are in kg
    def w_uc(self, a, b, c, d, w_to, unit, uc_type):
        if unit == 'im':
            k_multi = 1.0
        elif unit == 'si':
            k_multi = 0.768
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        if uc_type == 'low':
            k_uc = 1.0
        elif uc_type == 'high':
            k_uc = 1.08
        else:
            print "USAGE: 'uc_type' is 'low' or 'high'."

        return k_multi*k_uc*(a + b*w_to**(3/4) + c*w_to + d*w_to**(3/2))

## 6) surface controls weight estimation
# k_sc = 0.23 (light airplanes w/o duplicated system controls)
# k_sc = 0.44 (transport airplanes and trainers, manually controlled)
# k_sc = 0.64 (transport airplanes, with powered controls and trailing-edge high-lift devices only)
    def w_sc(self, w_to, unit, control):
        if unit == 'im':
            k_multi = 1.0
        elif unit == 'si':
            k_multi = 0.768
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        if control == 'light':
            k_sc = 0.23
        elif control == 'transport'
            k_sc = 0.44
        elif control == 'transportplus'
            k_sc = 0.64
        else:
            print "USAGE: 'control' is 'light' or 'transport' or 'transportplus'."

        return k_multi*k_sc*w_to**(2/3)

"""
TORENBEEK PROPULSION GROUP: SIMPLE APPROX
"""
## 7) torenbeek propulsion group weight estimation
# k_pg = 1.16 (single tractor propeller in fuselage)
# k_pg = 1.35 (multi-engine propeller airplanes)
# k_pg = 1.15 (jet transports, podded engines)
# k_pg = 1.40 (light jet airplanes, buried engines)

# propeller aircraft -- w_pg (lb), k_pgc = 0.24 (lb), k_pgc = 0.109 (kg)
    def w_pg(self, n_e, w_e, p_to, unit, engine):
        if unit == 'im':
            k_pgc = 0.24
        elif unit == 'si':
            k_pgc = 0.109
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        if engine == 'single':
            k_pg = 1.16
        elif engine == 'multi':
            k_pg = 1.35

        else:
            print "USAGE: 'engine' is 'single' or 'multi'."

        return k_pg*n_e*(w_e + k_pgc*p_to)

# jet aircraft -- k_thr = 1.00 (no thrust reversers), k_thr = 1.18 (thrust reversers installed)
    def w_pgj(self, n_e, w_e, reversers, engine):
        if engine == 'jet':
            k_pg = 1.15
        elif engine = 'light':
            k_pg = 1.40
        else:
            print "USAGE: 'engine' is 'jet' or 'light'."

        if reversers == 'no':
            k_thr = 1.00
        elif reversers == 'yes':
            k_thr = 1.18
        else:
            print "USAGE: 'reversers' is 'yes' or 'no'."

        return k_pg*k_thr*n_e*w_e

"""
TORENBEEK PROPULSION GROUP: DETAILED
"""
## 8) torenbeek engine installed
    def w_eni(self, n_e, w_e):
        return n_e*w_e

## 9) torenbeek accessory gear boxes and drive
# turbojet/turbofan -- k_acc = 0.03 (lb), k_acc = 0.0343 (kg)
    def w_acc(self, n_e, w_fto, unit):
        if unit == 'im':
            k_acc = 0.03
        elif unit == 'si':
            k_acc = 0.0343
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_acc*n_e*(w_fto)**1.168

# turboprop -- k_accp = 0.4 (lb), k_accp = 0.181 (kg)
    def w_accp(self, n_e, p_to, unit):
        if unit == 'im':
            k_accp = 0.4
        elif unit == 'si':
            k_accp = 0.181
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_accp*n_e*p_to**0.8

## 10) torenbeek air induction system
# turbojet/turbofan -- k_airi = 11.45 (lb), k_airi = 29.62 (kg), k_geo = 1.0 (round or one flat side), k_geo = 1.33 (two or more flat sides)
    def w_airi(self, l_d, n_i, a_i, unit, side):
        if unit == 'im':
            k_airi = 11.45
        elif unit == 'si':
            k_airi = 29.62
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        if side == 'single':
            k_geo = 1.0
        elif side == 'multi':
            k_geo = 1.33
        else:
            print "USAGE: 'side' is 'single' or 'multi'."

        return k_airi*(l_d*n_i*a_i**0.5*k_geo)**0.7331

## 11) torenbeek exhaust system
# tailpipes -- k_ext = 3 (lb), a (ft^2), k_ext = 14.63 (kg), a (m^2)
    def w_ext(self, a, unit):
        if unit == 'im':
            k_ext = 3
        elif unit == 'si':
            k_ext = 14.63
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_ext*a

# silencers
    def w_exs(self, n_e, t_to):
        return 0.01*n_e*t_to

## 12) if reciprocating: skip 8 - 11
# k_rec = 1.03 (lb), k_rec = 0.467 (kg)
    def w_rec(self, n_e, p_to, unit):
        if unit == 'im':
            k_rec = 1.03
        elif unit == 'si':
            k_rec = 0.467
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_rec*n_e*p_to**0.7

## 13) torenbeek superchargers: reciprocating only
# k_super = 0.455 (lb), k_super = 0.435 (kg)
    def w_super(self, n_e, w_e, unit):
        if unit == 'im':
            k_super = 0.455
        elif unit == 'si':
            k_super = 0.435
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_super*(n_e*w_e)**0.943

## 14) torenbeek oil system and cooler
# turbojet/turbofan -- k_oc = 0.01 to 0.03)
    def w_oc(self, n_e, w_e):
        k_oc = 0.02 # 0.01 to 0.03

        return k_oc*n_e*w_e

# turboprop
    def w_ocp(self, n_e, w_e):
        return 0.07*n_e*w_e

# reciprocating -- radial
    def w_ocrecr(self, n_e, w_e):
        return 0.08*n_e*w_e

# reciprocating -- horizontal opposed
    def w_ocrech(self, n_e, w_e):
        return 0.03*n_e*w_e

## 15) torenbeek fuel system
# turbojet/turbofan/turboprop -- integral tanks
# k_fs = 80 (lb), k_fs = 36.3 (kg)
# k_fss = 15 (lb), k_fss = 4.366 (kg)
    def w_fsi(self, n_e, n_ft, n_ft, v_ft, unit):
        if unit == 'im':
            k_fs = 80
            k_fss = 15
        elif unit == 'si':
            k_fs = 36.3
            k_fss = 4.366
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_fs*(n_e + n_ft - 1) + k_fss*n_ft**0.5*v_ft**0.333

# turbojet/turbofan/turboprop -- bladder tanks
# k_fsb = 3.2 (lb), k_fsb = 0.551 (kg)
    def w_fsb(self, v_ft, unit):
        if unit == 'im':
            k_fsb = 3.2
        elif unit == 'si':
            k_fsb = 0.551
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_fsb*v_ft**0.727

# reciprocating --  single engine
# k_fsrs = 2 (lb), k_fsrs = 0.3735 (kg)
    def w_fsrs(self, v_ft, unit):
        if unit == 'im':
            k_fsrs = 2
        elif unit == 'si':
            k_fsrs = 0.3735
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_fsrs*v_ft**0.667

# reciprocating --  multi engine
# k_fsrm = 4.5 (lb), k_fsrm = 0.9184 (kg)
    def w_fsrm(self, v_ft, unit):
        if unit == 'im':
            k_fsrm = 4.5
        elif unit == 'si':
            k_fsrm = 0.9184
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_fsrm*v_ft**0.60

## 16) torenbeek water injection system
# k_wis = 8.586 (lb), k_wis = 1.561 (kg)
    def w_wis(self, v_wt, unit):
        if unit == 'im':
            k_wis = 8.586
        elif unit == 'si':
            k_wis = 1.561
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_wis*v_wt**0.687

## 17) torenbeek propeller installation
# turboprop -- k_p = 0.108 (lb), k_p = 0.124 (kg) or k_p = 0.144 (lb), k_p = 0.165 (kg)
    def w_pi(self, n_p, b, d_p, p_to, unit):
        if unit == 'im':
            k_p = 0.108 # or 0.144
        elif unit == 'si':
            k_p = 0.124 # or 0.165
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_p*n_p*b*(d_p*p_to)**0.78174

## 18) torenbeek thrust reversers
# turbojet/turbofan
    def w_tr(self, n_e, w_e):
        return 0.18*n_e*w_e

"""
TORENBEEK EQUIPMENT GROUP
"""
## 19) torenbeek APU
# k_apu = 16 (lb), k_apu = 11.7 (kg)
    def w_apu(self, w_ba, unit):
        if unit == 'im':
            k_apu = 16
        elif unit == 'si':
            k_apu = 11.7
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_apu*w_ba**(3/5)

## 20) torenbeek instruments and NAV/COM
# propeller-powered utility airplanes -- k_navp = 40 (lb), k_navp = 18.1 (kg)
    def w_navp(self, w_to, unit):
        if unit == 'im':
            k_navp = 40
        elif unit == 'si':
            k_navp = 18.1
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_navp + 0.008*w_to

# low-subsonic transports -- k_navt = 120 (lb), k_navtt = 20 (lb), k_navt = 54.4 (kg), k_navtt = 9.1 (kg)
    def w_navt(self, n_e, w_to, unit):
        if unit == 'im':
            k_navt = 120
            k_navtt = 20
        elif unit == 'si':
            k_navt = 54.4
            k_navtt = 9.1
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_navt + k_navtt*n_e + 0.006*w_to

# high-subsonic jet transports -- k_ieg = 0.575 (lb), k_ieg = 0.347 (kg)
    def w_ieg(self, w_de, r_d, unit):
        if unit == 'im':
            k_ieg = 0.575
        elif unit == 'si':
            k_ieg = 0.347
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_ieg*w_de**(5/9)*r_d**(1/4)

## 21) torenbeek hydraulic, pneumatic, electrical
# DC electrical weight -- k_eldc = 400 (lb), k_eldc = 181 (kg)
    def w_eldc(self, w_to, unit):
        if unit == 'im':
            k_eldc = 400
        elif unit == 'si':
            k_eldc = 181
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return 0.02*w_to + k_eldc

# AC electrical weight -- k_elac = (lb), k_elac = (kg)
    def w_elac(self, p_el, unit):
        if unit == 'im':
            k_elac = 0
        elif unit == 'si':
            k_elac = 0
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_elac*p_el*(1 - 0.033*p_el**0.5)


class Raymer:
"""
RAYMER STRUCTURES GROUP
"""
## 1) raymer wing weight estimation w_w
    def w_w(w_dg, n_z, s_w, a, t, c, _lambda, Lambda, s_csw):
        return 0.0051*(w_dg*n_z)**0.557*s_w**0.649*a**0.5*(t/c)**-0.4*(1 + _lambda)**0.1*(math.cos(Lambda))**-1.0*s_csw**0.1

## 2) raymer tail weight estimation
# horizontal tail
    def w_htail(k_uht, f_w, b_h, w_dg, n_z, s_ht, l_t, k_y, Lambda_ht, a_h, s_e, s_ht):
        return 0.0379*k_uht*(1 + f_w/b_h)**-0.25*w_dg**0.639*n_z**0.10*s_ht**0.75*l_t**-1.0*k_y**0.704*(math.cos(Lambda_ht))**-1.0*a_h**0.166*(1 + s_e/s_ht)**0.1

# vertical tail
    def w_vtail(h_t, h_v, w_dg, n_z, l_t, s_vt, k_z, Lambda_vt, a_v, t, c):
        return 0.0026*(1 + h_t/h_v)**0.225*w_dg**0.556*n_z**0.536*l_t**-0.5*s_vt**0.5*k_z**0.875*(math.cos(Lambda_vt))**-1*a_v**0.35*(t/c)**-0.5

## 3) raymer fuselage weight estimation
    def w_f(k_door, k_lg, w_dg, n_z, l, s_f, k_ws, d):
        return 0.3280*k_door*k_lg*(w_dg*n_z)**0.5*l**0.25*s_f**0.302*(1 + k_ws)**0.04*(l/d)**0.10

## 4) raymer landing gear weight estimation
# main landing gear
    def w_ucm(k_mp, w_l, n_l, l_m, n_mw, n_mss, v_stall):
        return 0.0106*k_mp*w_l**0.888*n_l**0.25*l_m**0.4*n_mw**0.321*n_mss**-0.5*v_stall**0.1

# nose landing gear
    def w_ucn(k_np, w_l, n_l, l_n, n_nw):
        return 0.032*k_np*w_l**0.646*n_l**0.2*l_n**0.5*n_nw**0.45

## 5) raymer nacelle (engine) weight estimation
    def w_n(k_ng, n_lt, n_w, n_z, w_ec, n_en, s_n):
        return 0.6724*k_ng*n_lt**0.10*n_w**0.294*n_z**0.119*w_ec**0.611*n_en**0.984*s_n**0.224

"""
RAYMER PROPULSION GROUP
"""
## 6) raymer engine controls weight estimation
    def w_enc(n_en, l_ec):
        return 5.0*n_en + 0.80*l_ec

## 7) raymer started (pneumatic) weight estimation
    def w_s(n_en, w_en):
        return 49.19*(n_en*w_en/1000)**0.541

## 8) raymer fuel system weight estimation
    def w_fs(v_t, v_i, v_p, n_t):
        return 2.405*v_t**0.606*(1 + v_i/v_t)**-1.0*(1 + v_p/v_t)*n_t**0.5


"""
RAYMER EQUIPMENT GROUP
"""
## 9) raymer flight controls weight estimation
    def w_fc(n_f, n_m, s_cs, i_y):
        return 145.9*n_f**0.554*(1 + n_m/n_f)**-1.0*s_cs**0.20*(i_y*1e-6)**0.07

## 10) raymer APU installed weight estimation
    def w_apui(w_apuu):
        return 2.2*w_apuu

## 11) raymer instruments weight estimation
    def w_instr(k_r, k_tp, n_c, n_en, l_f, b_w):
        return 4.509*k_r*k_tp*n_c**0.541*n_en*(l_f + b_w)**0.5

## 12) raymer hydraulics weight estimation
    def w_hydr(n_f, l_f, b_w):
        return 0.2673*n_f*(l_f + b_w)**0.937

## 13) raymer electrical weight estimation
    def w_el(r_kva, l_a, n_gen):
        return 7.291*r_kva**0.782*l_a**0.346*n_gen**0.10

## 14) raymer avionics weight estimation
    def w_av(w_uav):
        return 1.73*w_uav**0.983

## 15) raymer furnishings weight estimation
    def w_furn(n_c, w_c, s_f):
        return 0.0577*n_c**0.1*w_c**0.393*s_f**0.75

## 16) raymer air conditioning weight estimation
    def w_ac(n_p, v_pr, w_uav):
        return 62.36*n_p**0.25*(v_pr/1000)**0.604*w_uav**0.10

## 17) raymer anti-ice weight estimation
    def w_ai(w_dg):
        return 0.002*w_dg

## 18) raymer handling gear weight estimation
    def w_hand(w_dg):
        return 3.0e-4*w_dg

## 19) raymer military cargo handling system
#s_cf (cargo floot area, ft^2)
    def w_mil(s_cf):
        return 2.4*s_cf
