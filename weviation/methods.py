"""
Author: Chy Lau
Created: 2014-2015
Description:
The three methods -- Torenbeek, Raymer and General dynamics.

References:
"Synthesis of Subsonic Airplane Design", Egbert Torenbeek
"Weight estimation techniques for composite airplanes in general aviation industry", T. Paramasivam, Walter J. Horn, and James Ritter
"""

from __future__ import division
import numpy as np
from math import *

class Torenbeek:

    """
    TORENBEEK STRUCTURES GROUP
    """
## 1) torenbeek wing weight estimation w_w
# k_w = 0.00125, w_g = MTOW (lb), b (ft), s (ft^2), w_w (lb)
# k_w = 0.00490, w_g = MTOW (kg), b (m), s (m^2), w_w (kg)
    def w_w(self, w_g, b_ref, Lambda, b, n_ult, s, t_r, unit):
        if unit == 'im':
            k_w = 0.0017
        elif unit == 'si':
            k_w = 0.00667
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_w*w_g*(b_ref/cos(radians(Lambda)))**0.75*(1 + (b_ref*cos(radians(Lambda))/b)**0.5)*n_ult**0.55*(b*s/(w_g*t_r*cos(radians(Lambda))))**0.3

## 2) torenbeek tail (empennage) weight estimation w_tail
# k_h = 1.0 (fixed incidence stabilizers)
# k_h = 1.1 (variable incidence stabilizers)
    def w_htail(self, s_h, v_d, Lambda_h, stabilizers):
        if stabilizers == 'fixed':
            k_h = 1.0
        elif stabilizers == 'variable':
            k_h = 1.1
        else:
            print "USAGE: 'stabilizers' is 'fixed' or 'variable'."

        return k_h*s_h*(3.81*(s_h**0.2*v_d)/(1000*cos(radians(Lambda_h))**0.5) - 0.287)

# k_v = 1.0 (fuselage mounted horizontal tails)
# k_v = (1 + 0.15*(s_h*z_h/(s_v*b_v)))  (fin mounted horizontal tails)
    def w_vtail(self, s_v, v_d, Lambda_v, mounted, s_h=None, z_h=None, b_v=None):
        if mounted == 'fuselage':
            k_v = 1.0
        elif mounted == 'fin':
            k_v = 1 + 0.15*(s_h*z_h/(s_v*b_v))
        else:
            print "USAGE: 'mounted' is 'fuselage' or 'fin'."

        return k_v*s_v*(3.81*(s_v**0.2*v_d)/(1000*cos(radians(Lambda_v))**0.5) - 0.287)

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

        if f_type == 'pressurized':
            k_f = 1.08
        elif f_type == 'main':
            k_f = 1.07
        elif f_type == 'cargo':
            k_f = 1.10
        elif f_type == 'rear':
            k_f = 1.04
        else:
            print "USAGE: 'f_type' is 'pressurized' or 'main' or 'cargo' or 'rear'."

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
        elif control == 'transport':
            k_sc = 0.44
        elif control == 'transportplus':
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
        elif engine == 'light':
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
    def w_ext(self, ax, unit):
        if unit == 'im':
            k_ext = 3
        elif unit == 'si':
            k_ext = 14.63
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_ext*ax

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
    def w_fsi(self, n_e, n_ft, v_ft, unit):
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
    def w_pi(self, n_p, b_p, d_p, p_to, unit):
        if unit == 'im':
            k_p = 0.108 # or 0.144
        elif unit == 'si':
            k_p = 0.124 # or 0.165
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_p*n_p*b_p*(d_p*p_to)**0.78174

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
# hydraulic and electrical
    def w_heu(self, w_e, unit, dtype):
        if unit == 'im':
            if dtype == 'utility':
                k_heu = 0.00780
                e_heu = 6/5
            elif dtype == 'jet':
                k_heu = 0.064
                e_heu = 1
            elif dtype == 'propeller':
                k_heu = 0.325
                e_heu = 4/5
            else:
                print "USAGE: 'dtype' is 'utility' or 'jet' or 'propeller'."
        elif unit == 'si':
            if dtype == 'utility':
                k_heu = 0.00914
                e_heu = 6/5
            elif dtype == 'jet':
                k_heu = 0.064
                e_heu = 1
            elif dtype == 'propeller':
                k_heu = 0.277
                e_heu = 4/5
            else:
                print "USAGE: 'dtype' is 'utility' or 'jet' or 'propeller'."
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_heu*w_e**e_heu

# hydraulic and pneumatic for jet
    def w_hp(self, w_de, unit, control):
        if unit == 'im':
            if control == 'no':
                k_hp1 = 0.004
                k_hp2 = 100
            elif control == 'boosted':
                k_hp1 = 0.007
                k_hp2 = 200
            elif control == 'duplicated':
                k_hp1 = 0.011
                k_hp2 = 400
            elif control == 'triplex':
                k_hp1 = 0.015
                k_hp2 = 600
            else:
                print "USAGE: 'control' is 'no' or 'boosted' or 'duplicated' or 'triplex'."
        elif unit == 'si':
            if control == 'no':
                k_hp1 = 0.004
                k_hp2 = 45
            elif control == 'boosted':
                k_hp1 = 0.007
                k_hp2 = 91
            elif control == 'duplicated':
                k_hp1 = 0.011
                k_hp2 = 181
            elif control == 'triplex':
                k_hp1 = 0.015
                k_hp2 = 272
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_hp1*w_de + k_hp2

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
            k_elac = 36
        elif unit == 'si':
            k_elac = 16.3
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_elac*p_el*(1 - 0.033*p_el**0.5)

## 22) torenbeek air-conditioning, pressurization, ant-ice
    def w_api(self, l_pax, unit):
        if unit == 'im':
            k_api = 6.75
        elif unit == 'si':
            k_api = 14.0
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_api*l_pax**1.28

## 23) torenbeek oxygen system
    def w_ox(self, n_pax, flight):
        if flight == 'below':
            k_ox1 = 20
            k_ox2 = 0.5
        elif flight == 'above':
            k_ox1 = 30
            k_ox2 = 1.2
        elif flight == 'overwater':
            k_ox1 = 40
            k_ox2 = 2.4
        else:
            print "USAGE: 'flight' is 'below' or 'above' or 'overwater'."

        return k_ox1 + k_ox2*n_pax

## 24) torenbeek furnishing
    def w_fur(self, w_zf, unit):
        if unit == 'im':
            k_zf = 0.211
        elif unit == 'si':
            k_zf = 0.196
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_zf*w_zf**0.91


class Raymer:
    """
    RAYMER STRUCTURES GROUP
    """
## 1) raymer wing weight estimation w_w
    def w_w(self, w_dg, n_z, s_w, a, t_c, _lambda, Lambda, s_csw):
        return 0.0051*(w_dg*n_z)**0.557*s_w**0.649*a**0.5*t_c**-0.4*(1 + _lambda)**0.1*(cos(radians(Lambda)))**-1.0*s_csw**0.1

## 2) raymer tail weight estimation
# horizontal tail
    def w_htail(self, f_w, b_h, w_dg, n_z, s_ht, l_t, Lambda_ht, a_h, s_e, dtype):
        if dtype == 'allmoving':
            k_uht = 1.143
        elif dtype == 'other':
            k_uht = 1.0
        else:
            print "USAGE: 'dtype' is 'allmoving' or 'other'."

        k_y = 0.3*l_t

        return 0.0379*k_uht*(1 + f_w/b_h)**-0.25*w_dg**0.639*n_z**0.10*s_ht**0.75*l_t**-1.0*k_y**0.704*(cos(radians(Lambda_ht)))**-1.0*a_h**0.166*(1 + s_e/s_ht)**0.1

# vertical tail
    def w_vtail(self, w_dg, n_z, l_t, s_vt, Lambda_vt, a_v, t_c, h_t=None, h_v=None, dtype=None):
        k_z = l_t

        if h_t == h_v == None:
            if dtype == 'conv':
                h_t = 0
                h_v = 1
            elif dtype == 'ttail':
                h_t = 1
                h_v = 1
            else:
                print "USAGE: 'dtype' is 'conv' or 'ttail'."

        return 0.0026*(1 + h_t/h_v)**0.225*w_dg**0.556*n_z**0.536*l_t**-0.5*s_vt**0.5*k_z**0.875*(cos(radians(Lambda_vt)))**-1*a_v**0.35*(t_c)**-0.5

## 3) raymer fuselage weight estimation
    def w_f(self, w_dg, n_z, l, s_f, d, _lambda, Lambda, b_w, door, landing):
        if door == 'nocargo':
            k_door = 1.0
        elif door == 'onecargo':
            k_door = 1.06
        elif door == 'twocargo':
            k_door = 1.12
        elif door == 'clam':
            k_door = 1.12
        elif door == 'cargoclam':
            k_door = 1.25
        else:
            print "USAGE: 'door' is 'nocargo' or  'onecargo' or  'twocargo' or  'clam' or 'cargoclam'."

        if landing == 'fuselage':
            k_lg = 1.12
        elif landing == 'other':
            k_lg = 1.0
        else:
            print "USAGE: 'landing' is 'fuselage' or 'other'."

        k_ws = 0.75*((1 + 2*_lambda)/(1 + _lambda))*(b_w*tan(radians(Lambda))/l)

        return 0.3280*k_door*k_lg*(w_dg*n_z)**0.5*l**0.25*s_f**0.302*(1 + k_ws)**0.04*(l/d)**0.10

## 4) raymer landing gear weight estimation
# main landing gear
    def w_ucm(self, w_l, n_l, l_m, n_mw, n_mss, v_stall, dtype):
        if dtype == 'kneeling':
            k_mp = 1.126
        elif dtype == 'other':
            k_mp = 1.0
        else:
            print "USAGE: 'dtype' is 'kneeling' or 'other'."

        return 0.0106*k_mp*w_l**0.888*n_l**0.25*l_m**0.4*n_mw**0.321*n_mss**-0.5*v_stall**0.1

# nose landing gear
    def w_ucn(self, w_l, n_l, l_n, n_nw, dtype):
        if dtype == 'kneeling':
            k_np = 1.15
        elif dtype == 'other':
            k_np = 1.0
        else:
            print "USAGE: 'dtype' is 'kneeling' or 'other'."

        return 0.032*k_np*w_l**0.646*n_l**0.2*l_n**0.5*n_nw**0.45

## 5) raymer nacelle (engine) weight estimation
    def w_n(self, n_lt, n_w, n_z, w_ec, n_en, s_n, dtype):
        if dtype == 'pylon':
            k_ng = 1.017
        elif dtype == 'other':
            k_ng = 1.0
        else:
            print "USAGE: 'dtype' is 'pylon' or 'other'."

        return 0.6724*k_ng*n_lt**0.10*n_w**0.294*n_z**0.119*w_ec**0.611*n_en**0.984*s_n**0.224

    """
    RAYMER PROPULSION GROUP
    """
## 6) raymer engine controls weight estimation
    def w_enc(self, n_en, l_ec):
        return 5.0*n_en + 0.80*l_ec

## 7) raymer started (pneumatic) weight estimation
    def w_s(self, n_en, w_en):
        return 49.19*(n_en*w_en/1000)**0.541

## 8) raymer fuel system weight estimation
    def w_fs(self, v_t, v_i, v_p, n_t):
        return 2.405*v_t**0.606*(1 + v_i/v_t)**-1.0*(1 + v_p/v_t)*n_t**0.5


    """
    RAYMER EQUIPMENT GROUP
    """
## 9) raymer flight controls weight estimation
    def w_fc(self, n_f, n_m, s_cs, i_y):
        return 145.9*n_f**0.554*(1 + n_m/n_f)**-1.0*s_cs**0.20*(i_y*1e-6)**0.07

## 10) raymer APU installed weight estimation
    def w_apui(self, w_apuu):
        return 2.2*w_apuu

## 11) raymer instruments weight estimation
    def w_instr(self, n_c, n_en, l_f, b_w, engine, dtype):
        if engine == 'reciprocating':
            k_r = 1.133
        elif engine == 'other':
            k_r = 1.0
        else:
            print "USAGE: 'engine' is 'reciprocrating' or 'other'."

        if dtype == 'turboprop':
            k_tp = 0.793
        elif dtype == 'other':
            k_tp = 1.0
        else:
            print "USAGE: 'dtype' is 'turboprop' or 'other'."

        return 4.509*k_r*k_tp*n_c**0.541*n_en*(l_f + b_w)**0.5

## 12) raymer hydraulics weight estimation
    def w_hydr(self, n_f, l_f, b_w):
        return 0.2673*n_f*(l_f + b_w)**0.937

## 13) raymer electrical weight estimation
    def w_el(self, r_kva, l_a, n_gen):
        return 7.291*r_kva**0.782*l_a**0.346*n_gen**0.10

## 14) raymer avionics weight estimation
    def w_av(self, w_uav):
        return 1.73*w_uav**0.983

## 15) raymer furnishings weight estimation
    def w_furn(self, n_c, w_c, s_f):
        return 0.0577*n_c**0.1*w_c**0.393*s_f**0.75

## 16) raymer air conditioning weight estimation
    def w_ac(self, n_p, v_pr, w_uav):
        return 62.36*n_p**0.25*(v_pr/1000)**0.604*w_uav**0.10

## 17) raymer anti-ice weight estimation
    def w_ai(self, w_dg):
        return 0.002*w_dg

## 18) raymer handling gear weight estimation
    def w_hand(self, w_dg):
        return 3.0e-4*w_dg

## 19) raymer military cargo handling system
#s_cf (cargo floot area, ft^2)
    def w_mil(self, s_cf):
        return 2.4*s_cf


class Gd:
    """
    GD STRUCTURES GROUP
    """
## 1) GD wing
# m_h from 0.4 to 0.8, tcm from 0.08 to 0.15, a from 4 to 12
    def w_w(self, s, a, m_h, w_to, n_ult, _lambda, t_cm, _Lambda_12):
        return (0.00428*s**0.48*a*m_h**0.43*(w_to*n_ult)**0.84*_lambda**0.14)/((100*t_cm)**0.76*cos(radians(_Lambda_12))**1.54)

## 2) GD tail
# horizontal tail
    def w_h(self, w_to, n_ult, s_h, b_h, t_rh, c, l_h):
        return 0.0034*((w_to*n_ult)**0.813*s_h**0.584*(b_h/t_rh)**0.033*(c/l_h)**0.28)**0.915

# vertical tail
    def w_v(self, z_h, b_v, w_to, n_ult, s_v, m_h, l_v, s_r, a_v, _lambda_v, _Lambda_14v):
        return 0.19*((1 + z_h/b_v)**0.5*(w_to*n_ult)**0.363*s_v**1.089*m_h**0.601*l_v**-0.726*(1 + s_r/s_v)**0.217*a_v**0.337*(1 + _lambda_v)**0.363*cos(radians(_Lambda_14v))**-0.484)**1.014

## 3) GD fuselage
    def w_f(self,q_d, w_to, l_f, h_f, inlets):
        if inlets == 'in':
            k_inl = 1.25
        elif inlets == 'out':
            k_inl = 1.0
        else:
            print "USAGE: 'inlets' is 'in' or 'out'."

        return 2*10.43*k_inl**1.42*(q_d/100)**0.283*(w_to/1000)**0.95*(l_f/h_f)**0.71

## 4) GD nacelle
    def w_n(self, n_inl, a_in, l_n, p_2, dtype):
        if dtype == 'turbojet':
            k_n = 3.0
        elif dtype == 'turbofan':
            k_n = 7.435
        else:
            print "USAGE: 'dtype' is 'turbojet' or 'turbofan'."

        return k_n*n_inl*(a_in**0.5*l_n*p_2)**0.731

## 5) GD landing gear
    def w_g(self, w_to):
        return 62.61*(w_to/1000)**0.84

    """
    GD PROPULSION GROUP
    """

## 7) GD engine: THIS ONE LOOK AT p. 85 roskam
    def w_e(self, n_e, w_eng):
        return n_e*w_eng

## 8) GD air induction
# p_2 from 15 to 50
    def w_ai(self, n_inl, l_d, a_inl, p_2, cross, m_d):
        if cross == 'flat':
            k_d = 1.33
        elif cross == 'curved':
            k_d = 1.0
        else:
            print "USAGE: 'cross' is 'flat' or 'curved'."

        if m_d == 'belowmd':
            k_m = 1.0
        elif m_d == 'abovemd':
            k_m = 1.5
        else:
            print "USAGE: 'm_d' is 'below' or 'above'."

        return 0.32*n_inl*l_d*a_inl**0.65*p_2**0.6 + 1.735*(l_d*n_inl*a_inl**0.5*p_2*k_d*k_m)**0.7331

## 9) GD propeller
    def w_prop(self, n_p, n_bl, d_p, p_to, n_e, prop):
        if prop == 'above':
            k_prop = 24.0
        elif prop == 'below':
            k_prop = 31.92
        else:
            print "USAGE: 'prop' is 'above' or 'below'."

        return k_prop*n_p*n_bl**0.391*(d_p*(p_to/n_e)/1000)**0.782

## 10) GD fuel system
    def w_fs(self, w_f, w_supp, sealing, fuel):
        if sealing == 'self':
            k_fs = 41.6
            e_fs = 0.818
        elif sealing == 'nonself':
            k_fs = 23.1
            e_fs = 0.758
        else:
            print "USAGE: 'sealing' is 'self' or 'nonself'."

        if fuel == 'aviation':
            k_fsp = 5.87
        elif fuel == 'jp4':
            k_fsp = 6.55
        else:
            print "USAGE: 'fuel' is 'aviation' or 'jp4'."

        return k_fs*((w_f/k_fsp)/1000)**e_fs + w_supp

## 11) GD propulsion system
# engine controls: fuselage/wing-root mounted jet engines
    def w_ec(self, l_f, n_e, dtype, b=None):
        if dtype == 'rootafter':
            k_ec = 0.686
            k_frac = 1
            e_ec = 0.792
            b = 0
        elif dtype == 'rootnoafter':
            k_ec = 1.080
            k_frac = 1
            e_ec = 0.792
            b = 0
        elif dtype == 'jet':
            k_ec = 88.46
            k_frac = 100
            e_ec = 0.294
        elif dtype == 'turboprops':
            k_ec = 56.84
            k_frac = 100
            e_ec = 0.514
        elif dtype == 'piston':
            k_ec = 60.27
            k_frac = 100
            e_ec = 0.724
        else:
            print "USAGE: 'afterburning' is 'no' or 'yes'."

        return k_ec*((l_f + b)*n_e/k_frac)**e_ec

# engine starting systems:
    def w_ess(self, w_e, system):
        if system == 'jetcp': # one or two jet engines using cartridge or pneumatic ss
            k_ess = 9.33
            e_ess = 1.078
        elif system == 'jetp': # four or more jet engines using pneumatic ss
            k_ess = 49.19
            e_ess = 0.541
        elif system == 'jete': # jet engines using electric ss
            k_ess = 38.93
            e_ess = 0.918
        elif system == 'turboprop':
            k_ess = 12.05
            e_ess = 1.458
        elif system == 'piston':
            k_ess = 50.38
            e_ess = 0.459
        else:
            print "USAGE: 'system' is 'jetcp' or 'jetp' or 'jete' or 'turboprop' or 'piston'."

        return k_ess*(w_e/1000)**e_ess

# propeller controls:
    def w_pc(self, n_bl, n_p, d_p, p_to, n_e, propeller):
        if propeller == 'turboprops':
            k_pc = 0.322
            e_pc1 = 0.589
            e_pc2 = 1.178
        elif propeller == 'piston':
            k_pc = 4.552
            e_pc1 = 0.379
            e_pc2 = 0.759
        else:
            print "USAGE: 'propeller' is 'turboprop' or 'piston'."

        return k_pc*n_bl**e_pc1*((n_p*d_p*p_to/n_e)/1000)**e_pc2

    """
    GD EQUIPMENT GROUP
    """

## 12) GD flight control system
    def w_fc(self, w_to, q_d):
        return 56.01*(w_to*q_d/100000)**0.576

## 13) GD hydraulic / pneumatic system
# k_hydr = 0.0060 - 0.0120
    def w_hydr(self, k_hydr, w_to):
        return k_hydr*w_to

## 14) GD electrical system
    def w_els(self, w_fs, w_iae):
        return 1163*((w_fs + w_iae)/1000)**0.506

## 15) GD instrumentation, avionics, electronics
    def w_i(self, n_pil, w_to, n_e):
        return n_pil*(15 + 0.032*(w_to/1000)) + n_e*(5 + 0.006*(w_to/1000)) + 0.15*(w_to/1000) + 0.012*w_to

## 16) GD air-conditioning, pressurization, anti- and deicing systems
    def w_api(self, v_pax, n_cr, n_pax):
        return 469*(v_pax*(n_cr + n_pax)/10000)**0.419

## 17) GD oxygen system
    def w_ox(self, n_cr, n_pax):
        return 7*(n_cr + n_pax)**0.702

## 18) GD auxiliary power unit
# k_apu = 0.004 to 0.013
    def w_apu(self, k_apu, w_to):
        return k_apu*w_to

## 19) GD furnishing CHECK RANGE 'LONG' -> k_buf
    def w_fur(self, n_fdc, n_pax, n_cc, p_c, w_to, drange):
        if drange == 'business':
            k_lav = 3.90
            k_buf = 5.68
        elif drange == 'short':
            k_lav = 0.31
            k_buf = 1.02
        elif drange == 'long':
            k_lav = 1.11
            k_buf = 5.68
        else:
            print "USAGE: 'drange' is 'business' or 'long' or 'short'."

        return 55*n_fdc + 32*n_pax + 15*n_cc + k_lav*n_pax**1.33 + k_buf*n_pax**1.12 + 109*(n_pax*(1 + p_c)/100)**0.505 + 0.771*(w_to/1000)

## 20) GD baggage and cargo handling THIS IS FOR MILITARY PASSENGER TRANSPORT THOUGH!
    def w_bc(self, n_pax, preload):
        if preload == 'no':
            k_bc = 0.0646
        elif preload == 'yes':
            k_bc = 0.316
        else:
            print "USAGE: 'preload' is 'no' or 'yes'."

        return k_bc*n_pax**1.456

## 21) GD auxiliary gear
    def w_aux(self, w_e):
        return 0.01*w_e

## 22) GD paint
# k_pt = 0.003 - 0.006
    def w_pt(self, k_pt, w_to):
        return k_pt*w_to

