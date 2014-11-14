"""
The weight estimation is done by summing the necessary equations of each method.
"""

import parse as p
import methods
import cairoplot

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
    ray['w_w'] = raymer.w_w(d2['w_dg'], d2['n_z'], d2['s_w'], d2['a'], d2['t_c'], d2['lambda'], d2['Lambda'], d2['s_csw'])
    ray['w_htail'] = raymer.w_htail(d2['f_w'], d2['b_h'], d2['w_dg'], d2['n_z'], d2['s_ht'], d2['l_t'], d2['Lambda_ht'], d2['a_h'], d2['s_e'], 'allmoving')
    ray['w_vtail'] = raymer.w_vtail(d2['w_dg'], d2['n_z'], d2['l_t'], d2['s_vt'], d2['Lambda_vt'], d2['a_v'], d2['t_c'], None, None, 'ttail')
    ray['w_f'] = raymer.w_f(d2['w_dg'], d2['n_z'], d2['l'], d2['s_f'], d2['d'], d2['lambda'], d2['Lambda'], d2['b_w'], 'nocargo', 'fuselage')
    ray['w_ucm'] = raymer.w_ucm(d2['w_l'], d2['n_l'], d2['l_m'], d2['n_mw'], d2['n_mss'], d2['v_stall'], 'kneeling')
    ray['w_ucn'] = raymer.w_ucn(d2['w_l'], d2['n_l'], d2['l_n'], d2['n_nw'], 'kneeling')
    ray['w_n'] = raymer.w_n(d2['n_lt'], d2['n_w'], d2['n_z'], d2['w_ec'], d2['n_en'], d2['s_n'], 'pylon')
    ray['w_enc'] = raymer.w_enc(d2['n_en'], d2['l_ec'])
    ray['w_s'] = raymer.w_s(d2['n_en'], d2['w_en'])
    ray['w_fs'] = raymer.w_fs(d2['v_t'], d2['v_i'], d2['v_p'], d2['n_t'])
    ray['w_fc'] = raymer.w_fc(d2['n_f'], d2['n_m'], d2['s_cs'], d2['i_y'])
    ray['w_apui'] = raymer.w_apui(d2['w_apuu'])
    ray['w_instr'] = raymer.w_instr(d2['n_c'], d2['n_en'], d2['l_f'], d2['b_w'], 'reciprocating', 'turboprop')
    ray['w_hydr'] = raymer.w_hydr(d2['n_f'], d2['l_f'], d2['b_w'])
    ray['w_el'] = raymer.w_el(d2['r_kva'], d2['l_a'], d2['n_gen'])
    ray['w_av'] = raymer.w_av(d2['w_uav'])
    ray['w_furn'] = raymer.w_furn(d2['n_c'], d2['w_c'], d2['s_f'])
    ray['w_ac'] = raymer.w_ac(d2['n_p'], d2['v_pr'], d2['w_uav'])
    ray['w_ai'] = raymer.w_ai(d2['w_dg'])
    ray['w_hand'] = raymer.w_hand(d2['w_dg'])
    ray['w_mil'] = raymer.w_mil(d2['s_cf'])
    gd = methods.Gd()

    gd = {}

    return tor, ray, gd

def pie_chart(data1, data2):
    tor = data1
    cairoplot.pie_plot("piechart1", tor, 500, 500, (0,0,0), True, False, None)

    ray = data2
    cairoplot.pie_plot("piechart2", ray, 500, 500, (0,0,0), True, False, None)


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
    print "wing", ray['w_w']
    print "htail", ray['w_htail']
    print "vtail", ray['w_vtail']
    print "fuselage", ray['w_f']
    print "landing main", ray['w_ucm']
    print "landing nose", ray['w_ucn']
    print "nacelle", ray['w_n']
    print "engine control", ray['w_enc']
    print "pneumatic", ray['w_s']
    print "fuel", ray['w_fs']
    print "flight controls", ray['w_fc']
    print "apu", ray['w_apui']
    print "instruments", ray['w_instr']
    print "hydraulics", ray['w_hydr']
    print "electrical", ray['w_el']
    print "avionics", ray['w_av']
    print "furnishing", ray['w_furn']
    print "air-cond.", ray['w_ac']
    print "anti-ice", ray['w_ai']
    print "handling gear", ray['w_hand']
    print "military cargo", ray['w_mil']
    print "raymer total", sum(ray.values())

    print "------------- GD -------------"

    pie_chart(tor, ray)

if __name__ == "__main__":
    main()
