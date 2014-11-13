"""
The weight estimation is done by summing the necessary equations of each method.
"""

import parse as p
import methods

def weight():
    d1, d2, d3 = p.parse_xml()

    torenbeek = methods.Torenbeek()

    tor = {}
    tor['w_w'] = torenbeek.w_w(d1['w_g'], d1['b_ref'], d1['Lambda'], d1['b'], d1['n_ult'], d1['s_w'], d1['t_r'], 'si')
    tor['w_tail'] = torenbeek.w_tail(d1['n_ult'], d1['s_v'], d1['s_h'], 'im')
    tor['w_htail'] = torenbeek.w_htail(d1['s_h'], d1['v_d'], d1['Lambda_h'], 'fixed')
    tor['w_vtail'] = torenbeek.w_vtail(d1['s_v'], d1['v_d'], d1['Lambda_v'], 'fuselage')
    tor['w_f'] = torenbeek.w_f(d1['v_d'], d1['l_t'], d1['b_f'], d1['h_f'], d1['s_g'], 'im', 'main')
    tor['w_n'] = torenbeek.w_n(d1['p_to'], 'im')
    tor['w_ucm'] = torenbeek.w_uc(d1['a_m'], d1['b_m'], d1['c_m'], d1['d_m'], d1['w_to'], 'im', 'low')
    tor['w_ucn'] = torenbeek.w_uc(d1['a_n'], d1['b_n'], d1['c_n'], d1['d_n'], d1['w_to'], 'im', 'low')
    tor['w_sc'] = torenbeek.w_sc(d1['w_to'], 'im', 'light')
    tor['w_eni'] = torenbeek.w_eni(d1['n_e'], d1['w_e'])
    tor['w_acc'] = torenbeek.w_acc(d1['n_e'], d1['w_fto'], 'im')
    tor['w_airi'] = torenbeek.w_airi(d1['l_d'], d1['n_i'], d1['a_i'], 'im', 'single')
    tor['w_ext'] = torenbeek.w_ext(d1['ax'], 'im')
    tor['w_oc'] = torenbeek.w_oc(d1['n_e'], d1['w_e'])
    tor['w_fsi'] = torenbeek.w_fsi(d1['n_e'], d1['n_ft'], d1['v_ft'], 'im')
    tor['w_wis'] = torenbeek.w_wis(d1['v_wt'], 'im')
    tor['w_pi'] = torenbeek.w_pi(d1['n_p'], d1['b_p'], d1['d_p'], d1['p_to'], 'im')
    tor['w_tr'] = torenbeek.w_tr(d1['n_e'], d1['w_e'])
    tor['w_apu'] = torenbeek.w_apu(d1['w_ba'], 'im')
    tor['w_navp'] = torenbeek.w_navp(d1['w_to'], 'im')
    tor['w_heu'] = torenbeek.w_heu(d1['w_e'], 'im', 'utility')
    tor['w_api'] = torenbeek.w_api(d1['l_pax'], 'im')
    tor['w_ox'] = torenbeek.w_ox(d1['n_pax'], 'below')
    tor['w_fur'] = torenbeek.w_fur(d1['w_zf'], 'im')

    raymer = methods.Raymer()

    ray = {}


    gd = methods.Gd()

    gd = {}

    return tor, ray, gd

def main():
    tor, ray, gd = weight()
    print "--------- TORENBEEK ----------"
    print "wing", tor['w_w']
    print "tail", tor['w_tail']
    print "htail", tor['w_htail']
    print "vtail", tor['w_vtail']
    print "fuselage", tor['w_f']
    print "nacelle", tor['w_n']
    print "landing main", tor['w_ucm']
    print "landing nose", tor['w_ucn']
    print "surface controls", tor['w_sc']
    print "engine", tor['w_eni']
    print "accessory", tor['w_acc']
    print "air induction", tor['w_airi']
    print "exhaust", tor['w_ext']
    print "oil/cooler", tor['w_oc']
    print "fuel", tor['w_fsi']
    print "water injection", tor['w_wis']
    print "propeller install.", tor['w_pi']
    print "thrust reversers", tor['w_tr']
    print "apu", tor['w_apu']
    print "instruments", tor['w_navp']
    print "hydraulic/electrical", tor['w_heu']
    print "air-cond./pressure/anti-ice", tor['w_api']
    print "oxygen", tor['w_ox']
    print "furnishing", tor['w_fur']
    print "torenbeek total", sum(tor.values())

    print "----------- RAYMER -----------"

    print "------------- GD -------------"

if __name__ == "__main__":
    main()
