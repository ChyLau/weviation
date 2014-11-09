"""
The weight estimation is done by summing the necessary equations of each method.
"""

import parse as p
import methods

def weight(parsed_data):
    d = parsed_data
    torenbeek = methods.Torenbeek()

    print "wing", torenbeek.w_w(d['w_g'], d['b_ref'], d['Lambda'], d['b'], d['n_ult'], d['s'], d['t_r'], 'si')

    print "tail", torenbeek.w_tail(d['n_ult'], d['s_v'], d['s_h'], 'im')

    print "htail", torenbeek.w_htail(d['s_h'], d['v_d'], d['Lambda_h'], 'fixed')

    print "vtail", torenbeek.w_vtail(d['s_v'], d['v_d'], d['Lambda_v'], 'fuselage')

    print "fuselage", torenbeek.w_f(d['v_d'], d['l_t'], d['b_f'], d['h_f'], d['s_g'], 'im', 'main')

    print "nacelle", torenbeek.w_n(d['p_to'], 'im')

    print "main landing", torenbeek.w_uc(d['a_m'], d['b_m'], d['c_m'], d['d_m'], d['w_to'], 'im', 'low')

    print "nose landing", torenbeek.w_uc(d['a_n'], d['b_n'], d['c_n'], d['d_n'], d['w_to'], 'im', 'low')

    print "surface control", torenbeek.w_sc(d['w_to'], 'im', 'light')

def main():
    data = p.parse_xml()
    weight(data)


if __name__ == "__main__":
    main()
