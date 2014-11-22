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
    tor['w_w'] = torenbeek.w_w(d1['w_g'], d1['b_ref'], d1['Lambda'], d1['b'], d1['n_ult'], d1['s_w'], d1['t_r'], d1['tunit_w'])
    tor['w_tail'] = torenbeek.w_tail(d1['n_ult'], d1['s_v'], d1['s_h'], d1['tunit_tail'])
    tor['w_htail'] = torenbeek.w_htail(d1['s_h'], d1['v_d'], d1['Lambda_h'], d1['ttype_htail'])
    tor['w_vtail'] = torenbeek.w_vtail(d1['s_v'], d1['v_d'], d1['Lambda_v'], d1['ttype_vtail'])
    tor['w_f'] = torenbeek.w_f(d1['v_d'], d1['l_t'], d1['b_f'], d1['h_f'], d1['s_g'], d1['tunit_f'], d1['ttype_f'])
    tor['w_n'] = torenbeek.w_n(d1['p_to'], d1['tunit_n'])
    tor['w_ucm'] = torenbeek.w_uc(d1['a_m'], d1['b_m'], d1['c_m'], d1['d_m'], d1['w_to'], d1['tunit_ucm'], d1['ttype_ucm'])
    tor['w_ucn'] = torenbeek.w_uc(d1['a_n'], d1['b_n'], d1['c_n'], d1['d_n'], d1['w_to'], d1['tunit_ucn'], d1['ttype_ucn'])
    tor['w_sc'] = torenbeek.w_sc(d1['w_to'], d1['tunit_sc'], d1['ttype_sc'])
    tor['w_eni'] = torenbeek.w_eni(d1['n_e'], d1['w_e'])
    tor['w_acc'] = torenbeek.w_acc(d1['n_e'], d1['w_fto'], d1['tunit_acc'])
    tor['w_airi'] = torenbeek.w_airi(d1['l_d'], d1['n_i'], d1['a_i'], d1['tunit_airi'], d1['ttype_airi'])
    tor['w_ext'] = torenbeek.w_ext(d1['ax'], d1['tunit_ext'])
    tor['w_oc'] = torenbeek.w_oc(d1['n_e'], d1['w_e'])
    tor['w_fsi'] = torenbeek.w_fsi(d1['n_e'], d1['n_ft'], d1['v_ft'], d1['tunit_fsi'])
    tor['w_wis'] = torenbeek.w_wis(d1['v_wt'], d1['tunit_wis'])
    tor['w_pi'] = torenbeek.w_pi(d1['n_p'], d1['b_p'], d1['d_p'], d1['p_to'], d1['tunit_pi'])
    tor['w_tr'] = torenbeek.w_tr(d1['n_e'], d1['w_e'])
    tor['w_apu'] = torenbeek.w_apu(d1['w_ba'], d1['tunit_apu'])
    tor['w_navp'] = torenbeek.w_navp(d1['w_to'], d1['tunit_navp'])
    tor['w_heu'] = torenbeek.w_heu(d1['w_e'], d1['tunit_heu'], d1['ttype_heu'])
    tor['w_api'] = torenbeek.w_api(d1['l_pax'], d1['tunit_api'])
    tor['w_ox'] = torenbeek.w_ox(d1['n_pax'], d1['ttype_ox'])
    tor['w_fur'] = torenbeek.w_fur(d1['w_zf'], d1['tunit_fur'])


    raymer = methods.Raymer()

    ray = {}
    ray['w_w'] = raymer.w_w(d2['w_dg'], d2['n_z'], d2['s_w'], d2['a'], d2['t_c'], d2['lambda'], d2['Lambda'], d2['s_csw'])
    ray['w_htail'] = raymer.w_htail(d2['f_w'], d2['b_h'], d2['w_dg'], d2['n_z'], d2['s_ht'], d2['l_t'], d2['Lambda_ht'], d2['a_h'], d2['s_e'], d2['rtype_htail'])
    ray['w_vtail'] = raymer.w_vtail(d2['w_dg'], d2['n_z'], d2['l_t'], d2['s_vt'], d2['Lambda_vt'], d2['a_v'], d2['t_c'], None, None, d2['rtype_vtail'])
    ray['w_f'] = raymer.w_f(d2['w_dg'], d2['n_z'], d2['l'], d2['s_f'], d2['d'], d2['lambda'], d2['Lambda'], d2['b_w'], d2['rtype_f1'], d2['rtype_f2'])
    ray['w_ucm'] = raymer.w_ucm(d2['w_l'], d2['n_l'], d2['l_m'], d2['n_mw'], d2['n_mss'], d2['v_stall'], d2['rtype_ucm'])
    ray['w_ucn'] = raymer.w_ucn(d2['w_l'], d2['n_l'], d2['l_n'], d2['n_nw'], d2['rtype_ucn'])
    ray['w_n'] = raymer.w_n(d2['n_lt'], d2['n_w'], d2['n_z'], d2['w_ec'], d2['n_en'], d2['s_n'], d2['rtype_n'])
    ray['w_enc'] = raymer.w_enc(d2['n_en'], d2['l_ec'])
    ray['w_s'] = raymer.w_s(d2['n_en'], d2['w_en'])
    ray['w_fs'] = raymer.w_fs(d2['v_t'], d2['v_i'], d2['v_p'], d2['n_t'])
    ray['w_fc'] = raymer.w_fc(d2['n_f'], d2['n_m'], d2['s_cs'], d2['i_y'])
    ray['w_apui'] = raymer.w_apui(d2['w_apuu'])
    ray['w_instr'] = raymer.w_instr(d2['n_c'], d2['n_en'], d2['l_f'], d2['b_w'], d2['rtype_instr1'], d2['rtype_instr2'])
    ray['w_hydr'] = raymer.w_hydr(d2['n_f'], d2['l_f'], d2['b_w'])
    ray['w_el'] = raymer.w_el(d2['r_kva'], d2['l_a'], d2['n_gen'])
    ray['w_av'] = raymer.w_av(d2['w_uav'])
    ray['w_furn'] = raymer.w_furn(d2['n_c'], d2['w_c'], d2['s_f'])
    ray['w_ac'] = raymer.w_ac(d2['n_p'], d2['v_pr'], d2['w_uav'])
    ray['w_ai'] = raymer.w_ai(d2['w_dg'])
    ray['w_hand'] = raymer.w_hand(d2['w_dg'])
    ray['w_mil'] = raymer.w_mil(d2['s_cf'])


    gendyn = methods.Gd()

    gd = {}
    gd['w_w'] = gendyn.w_w(d3['s'], d3['a'], d3['m_h'], d3['w_to'], d3['n_ult'], d3['lambda'], d3['t_cm'], d3['Lambda_12'])
    gd['w_h'] = gendyn.w_h(d3['w_to'], d3['n_ult'], d3['s_h'], d3['b_h'], d3['t_rh'], d3['c'], d3['l_h'])
    gd['w_v'] = gendyn.w_v(d3['z_h'], d3['b_v'], d3['w_to'], d3['n_ult'], d3['s_v'], d3['m_h'], d3['l_v'], d3['s_r'], d3['a_v'], d3['lambda_v'], d3['Lambda_14v'])
    gd['w_f'] = gendyn.w_f(d3['q_d'], d3['w_to'], d3['l_f'], d3['h_f'], d3['gtype_f'])
    gd['w_n'] = gendyn.w_n(d3['n_inl'], d3['a_in'], d3['l_n'], d3['p_2'], d3['gtype_n'])
    gd['w_g'] = gendyn.w_g(d3['w_to'])
    gd['w_e'] = gendyn.w_e(d3['n_e'], d3['w_eng'])
    gd['w_ai'] = gendyn.w_ai(d3['n_inl'], d3['l_d'], d3['a_inl'], d3['p_2'], d3['gtype_ai1'], d3['gtype_ai2'])
    gd['w_prop'] = gendyn.w_prop(d3['n_p'], d3['n_bl'], d3['d_p'], d3['p_to'], d3['n_e'], d3['gtype_prop'])
    gd['w_fs'] = gendyn.w_fs(d3['w_f'], d3['w_supp'], d3['gtype_fs1'], d3['gtype_fs2'])
    gd['w_ec'] = gendyn.w_ec(d3['l_f'], d3['n_e'], d3['gtype_ec'])
    gd['w_ecw'] = gendyn.w_ecw(d3['l_f'], d3['b'], d3['n_e'], d3['gtype_ecw'])
    gd['w_ess'] = gendyn.w_ess(gd['w_e'], d3['gtype_ess'])
    gd['w_pc'] = gendyn.w_pc(d3['n_bl'], d3['n_p'], d3['d_p'], d3['p_to'], d3['n_e'], d3['gtype_pc'])
    gd['w_fc'] = gendyn.w_fc(d3['w_to'], d3['q_d'])
    gd['w_hydr'] = gendyn.w_hydr(d3['k_hydr'], d3['w_to'])
    gd['w_els'] = gendyn.w_els(d3['w_fs'], d3['w_iae'])
    gd['w_i'] = gendyn.w_i(d3['n_pil'], d3['w_to'], d3['n_e'])
    gd['w_api'] = gendyn.w_api(d3['v_pax'], d3['n_cr'], d3['n_pax'])
    gd['w_ox'] =  gendyn.w_ox(d3['n_cr'], d3['n_pax'])
    gd['w_apu'] = gendyn.w_apu(d3['k_apu'], d3['w_to'])
    gd['w_fur'] = gendyn.w_fur(d3['n_fdc'], d3['n_pax'], d3['n_cc'], d3['p_c'], d3['w_to'], d3['gtype_fur'])
    gd['w_bc'] = gendyn.w_bc(d3['n_pax'], d3['gtype_bc'])
    gd['w_aux'] = gendyn.w_aux(gd['w_e'])
    gd['w_pt'] = gendyn.w_pt(d3['k_pt'], d3['w_to'])

    return tor, ray, gd

def pie_chart(data1, data2, data3):
    tor = data1
    cairoplot.pie_plot("piechart1", tor, 500, 500, (0,0,0), True, False, None)

    ray = data2
    cairoplot.pie_plot("piechart2", ray, 500, 500, (0,0,0), True, False, None)

    gd = data3
    cairoplot.pie_plot("piechart3", gd, 500, 500, (0,0,0), True, False, None)


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
    print "wing", gd['w_w']
    print "htail", gd['w_h']
    print "vtail", gd['w_v']
    print "fuselage", gd['w_f']
    print "nacelle", gd['w_n']
    print "landing gear", gd['w_g']
    print "engine", gd['w_e']
    print "air induction", gd['w_ai']
    print "propeller", gd['w_prop']
    print "fuel", gd['w_fs']
    print "engine controls 1", gd['w_ec']
    print "engine controls 2", gd['w_ecw']
    print "engine ss", gd['w_ess']
    print "propeller controls", gd['w_pc']
    print "flight control", gd['w_fc']
    print "hydraulic/pneumatic", gd['w_hydr']
    print "electrical", gd['w_els']
    print "instruments/avionics/electronics", gd['w_i']
    print "api", gd['w_api']
    print "oxygen", gd['w_ox']
    print "apu", gd['w_apu']
    print "furnishing", gd['w_fur']
    print "baggage", gd['w_bc']
    print "auxiliary", gd['w_aux']
    print "paint", gd['w_pt']
    print "gd total", sum(gd.values())

    pie_chart(tor, ray, gd)

if __name__ == "__main__":
    main()
