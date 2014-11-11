"""
The weight estimation is done by summing the necessary equations of each method.
"""

import parse as p
import methods

def weight():
    d1, d2, d3 = p.parse_xml()

    torenbeek = methods.Torenbeek()

    tor = {}
    tor['w_w'] = torenbeek.w_w(d1['w_g'], d1['b_ref'], d1['Lambda'], d1['b'], d1['n_ult'], d1['s'], d1['t_r'], 'si')
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

    return tor

def main():
    tor = weight()
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
    print "torenbeek total", sum(tor.values())


if __name__ == "__main__":
    main()
