import wx
import methods
import parse as p
import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib import cm
from matplotlib.font_manager import FontProperties
import lxml.etree as ET
import os

class TabTorenbeek(wx.ScrolledWindow):
    def __init__(self, parent):
        """"""
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(5,15)

        self.init_tab()


    def init_tab(self):
        self.parameters = ['marker', 'line', 'w_g', 'w_to', 'marker', 'line','b_ref', 'Lambda', 'b', 'n_ult', 's_w', 't_r', 'marker', 'line', 'htail type', 'vtail type', 's_v', 's_h', 'Lambda_h', 'Lambda_v', 'marker', 'line', 'fuselage type', 'v_d', 'l_t', 'b_f', 'h_f', 's_g', 'marker', 'line', 'main type', 'nose type', 'a_m', 'b_m', 'c_m', 'd_m', 'a_n', 'b_n', 'c_n', 'd_n', 'marker', 'line', 'surface controls type', 'n_e', 'w_e', 'marker', 'line', 'w_fto', 'marker', 'line', 'air induction type', 'l_d', 'n_i', 'a_i', 'marker', 'line', 'ax', 't_to', 'marker', 'line', 'n_ft', 'v_ft', 'marker', 'line', 'v_wt', 'marker', 'line', 'w_ba', 'marker', 'line', 'w_de','r_d', 'marker', 'line', 'hydr./elec. type', 'p_el','marker', 'line', 'l_pax', 'marker', 'line', 'oxygen type', 'n_pax', 'marker','line', 'w_zf']

        self.components = ['wing', 'tail', 'fuselage', 'nacelle', 'landing main', 'landing nose', 'surface controls', 'engine', 'accessory', 'air induction', 'exhaust', 'oil/cooler', 'fuel system', 'water injection', 'thrust reversers', 'APU', 'instruments', 'hydraulic/lectrical', 'AC/pressure/anti-ice', 'oxygen system', 'furnishing']

        ################ TOOLTIP LIST
        tooltip = ['Gross weight', 'Takeoff weight', 'Reference wing span', 'Sweepback angle at 50% chord', 'Wing span', 'Ultimate load factor', 'Wing area', 'Maximum thickness of root chord', 'Vertical tail area', 'Horizontal tail area', 'Horizontal tail sweep angle', 'Vertical tail sweep angle', 'Design dive speed', 'Distance between 1/4-chord points of wing and horizontal tailplane root', 'Fuselage width', 'Fuselage height', 'Gross shell area of the fuselage', 'Coefficient main landing gear', 'Coefficient main landing gear', 'Coefficient main landing gear', 'Coefficient main landing gear', 'Coefficient nose landing gear', 'Coefficient nose landing gear', 'Coefficient nose landing gear', 'Coefficient nose landing gear', 'Number of engines', 'Engine weight', 'Fuel flow per engine', 'Duct length', 'Number of inlets', 'Capture area per inlet', 'TODO', 'Takeoff thrust per engine', 'Number of fuel tanks', 'Total fuel tank volume', 'Total water tank capacity', 'Rated bleed airflow of APU', 'Delivery empty weight', 'Maximum range with maximum fuel', 'Total electrical generator power', 'Length of passenger cabin', 'Number of passengers', 'Maximum zero fuel weight']

        hbox = wx.BoxSizer(wx.VERTICAL)

        stxt0 = wx.StaticText(self, label='Components')
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        stxt0.SetFont(font)
        line0 = wx.StaticLine(self)
        hbox.Add(stxt0, 0, wx.ALL, 5)
        hbox.Add(line0, 1, wx.ALL|wx.EXPAND, 5)


        self.cball = wx.CheckBox(self, label='(de)select all')
        hbox.Add(self.cball, 0)
        self.Bind(wx.EVT_CHECKBOX, self.select_all, self.cball)

        self.cb_dict = {}
        # component checkboxes

        gs = wx.GridSizer(8, 3, 0, 0)
        for item in self.components:
            cb = wx.CheckBox(self, label=item)
            gs.Add(cb, 0, wx.ALIGN_LEFT)
            self.cb_dict[item] = cb

        hbox.Add(gs, 0)

        # component list
        comp_title = ['General', 'Wing', 'Tail', 'Fuselage','Landing gear,..', 'Engine,..', 'Accessory', 'Air induction', 'Exhaust', 'Fuel system', 'Water injection', 'APU', 'Instruments, ...', 'Electrical', 'Air conditioning', 'Oxygen system', 'Furnishing']

        units_im = ['lb', 'lb', 'ft', 'deg', 'ft', '', 'ft^2', 'ft', 'ft^2', 'ft^2', 'deg', 'deg', 'kts', 'ft', 'ft', 'ft', 'ft^2', '', '', '', '', '', '', '', '', '', 'lb', '', 'ft', '', 'ft^2', 'ft^2', 'N', '', 'gal', 'gal',  '', 'lb', 'ft', 'kVA', 'ft', '', 'ft']

        units_si = ['kg', 'kg', 'm', 'rad', 'm', '', 'm^2', 'm', 'm^2', 'm^2', 'rad', 'rad', 'm/s', 'm', 'm', 'm', 'm^2', '', '', '', '', '', '', '', '', '', 'kg', '', 'm', '', 'm^2', 'm^2', '', '', 'L', 'L',  '', 'kg', 'm', '', 'm', '', 'm']

        htail_type = ['Fixed stabilizer', 'Variable-incidence']
        vtail_type = ['Fuselage-mounted', 'Fin-mounted']
        fuselage_type = ['Pressurized fuselage', 'Main landing gear', 'Rear fuselage', 'Cargo']
        ucm_type = ['Low', 'High']
        ucn_type = ['Low', 'High']
        sc_type = ['Manually controlled', 'Powered controlled']
        airi_type = ['Single flat side', 'Multi flat side']
        heu_type = ['Utility aircraft', 'Jet trainer', 'Propeller transport']
        ox_type = ['Below 25,000 ft', 'Short flight above', 'Extended overwater']
        combo_type = [htail_type, vtail_type, fuselage_type, ucm_type, ucn_type, sc_type, airi_type, heu_type, ox_type]

        sizer = wx.GridBagSizer(0, 0)
        j = 0 # 'comp' list index
        k = 0 # 'combo_type' list index
        m = 0 # 'units_im' list index
        n = 0 # 'units_si' list index
        z = 0 # tooltip list index
        self.par_extra = [] # list for units parameters
        self.tc_dict = {} # dict of TextCtrl
        self.ttype = {} # dict of comboboxes
        self.rb_im = {} # dict of radiobuttons 'im'
        self.rb_si = {} # dict of radiobuttons 'si'
        self.icon_dict = {}

        for i, item in enumerate(self.parameters):
            if item == 'marker':
                comp_name = wx.StaticText(self, label=comp_title[j])
                font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
                comp_name.SetFont(font)
                j += 1
                sizer.Add(comp_name, pos=(i,0), flag=wx.TOP, border=10)
            elif item == 'line':
                line = wx.StaticLine(self)
                sizer.Add(line, pos=(i,0), span=(1,5), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)
            elif 'type' in item:
                combo = wx.ComboBox(self, choices=combo_type[k], style=wx.CB_READONLY)
                combo_title = wx.StaticText(self, label=item)
                self.ttype[item] = combo
                sizer.Add(combo, pos=(i,2))
                sizer.Add(combo_title, pos=(i, 0))
                k += 1
            else:
                par = wx.StaticText(self, label=item)
                tc = wx.TextCtrl(self, wx.ID_ANY, "")
                self.tc_dict[item] = tc

                start_icon = wx.Image('icon.png')
                start_icon.Rescale(20, 20)
                almost_icon = wx.BitmapFromImage(start_icon)
                icon = wx.StaticBitmap(self, -1, almost_icon, wx.DefaultPosition, style=wx.BITMAP_TYPE_PNG)
                self.icon_dict[item] = icon
                icon.SetToolTip(wx.ToolTip(tooltip[z]))
                z += 1
                sizer.Add(par, pos=(i,0))
                sizer.Add(tc, pos=(i,2))
                sizer.Add(icon, pos=(i,1), flag=wx.RIGHT, border=10)

                if units_im[m] == '':
                    m += 1
                    n += 1
                    continue
                else:
                    rb1 = wx.RadioButton(self, label=units_im[m], style=wx.RB_GROUP)
                    sizer.Add(rb1, pos=(i,3))
                    self.rb_im[item] = rb1
                    self.par_extra.append(item)
                    m += 1
                    if units_si[n] == '':
                        filler = wx.StaticText(self, label='')
                        sizer.Add(filler, pos=(i,4))
                        n += 1
                    else:
                        rb2 = wx.RadioButton(self, label=units_si[n])
                        sizer.Add(rb2, pos=(i,4))
                        self.rb_si[item] = rb2
                        n += 1

        hbox.Add(sizer, 0, wx.ALL, 5)
        self.SetSizer(hbox)

    def calculate_weight(self, cunit):

        d1 = {}

        for key, value in self.tc_dict.iteritems():
            if value.GetValue() is not u'':
                if key in self.par_extra:
                    if self.rb_im[key].GetValue() == True:
                        k = 1
                    else:
                        if self.rb_im[key].GetLabel() == 'lb':
                            k = 2.20462
                        elif self.rb_im[key].GetLabel() == 'ft':
                            k = 3.28084
                        elif self.rb_im[key].GetLabel() == 'ft^2':
                            k = 10.7639
                        elif self.rb_im[key].GetLabel() == 'deg':
                            k = 57.2957795
                        elif self.rb_im[key].GetLabel() == 'gal':
                            k = 4.54609
                        else:
                            k = 1
                            print "[INFO]: key %r not specified." % key
                else:
                    k = 1
            d1[key] = k*float(value.GetValue())


        for key, value in self.ttype.iteritems():
            ret = value.GetValue()
            if key == 'htail type':
                if ret == 'Fixed stabilizer':
                    d1['ttype_htail'] = 'fixed'
                elif ret == 'Variable-incidence':
                    d1['ttype_htail'] = 'variable'
            elif key == 'vtail type':
                if ret == 'Fuselage-mounted':
                    d1['ttype_vtail'] = 'fuselage'
                elif ret == 'Fin-mounted':
                    d1['ttype_vtail'] = 'fin'
            elif key == 'fuselage type':
                if ret == 'Pressurized fuselage':
                    d1['ttype_f'] = 'pressurized'
                elif ret == 'Main landing gear':
                    d1['ttype_f'] = 'main'
                elif ret == 'Rear fuselage':
                    d1['ttype_f'] = 'rear'
                elif ret == 'Cargo':
                    d1['ttype_f'] = 'cargo'
            elif key == 'main type':
                if ret == 'Low':
                    d1['ttype_ucm'] = 'low'
                elif ret == 'High':
                    d1['ttype_ucm'] = 'high'
            elif key == 'nose type':
                if ret == 'Low':
                    d1['ttype_ucn'] = 'low'
                elif ret == 'High':
                    d1['ttype_ucn'] = 'high'
            elif key == 'surface controls type':
                if ret == 'Manually controlled':
                    d1['ttype_sc'] = 'transport'
                elif ret == 'Powered controlled':
                    d1['ttype_sc'] = 'transportplus'
            elif key == 'air induction type':
                if ret == 'Single flat side':
                    d1['ttype_airi'] = 'single'
                elif ret == 'Multi flat side':
                    d1['ttype_airi'] = 'multi'
            elif key == 'hydr./elec. type':
                if ret == 'Utility aircraft':
                    d1['ttype_heu'] = 'utility'
                elif ret == 'Jet trainer':
                    d1['ttype_heu'] = 'jet'
                elif ret == 'Propeller transport':
                    d1['ttype_heu'] = 'propeller'
            elif key == 'oxygen type':
                if ret == 'Below 25,000 ft':
                    d1['ttype_ox'] = 'below'
                elif ret == 'Short flight above':
                    d1['ttype_ox'] = 'above'
                elif ret == 'Extended overwater':
                    d1['ttype_ox'] = 'overwater'

        torenbeek = methods.Torenbeek()
        tor = {}

        d1['tunit_w']= 'im'
        d1['tunit_tail']= 'im'
        d1['tunit_htail']= 'im'
        d1['tunit_vtail']= 'im'
        d1['tunit_f']= 'im'
        d1['tunit_n']= 'im'
        d1['tunit_ucm']= 'im'
        d1['tunit_ucn']= 'im'
        d1['tunit_sc']= 'im'
        d1['tunit_eni']= 'im'
        d1['tunit_acc']= 'im'
        d1['tunit_airi']= 'im'
        d1['tunit_ext']= 'im'
        d1['tunit_oc']= 'im'
        d1['tunit_fsi']= 'im'
        d1['tunit_wis']= 'im'
        d1['tunit_pi']= 'im'
        d1['tunit_tr']= 'im'
        d1['tunit_apu']= 'im'
        d1['tunit_navp']= 'im'
        d1['tunit_heu']= 'im'
        d1['tunit_api']= 'im'
        d1['tunit_ox']= 'im'
        d1['tunit_fur']= 'im'

        weights = ['w_w', 'w_tail', 'w_f', 'w_n', 'w_ucm', 'w_ucn', 'w_sc', 'w_eni', 'w_acc', 'w_airi', 'w_ext', 'w_oc', 'w_fsi', 'w_wis', 'w_tr', 'w_apu', 'w_navp', 'w_heu', 'w_api', 'w_ox', 'w_fur']

        # dictionary of weights and components
        reference = {}
        for i, weight in enumerate(weights):
            reference[self.components[i]] = weight

        tor['w_w'] = torenbeek.w_w(d1['w_g'], d1['b_ref'], d1['Lambda'], d1['b'], d1['n_ult'], d1['s_w'], d1['t_r'], d1['tunit_w'])
        tor['w_tail'] = torenbeek.w_htail(d1['s_h'], d1['v_d'], d1['Lambda_h'], d1['ttype_htail']) + torenbeek.w_vtail(d1['s_v'], d1['v_d'], d1['Lambda_v'], d1['ttype_vtail'])
        tor['w_f'] = torenbeek.w_f(d1['v_d'], d1['l_t'], d1['b_f'], d1['h_f'], d1['s_g'], d1['tunit_f'], d1['ttype_f'])
        tor['w_n'] = torenbeek.w_n(d1['t_to'], d1['tunit_n'])
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
        tor['w_tr'] = torenbeek.w_tr(d1['n_e'], d1['w_e'])
        tor['w_apu'] = torenbeek.w_apu(d1['w_ba'], d1['tunit_apu'])
        tor['w_navp'] = torenbeek.w_navp(d1['w_to'], d1['tunit_navp'])
        tor['w_heu'] = torenbeek.w_heu(d1['w_e'], d1['tunit_heu'], d1['ttype_heu'])
        tor['w_api'] = torenbeek.w_api(d1['l_pax'], d1['tunit_api'])
        tor['w_ox'] = torenbeek.w_ox(d1['n_pax'], d1['ttype_ox'])
        tor['w_fur'] = torenbeek.w_fur(d1['w_zf'], d1['tunit_fur'])

        ret = ""
        ret += " TORENBEEK" + "\n" + " ------------------------------" + "\n"

        var = ['w_w', 'w_tail', 'w_f', 'w_n', 'w_ucm', 'w_ucn', 'w_sc', 'w_eni', 'w_acc', 'w_airi', 'w_ext', 'w_oc', 'w_fsi', 'w_wis', 'w_tr', 'w_apu', 'w_navp', 'w_heu', 'w_api', 'w_ox', 'w_fur']

        compvar = dict(zip(self.components, var))

        if cunit == True:
            k_ret = 1
            s_ret = "lb"
        else:
            k_ret = 0.453592
            s_ret = "kg"

        struct_group = ['wing', 'tail', 'fuselage', 'nacelle', 'landing main', 'landing nose', 'surface controls']

        prop_group = ['engine', 'accessory', 'air induction', 'exhaust', 'oil/cooler', 'fuel system', 'water injection', 'thrust reversers']

        equip_group = ['APU', 'instruments', 'hydraulic/lectrical', 'AC/pressure/anti-ice', 'oxygen system', 'furnishing']

        flag_struct = True
        flag_prop = True
        flag_equip = True

        for component in self.components:
            if self.cb_dict[component].GetValue() == True:
                if component in struct_group:
                    if flag_struct == True:
                        ret += " STRUCTURES GROUP\n"
                        flag_struct = False

                if component in prop_group:
                    if flag_prop == True:
                        ret += " PROPULSION GROUP\n"
                        flag_prop = False

                if component in equip_group:
                    if flag_equip == True:
                        ret += " EQUIPMENT GROUP\n"
                        flag_equip = False

                ret += "\t " + component + " (" + compvar[component] + ")" + ": " + str(round(k_ret*tor[reference[component]], 2)) + " " + s_ret + "\n"
            else:
                del tor[compvar[component]]

        if self.cb_dict[component].GetValue() == True:
            ret += " ..................................\n" + " TOTAL: " + str(round(k_ret*sum(tor.values()), 2)) + " " + s_ret + "\n\n"

        return ret, tor

    def load_xml(self, d1):
        utype = ['fixed', 'variable', 'fuselage', 'fin', 'pressurized', 'main', 'rear', 'cargo', 'low', 'high', 'transport', 'transportplus', 'single', 'multi', 'utility', 'jet', 'propeller', 'below', 'above', 'overwater']

        ltype = ['Fixed stabilizer', 'Variable-incidence', 'Fuselage-mounted', 'Fin-mounted', 'Pressurized fuselage', 'Main landing gear', 'Rear fuselage', 'Cargo', 'Low', 'High', 'Manually controlled', 'Powered controlled', 'Single flat side', 'Multi flat side', 'Utility aircraft', 'Jet trainer', 'Propeller transport', 'Below 25,000 ft', 'Short flight above', 'Extended overwater']

        type_too = dict(zip(utype, ltype))

        ktype = ['ttype_htail', 'ttype_vtail', 'ttype_f', 'ttype_ucm', 'ttype_ucn', 'ttype_sc', 'ttype_airi', 'ttype_heu', 'ttype_ox']

        mtype = ['htail type', 'vtail type', 'fuselage type', 'main type', 'nose type', 'surface controls type', 'air induction type', 'hydr./elec. type', 'oxygen type']

        type_moo = dict(zip(ktype, mtype))

        for key, value in d1.iteritems():
            if 'tunit' not in key:
                if 'ttype' in key:
                    self.ttype[type_moo[key]].SetValue((type_too[value]))
                else:
                    self.tc_dict[key].SetValue(str(value))

    def select_all(self, evt):
        label = evt.GetEventObject().GetValue()

        if label:
            for key, value in self.cb_dict.iteritems():
                value.SetValue(True)
        else:
            for key, value in self.cb_dict.iteritems():
                value.SetValue(False)

############################################################################
############################################################################

class TabRaymer(wx.ScrolledWindow):
    def __init__(self, parent):
        """"""
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(5,15)

        self.init_tab()


    def init_tab(self):
        self.parameters = ['marker', 'line', 'w_dg', 'n_z', 'marker', 'line', 'a', 't_c', 'lambda', 'Lambda', 's_w', 's_csw', 'marker', 'line', 'htail type', 'vtail type', 'a_h', 'a_v', 'b_h', 'f_w', 'h_t', 'h_v', 'Lambda_ht', 'Lambda_vt', 'l_t', 's_e', 's_ht', 's_vt', 'marker', 'line', 'fuselage type', 'fuselage door type', 'b_w', 'd', 'l', 's_f', 'marker', 'line', 'nacelle type', 'n_en', 'n_lt', 'n_w', 's_n', 'w_ec', 'marker', 'line', 'main type', 'nose type', 'l_m', 'l_n', 'n_l', 'n_mss', 'n_mw', 'n_nw', 'v_stall', 'w_l', 'marker', 'line', 'l_ec', 'marker', 'line', 'w_en', 'marker', 'line', 'n_t', 'v_i', 'v_p', 'v_t', 'marker', 'line', 'i_y', 'n_f', 'n_m', 's_cs', 'marker', 'line', 'w_apuu', 'marker', 'line', 'engine type', 'aircraft type', 'l_f', 'n_c', 'marker', 'line', 'l_a', 'n_gen', 'r_kva', 'marker', 'line', 'w_uav', 'marker', 'line', 'w_c', 'marker', 'line', 'n_p', 'v_pr']


        self.components = ['wing', 'tail', 'fuselage', 'nacelle', 'landing main', 'landing nose', 'engine', 'engine controls', 'pneumatic', 'fuel system', 'flight controls', 'APU', 'instruments', 'hydraulics', 'electrical', 'avionics', 'furnishing', 'air conditioning', 'anti-icing', 'handling gear']

        tooltip = ['Design gross weight', 'Ultimate load factor', 'Aspect ratio', 'Airfoil thickness (%)', 'Taper ratio', 'Wing sweep at 25% MAC', 'Trapezoidal wing area', 'Control surface area', 'Aspect ratio', 'Aspect ratio', 'Horizontal tail span', 'Fuselage width at horizontal tail intersection', 'Horizontal tail height above fuselage', 'Vertical tail height above fuselage', 'Horizontal tail sweep at 25% MAC', 'Vertical tail sweep at 25% MAC', 'Tail length; wing quarter-MAC to tail quarter-MAC', 'Elevator area', 'Horizontal tail area', 'Vertical tail area', 'Wing span', 'Fuselage structural depth', 'Fuselage structural length', 'Fuselage wetted area', 'Number of engines', 'Nacelle length', 'Nacelle width', 'Nacelle wetted area', 'Weight of engine and contents', 'Length of main landing gear', 'Nose gear length', 'Ultimate landing load factor; = N_gear * 1.5', 'Number of main gear shock struts', 'Number of main wheels', 'Number of nose wheels', 'Stalling velocity', 'Landing design gross weight', 'Length from engine front to cockpit -- total if multiengine', 'Engine weight, each', 'Number of fuel tanks', 'Integral tanks volume', 'Self-sealing protected tanks volume', 'Total fuel volume', 'Yawing moment of inertia', 'Number of functions performed by controls (typically 4-7)', 'Number of mechanical functions (typically 0-2)', 'Total area of control surfaces', 'Uninstalled APU weight', 'Total fuselage length', 'Number of crew', 'Electrical routing distance, generators to avionics to cockpit', 'Number of generators (typically = number of engines)', 'System electrical rating (typically 40-60)', 'Uninstalled avionics weight (typically = 800-1400 lb)', 'Maximum cargo weight', 'Number of personnel onboard (crew and passengers)', 'Volume of pressurized section']

        hbox = wx.BoxSizer(wx.VERTICAL)

        stxt0 = wx.StaticText(self, label='Components')
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        stxt0.SetFont(font)
        line0 = wx.StaticLine(self)
        hbox.Add(stxt0, 0, wx.ALL, 5)
        hbox.Add(line0, 1, wx.ALL|wx.EXPAND, 5)

        self.cball = wx.CheckBox(self, label='(de)select all')
        hbox.Add(self.cball, 0)
        self.Bind(wx.EVT_CHECKBOX, self.select_all, self.cball)

        self.cb_dict = {}
        # component checkboxes

        gs = wx.GridSizer(5, 4, 0, 0)
        for item in self.components:
            cb = wx.CheckBox(self, label=item)
            gs.Add(cb, 0, wx.ALIGN_LEFT)
            self.cb_dict[item] = cb

        hbox.Add(gs, 0)

        # component list
        comp_title = ['General', 'Wing', 'Tail', 'Fuselage', 'Nacelle,..', 'Landing gear,..', 'Engine', 'Pneumatic', 'Fuel system', 'Flight controls,...', 'APU', 'Instruments,...', 'Electrical', 'Avionics', 'Furnishing', 'Air-conditioning']

        units_im = ['lb', '', '', '', '', 'deg', 'ft^2', 'ft^2', '', '', 'ft', 'ft', 'ft', 'ft', 'deg', 'deg', 'ft', 'ft^2', 'ft^2', 'ft^2', 'ft', 'ft', 'ft', 'ft^2', '', 'ft', 'ft', 'ft^2', 'lb', 'ft', 'ft', '', '', '', '', '', 'lb', 'ft', 'lb',  '', 'gal', 'gal', 'gal', 'lb-ft^2', '', '', 'ft^2', 'lb', 'ft', '', 'ft', '', 'kvA', 'lb', 'lb', '', 'ft^3']

        units_si = ['kg', '', '', '', '', 'rad', 'm^2', 'm^2', '', '', 'm', 'm', 'm', 'm', 'rad', 'rad', 'm', 'm^2', 'm^2', 'm^2', 'm', 'm', 'm', 'm^2', '', 'm', 'm', 'm^2', 'kg', 'm', 'm', '', '', '', '', '', 'kg', 'm', 'kg',  '', 'L', 'L', 'L', 'kg-m^2', '', '', 'm^2', 'kg', 'm', '', 'm', '', '', 'lg', 'kg', '', 'm^3']


        htail_type = ['All-moving', 'Other']
        vtail_type = ['Conventional', 'T-tail']
        fuselage1_type = ['Fuselage-mounted main landing gear', 'Other']
        fuselage2_type = ['No cargo door', 'Single side cargo', 'Double side cargo', 'Aft clamshell', 'Double side + aft clamshell']
        nacelle_type = ['Pylon-mounted', 'Other']
        ucm_type = ['Kneeling gear', 'Other']
        ucn_type = ['Kneeling gear', 'Other']
        instr1_type = ['Reciprocating', 'Other']
        instr2_type = ['Turboprop', 'Other']

        combo_type = [htail_type, vtail_type, fuselage1_type, fuselage2_type, nacelle_type, ucm_type, ucn_type, instr1_type, instr2_type]

        sizer = wx.GridBagSizer(0, 0)
        j = 0 # 'comp' list index
        k = 0 # 'combo_type' list index
        m = 0 # 'units_im' list index
        n = 0 # 'units_si' list index
        z = 0 # tooltip list index
        self.par_extra = [] # list for units parameters
        self.tc_dict = {} # dict of TextCtrl
        self.rtype = {} # dict of comboboxes
        self.rb_im = {} # dict of radiobuttons 'im'
        self.rb_si = {} # dict of radiobuttons 'si'

        for i, item in enumerate(self.parameters):
            if item == 'marker':
                comp_name = wx.StaticText(self, label=comp_title[j])
                font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
                comp_name.SetFont(font)
                j += 1
                sizer.Add(comp_name, pos=(i,0), flag=wx.TOP, border=10)
            elif item == 'line':
                line = wx.StaticLine(self)
                sizer.Add(line, pos=(i,0), span=(1,5), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)
            elif 'type' in item:
                combo = wx.ComboBox(self, choices=combo_type[k], style=wx.CB_READONLY)
                combo_title = wx.StaticText(self, label=item)
                self.rtype[item] = combo
                sizer.Add(combo, pos=(i,2))
                sizer.Add(combo_title, pos=(i, 0))
                k += 1
            else:
                par = wx.StaticText(self, label=item)
                tc = wx.TextCtrl(self, wx.ID_ANY, "")
                self.tc_dict[item] = tc

                start_icon = wx.Image('icon.png')
                start_icon.Rescale(20, 20)
                almost_icon = wx.BitmapFromImage(start_icon)
                icon = wx.StaticBitmap(self, -1, almost_icon, wx.DefaultPosition, style=wx.BITMAP_TYPE_PNG)
                icon.SetToolTip(wx.ToolTip(tooltip[z]))
                z += 1

                sizer.Add(par, pos=(i,0))
                sizer.Add(tc, pos=(i,2))
                sizer.Add(icon, pos=(i,1), flag=wx.RIGHT, border=10)
                if units_im[m] == '':
                    m += 1
                    n += 1
                    continue
                else:
                    rb1 = wx.RadioButton(self, label=units_im[m], style=wx.RB_GROUP)
                    sizer.Add(rb1, pos=(i,3))
                    self.rb_im[item] = rb1
                    self.par_extra.append(item)
                    m += 1
                    if units_si[n] == '':
                        filler = wx.StaticText(self, label='')
                        sizer.Add(filler, pos=(i,4))
                        n += 1
                    else:
                        rb2 = wx.RadioButton(self, label=units_si[n])
                        sizer.Add(rb2, pos=(i,4))
                        self.rb_si[item] = rb2
                        n += 1

        hbox.Add(sizer, 0, wx.ALL, 5)
        self.SetSizer(hbox)

    def calculate_weight(self, cunit):

        d2 = {}

        for key, value in self.tc_dict.iteritems():
            if value.GetValue() is not u'':
                if key in self.par_extra:
                    if self.rb_im[key].GetValue() == True:
                        k = 1
                    else:
                        if self.rb_im[key].GetLabel() == 'lb':
                            k = 2.20462
                        elif self.rb_im[key].GetLabel() == 'ft':
                            k = 3.28084
                        elif self.rb_im[key].GetLabel() == 'ft^2':
                            k = 10.7639
                        elif self.rb_im[key].GetLabel() == 'deg':
                            k = 57.2957795
                        elif self.rb_im[key].GetLabel() == 'gal':
                            k = 4.54609
                        elif self.rb_im[key].GetLabel() == 'in.':
                            k = 0.393701
                        elif self.rb_im[key].GetLabel() == 'lb-ft^2':
                            k = 23.73036
                        elif self.rb_im[key].GetLabel() == 'ft^3':
                            k = 35.3147
                        else:
                            k = 1
                            print "[INFO]: key %r not specified." % key
                else:
                    k = 1
            d2[key] = k*float(value.GetValue())


        for key, value in self.rtype.iteritems():
            ret = value.GetValue()
            if key == 'htail type':
                if ret == 'All-moving':
                    d2['rtype_htail'] = 'allmoving'
                elif ret == 'Other':
                    d2['rtype_htail'] = 'other'
            elif key == 'vtail type':
                if ret == 'Conventional':
                    d2['rtype_vtail'] = 'conv'
                elif ret == 'T-tail':
                    d2['rtype_vtail'] = 'ttail'
            elif key == 'fuselage door type':
                if ret == 'No cargo door':
                    d2['rtype_f1'] = 'nocargo'
                elif ret == 'Single side cargo':
                    d2['rtype_f1'] = 'onecargo'
                elif ret == 'Double side cargo':
                    d2['rtype_f1'] = 'twocargo'
                elif ret == 'Aft clamshell':
                    d2['rtype_f1'] = 'clam'
                elif ret == 'Double side + aft clamshell':
                    d2['rtype_f1'] = 'cargoclam'
            elif key == 'fuselage type':
                if ret == 'Fuselage-mounted main landing gear':
                    d2['rtype_f2'] = 'fuselage'
                elif ret == 'Other':
                    d2['rtype_f2'] = 'other'
            elif key == 'fuselage door type':
                if ret == 'No cargo door':
                    d2['rtype_f2'] = 'nocargo'
                elif ret == 'Single side cargo':
                    d2['rtype_f2'] = 'onecargo'
                elif ret == 'Double side cargo':
                    d2['rtype_f2'] = 'twocargo'
                elif ret == 'Aft clamshell':
                    d2['rtype_f2'] = 'clam'
                elif ret == 'Double side + aft clamshell':
                    d2['rtype_f2'] = 'cargoclam'
            elif key == 'nacelle type':
                if ret == 'Pylon-mounted':
                    d2['rtype_n'] = 'pylon'
                elif ret == 'Other':
                    d2['rtype_n'] = 'other'
            elif key == 'main type':
                if ret == 'Kneeling gear':
                    d2['rtype_ucm'] = 'kneeling'
                elif ret == 'Other':
                    d2['rtype_ucm'] = 'other'
            elif key == 'nose type':
                if ret == 'Kneeling gear':
                    d2['rtype_ucn'] = 'kneeling'
                elif ret == 'Other':
                    d2['rtype_ucn'] = 'other'
            elif key == 'engine type':
                if ret == 'Reciprocating':
                    d2['rtype_instr1'] = 'reciprocating'
                elif ret == 'Other':
                    d2['rtype_instr1'] = 'other'
            elif key == 'aircraft type':
                if ret == 'Turboprop':
                    d2['rtype_instr2'] = 'turboprop'
                elif ret == 'Other':
                    d2['rtype_instr2'] = 'other'

        raymer = methods.Raymer()
        ray = {}

        weights = ['w_w', 'w_tail', 'w_f', 'w_n', 'w_ucm', 'w_ucn', 'w_e', 'w_enc', 'w_s', 'w_fs', 'w_fc', 'w_apui', 'w_instr', 'w_hydr', 'w_el', 'w_av', 'w_furn', 'w_ac', 'w_ai', 'w_hand']

        # dictionary of weights and components
        reference = {}
        for i, weight in enumerate(weights):
            reference[self.components[i]] = weight

        ray['w_w'] = raymer.w_w(d2['w_dg'], d2['n_z'], d2['s_w'], d2['a'], d2['t_c'], d2['lambda'], d2['Lambda'], d2['s_csw'])
        ray['w_tail'] = raymer.w_htail(d2['f_w'], d2['b_h'], d2['w_dg'], d2['n_z'], d2['s_ht'], d2['l_t'], d2['Lambda_ht'], d2['a_h'], d2['s_e'], d2['rtype_htail']) + raymer.w_vtail(d2['w_dg'], d2['n_z'], d2['l_t'], d2['s_vt'], d2['Lambda_vt'], d2['a_v'], d2['t_c'], None, None, d2['rtype_vtail'])
        ray['w_f'] = raymer.w_f(d2['w_dg'], d2['n_z'], d2['l'], d2['s_f'], d2['d'], d2['lambda'], d2['Lambda'], d2['b_w'], d2['rtype_f1'], d2['rtype_f2'])
        ray['w_ucm'] = raymer.w_ucm(d2['w_l'], d2['n_l'], d2['l_m'], d2['n_mw'], d2['n_mss'], d2['v_stall'], d2['rtype_ucm'])
        ray['w_ucn'] = raymer.w_ucn(d2['w_l'], d2['n_l'], d2['l_n'], d2['n_nw'], d2['rtype_ucn'])
        ray['w_n'] = raymer.w_n(d2['n_lt'], d2['n_w'], d2['n_z'], d2['w_ec'], d2['n_en'], d2['s_n'], d2['rtype_n'])
        ray['w_e'] = raymer.w_e(d2['n_en'], d2['w_en'])
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

        ret = ""
        ret += " RAYMER" + "\n" + " ------------------------------" + "\n"

        var = ['w_w', 'w_tail', 'w_f', 'w_ucm', 'w_ucn', 'w_n', 'w_e', 'w_enc', 'w_s', 'w_fs', 'w_fc', 'w_apui', 'w_instr', 'w_hydr', 'w_el', 'w_av', 'w_furn', 'w_ac', 'w_ai', 'w_hand']

        compvar = dict(zip(self.components, var))

        if cunit == True:
            k_ret = 1
            s_ret = "lb"
        else:
            k_ret = 0.453592
            s_ret = "kg"

        struct_group = ['wing', 'tail', 'fuselage', 'nacelle', 'landing main', 'landing nose']
        prop_group = ['engine', 'engine controls', 'pneumatic', 'fuel system']
        equip_group = ['flight controls', 'APU', 'instruments', 'hydraulics', 'electrical', 'avionics', 'furnishing', 'air conditioning', 'anti-icing', 'handling gear']

        flag_struct = True
        flag_prop = True
        flag_equip = True

        for component in self.components:
            if self.cb_dict[component].GetValue() == True:
                if component in struct_group:
                    if flag_struct == True:
                        ret += " STRUCTURES GROUP\n"
                        flag_struct = False
                if component in prop_group:
                    if flag_prop == True:
                        ret += " PROPULSION GROUP\n"
                        flag_prop = False
                if component in equip_group:
                    if flag_equip == True:
                        ret += " EQUIPMENT GROUP\n"
                        flag_equip = False

                ret += "\t " + component + " (" + compvar[component] + ")" + ": " + str(round(k_ret*ray[reference[component]], 2)) + " " + s_ret + "\n"
            else:
                del ray[compvar[component]]

        if self.cb_dict[component].GetValue() == True:
            ret += " ..................................\n" + " TOTAL: " + str(round(k_ret*sum(ray.values()), 2)) + " " + s_ret + "\n\n"

        return ret, ray

    def load_xml(self, d2):
        utype = ['allmoving', 'other', 'conv', 'ttail', 'fuselage', 'nocargo', 'onecargo', 'twocargo', 'clam', 'cargoclam', 'pylon', 'kneeling', 'reciprocating', 'turboprop']

        ltype = ['All-moving', 'Other', 'Conventional', 'T-tail', 'Fuselage-mounted main landing gear', 'No cargo door', 'Single side cargo', 'Double side cargo', 'Aft clamshell', 'Double side + aft clamshell', 'Pylon-mounted', 'Kneeling gear', 'Reciprocating', 'Turboprop']

        type_too = dict(zip(utype, ltype))

        ktype = ['rtype_htail', 'rtype_vtail', 'rtype_f1', 'rtype_f2', 'rtype_n', 'rtype_ucm', 'rtype_ucn', 'rtype_instr1', 'rtype_instr2']

        mtype = ['htail type', 'vtail type', 'fuselage door type', 'fuselage type', 'nacelle type', 'main type', 'nose type', 'engine type', 'aircraft type']

        type_moo = dict(zip(ktype, mtype))

        for key, value in d2.iteritems():
            if 'rtype' in key:
                self.rtype[type_moo[key]].SetValue((type_too[value]))
            else:
                self.tc_dict[key].SetValue(str(value))

    def select_all(self, evt):
        label = evt.GetEventObject().GetValue()

        if label:
            for key, value in self.cb_dict.iteritems():
                value.SetValue(True)
        else:
            for key, value in self.cb_dict.iteritems():
                value.SetValue(False)

####################################################################
####################################################################

class TabGeneralDynamics(wx.ScrolledWindow):
    def __init__(self, parent):
        """"""
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(5,15)

        self.init_tab()


    def init_tab(self):
        self.parameters = ['marker', 'line', 'w_to', 'n_ult', 'marker', 'line', 'a', 'lambda', 'Lambda_12', 'm_h', 's', 't_cm', 'marker', 'line', 'a_v', 'b_h', 'b_v', 'c', 'lambda_v', 'Lambda_14v', 'l_h', 'l_v', 's_h', 's_r', 's_v', 't_rh', 'z_h', 'marker', 'line', 'fuselage type','h_f', 'l_f', 'q_d', 'marker', 'line', 'nacelle type','a_in', 'l_n', 'n_inl', 'p_2', 'marker', 'line', 'engine controls type', 'engine s.s. type','n_e', 'w_eng', 'marker', 'line', 'duct type', 'air induction type', 'a_inl', 'l_d', 'marker', 'line', 'fuel system type', 'fuel type', 'w_f', 'w_supp', 'marker', 'line', 'b', 'marker', 'line', 'k_hydr', 'marker', 'line', 'w_fs', 'w_iae',  'marker', 'line', 'n_pil', 'marker', 'line', 'baggage type', 'n_cr', 'n_pax', 'v_pax', 'marker', 'line', 'k_apu', 'marker', 'line', 'furnishing type', 'n_cc', 'n_fdc', 'p_c', 'marker', 'line', 'k_pt']


        self.components = ['wing', 'tail', 'fuselage', 'nacelle', 'landing gear', 'air induction', 'engine', 'fuel system', 'engine controls', 'engine starting system', 'flight controls', 'hydraulic/pneumatic', 'electrical', 'instr./avio./elec.', 'AC/pressure/anti-ice', 'oxygen system', 'APU', 'furnishing', 'baggage', 'auxiliary gear', 'paint']

        tooltip = ['Takeoff weight', 'Ultimate load factor', 'Aspect ratio (typically 4-12)', 'Taper ratio', 'Sweepback angle at 50% chord', 'Maximum Mach number at sealevel (typically 0.4-0.8)', 'Wing area', 'Airfoil thickness ratio (typically 0.08-0.15)', 'Vertical tail aspect ratio', 'Horizontal tail span', 'Vertical tail span', 'Chord length (?)', 'Vertical tail taper ratio', 'Vertical tail sweep at 25% MAC', 'Distance from wing c/4 to horizontal tail c_h/4', 'Distance from wing c/4 to vertical tail c_v/4', 'Horizontal tail area', 'Rudder area', 'Vertical tail area', 'Horizontal tail thickness root', 'Distance from the vertical tail root to where the horizontal tail is mounted on the vertical tail; = 0 for fuselage mounted horizontal tails', 'Fuselage height', 'Fuselage length', 'Design dive dynamic pressure', 'Capture area per inlet', 'Nacelle length from inlet lip to compressor face', 'Number of inlets', 'Maximum static pressure at engine compressor face (typically 15-50)', 'Number of engines', 'Weight per engine', 'Capture area per inlet', 'Duct length', 'Mission fuel weight (includes reserves)', 'Bladder support structure weight', 'Wing span', 'Typically 0.0060-0.0120', 'Fuel system weight', 'Instrumentation, avionics and electronics weight', 'Number of pilots', 'Number of crew', 'Number of passengers', 'Passenger cabin volume', 'Typically 0.004-0.013', 'TODO', 'TODO', 'Design ultimate cabin pressure', 'Typically 0.003-0.006']

        hbox = wx.BoxSizer(wx.VERTICAL)

        stxt0 = wx.StaticText(self, label='Components')
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        stxt0.SetFont(font)
        line0 = wx.StaticLine(self)
        hbox.Add(stxt0, 0, wx.ALL, 5)
        hbox.Add(line0, 1, wx.ALL|wx.EXPAND, 5)

        self.cball = wx.CheckBox(self, label='(de)select all')
        hbox.Add(self.cball, 0)
        self.Bind(wx.EVT_CHECKBOX, self.select_all, self.cball)

        self.cb_dict = {}
        # component checkboxes

        gs = wx.GridSizer(8, 3, 0, 0)
        for item in self.components:
            cb = wx.CheckBox(self, label=item)
            gs.Add(cb, 0, wx.ALIGN_LEFT)
            self.cb_dict[item] = cb

        hbox.Add(gs, 0)

        # component list
        comp_title = ['General', 'Wing', 'Tail', 'Fuselage', 'Nacelle', 'Engine,...', 'Air induction,...', 'Fuel system', 'Propulsion', 'Hydraulics', 'Electrical','Instruments', 'Air-donditioning', 'Auxiliary power', 'Furnishing', 'Paint']

        units_im = ['lb', '', '', '', 'deg', '', 'ft^2', '', 'ft', 'ft', 'ft', 'ft', '', 'deg', 'ft', 'ft', 'ft^2', 'ft^2', 'ft^2', 'ft', 'ft', 'ft', 'ft', 'psf', 'ft^2', 'ft', '', 'psi', '', 'lb', 'ft^2', 'ft', 'lb', 'lb',  'ft', '', 'lb', 'lb', '', '', '', '', '', '', '', 'psi', '', '']

        units_si = ['kg', '', '', '', 'rad', '', 'm^2', '', 'm', 'm', 'm', 'm', '', 'rad', 'm', 'm', 'm^2', 'm^2', 'm^2', 'm', 'm', 'm', 'm', '', 'm^2', 'm', '', '', '', 'kg', 'm^2', 'm', 'kg', 'kg',  'm', '', 'kg', 'kg', '', '', '', '', '', '', '', '', '']


        fuselage_type = ['Inlets in', 'Inlets elsewhere']
        nacelle_type = ['Turbojet', 'Turbofan']
        ai1_type = ['Flat cross sections', 'Curved cross sections']
        ai2_type = ['M_D below 1.4', 'M_D above 1.4']
        fs1_type = ['Self-sealing bladder cells', 'Non-self sealing bladder cells']
        fs2_type = ['Aviation gasoline', 'JP-4']
        ec_type = ['Non-afterburning', 'Afterburnig', 'Jet', 'Turboprops', 'Piston']
        ess_type = ['Single/double jet engine', 'Four or more jet engine', 'Electric', 'Turboprop, pneumatic', 'Piston']
        fur_type = ['Business', 'Short', 'Long']
        bc_type = ['Without preload provisions', 'With preload provisions']

        combo_type = [fuselage_type, nacelle_type, ec_type, ess_type, ai1_type, ai2_type, fs1_type, fs2_type, bc_type, fur_type]

        sizer = wx.GridBagSizer(0, 0)
        j = 0 # 'comp' list index
        k = 0 # 'combo_type' list index
        m = 0 # 'units_im' list index
        n = 0 # 'units_si' list index
        z = 0 # tooltip list index
        self.par_extra = [] # list for units parameters
        self.tc_dict = {} # dict of TextCtrl
        self.gtype = {} # dict of comboboxes
        self.rb_im = {} # dict of radiobuttons 'im'
        self.rb_si = {} # dict of radiobuttons 'si'

        for i, item in enumerate(self.parameters):
            if item == 'marker':
                comp_name = wx.StaticText(self, label=comp_title[j])
                font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
                comp_name.SetFont(font)
                j += 1
                sizer.Add(comp_name, pos=(i,0), flag=wx.TOP, border=10)
            elif item == 'line':
                line = wx.StaticLine(self)

                sizer.Add(line, pos=(i,0), span=(1,5), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)
            elif 'type' in item:
                combo = wx.ComboBox(self, choices=combo_type[k], style=wx.CB_READONLY)
                combo_title = wx.StaticText(self, label=item)
                self.gtype[item] = combo
                sizer.Add(combo, pos=(i,2))
                sizer.Add(combo_title, pos=(i, 0))
                k += 1
            else:
                par = wx.StaticText(self, label=item)
                tc = wx.TextCtrl(self, wx.ID_ANY, "")
                self.tc_dict[item] = tc

                start_icon = wx.Image('icon.png')
                start_icon.Rescale(20, 20)
                almost_icon = wx.BitmapFromImage(start_icon)
                icon = wx.StaticBitmap(self, -1, almost_icon, wx.DefaultPosition, style=wx.BITMAP_TYPE_PNG)
                icon.SetToolTip(wx.ToolTip(tooltip[z]))
                z += 1

                sizer.Add(par, pos=(i,0))
                sizer.Add(tc, pos=(i,2))
                sizer.Add(icon, pos=(i,1), flag=wx.RIGHT, border=10)
                if units_im[m] == '':
                    m += 1
                    n += 1
                    continue
                else:
                    rb1 = wx.RadioButton(self, label=units_im[m], style=wx.RB_GROUP)
                    sizer.Add(rb1, pos=(i,3))
                    self.rb_im[item] = rb1
                    self.par_extra.append(item)
                    m += 1
                    if units_si[n] == '':
                        filler = wx.StaticText(self, label='')
                        sizer.Add(filler, pos=(i,4))
                        n += 1
                    else:
                        rb2 = wx.RadioButton(self, label=units_si[n])
                        sizer.Add(rb2, pos=(i,4))
                        self.rb_si[item] = rb2
                        n += 1

        hbox.Add(sizer, 0, wx.ALL, 5)
        self.SetSizer(hbox)

    def calculate_weight(self, cunit):

        d3 = {}

        for key, value in self.tc_dict.iteritems():
            if value.GetValue() is not u'':
                if key in self.par_extra:
                    if self.rb_im[key].GetValue() == True:
                        k = 1
                    else:
                        if self.rb_im[key].GetLabel() == 'lb':
                            k = 2.20462
                        elif self.rb_im[key].GetLabel() == 'ft':
                            k = 3.28084
                        elif self.rb_im[key].GetLabel() == 'ft^2':
                            k = 10.7639
                        elif self.rb_im[key].GetLabel() == 'deg':
                            k = 57.2957795
                        else:
                            k = 1
                            print "[INFO]: key %r not specified." % key
                else:
                    k = 1
            d3[key] = k*float(value.GetValue())


        for key, value in self.gtype.iteritems():
            ret = value.GetValue()
            if key == 'fuselage type':
                if ret == 'Inlets in':
                    d3['gtype_f'] = 'in'
                elif ret == 'Inlets elsewhere':
                    d3['gtype_f'] = 'out'
            elif key == 'nacelle type':
                if ret == 'Turbojet':
                    d3['gtype_n'] = 'turbojet'
                elif ret == 'Turbofan':
                    d3['gtype_n'] = 'turbofan'
            elif key == 'engine controls type':
                if ret == 'Non-afterburning':
                    d3['gtype_ec'] = 'rootnoafter'
                elif ret == 'Afterburning':
                    d3['gtype_ec'] = 'rootafter'
                elif ret == 'Jet':
                    d3['gtype_ec'] = 'jet'
                elif ret == 'Turboprops':
                    d3['gtype_ec'] = 'turboprops'
                elif ret == 'Piston':
                    d3['gtype_ec'] = 'piston'
            elif key == 'engine s.s. type':
                if ret == 'Single/double jet engine':
                    d3['gtype_ess'] = 'jetcp'
                elif ret == 'Four or more jet engine':
                    d3['gtype_ess'] = 'jetp'
                elif ret == 'Electric':
                    d3['gtype_ess'] = 'jete'
                elif ret == 'Turboprop, pneumatic':
                    d3['gtype_ess'] = 'turboprop'
                elif ret == 'Piston':
                    d3['gtype_ess'] = 'piston'
            elif key == 'duct type':
                if ret == 'Flat cross sections':
                    d3['gtype_ai1'] = 'flat'
                elif ret == 'Curved cross sections':
                    d3['gtype_ai1'] = 'curved'
            elif key == 'air induction type':
                if ret == 'M_D below 1.4':
                    d3['gtype_ai2'] = 'belowmd'
                elif ret == 'M_D above 1.4':
                    d3['gtype_ai2'] = 'abovemd'
            elif key == 'fuel system type':
                if ret == 'Self-sealing bladder cells':
                    d3['gtype_fs1'] = 'self'
                elif ret == 'Non-self sealing bladder cells':
                    d3['gtype_fs1'] = 'nonself'
            elif key == 'fuel type':
                if ret == 'Aviation gasoline':
                    d3['gtype_fs2'] = 'aviation'
                elif ret == 'JP-4':
                    d3['gtype_fs2'] = 'jp4'
            elif key == 'baggage type':
                if ret == 'Without preload provisions':
                    d3['gtype_bc'] = 'no'
                elif ret == 'With preload provisions':
                    d3['gtype_bc'] = 'yes'
            elif key == 'furnishing type':
                if ret == 'Business':
                    d3['gtype_fur'] = 'business'
                elif ret == 'Short':
                    d3['gtype_fur'] = 'short'
                elif ret == 'Long':
                    d3['gtype_fur'] = 'long'
            else:
                print "ERROR"

        gendyn = methods.Gd()
        gd = {}

        weights = ['w_w', 'w_tail', 'w_f', 'w_n', 'w_g', 'w_ai', 'w_e', 'w_fs', 'w_ec', 'w_ess', 'w_fc', 'w_hydr', 'w_els', 'w_i', 'w_api', 'w_ox', 'w_apu', 'w_fur', 'w_bc', 'w_aux', 'w_pt']

        # dictionary of weights and components
        reference = {}
        for i, weight in enumerate(weights):
            reference[self.components[i]] = weight

        gd['w_w'] = gendyn.w_w(d3['s'], d3['a'], d3['m_h'], d3['w_to'], d3['n_ult'], d3['lambda'], d3['t_cm'], d3['Lambda_12'])
        gd['w_tail'] = gendyn.w_h(d3['w_to'], d3['n_ult'], d3['s_h'], d3['b_h'], d3['t_rh'], d3['c'], d3['l_h']) + gendyn.w_v(d3['z_h'], d3['b_v'], d3['w_to'], d3['n_ult'], d3['s_v'], d3['m_h'], d3['l_v'], d3['s_r'], d3['a_v'], d3['lambda_v'], d3['Lambda_14v'])
        gd['w_f'] = gendyn.w_f(d3['q_d'], d3['w_to'], d3['l_f'], d3['h_f'], d3['gtype_f'])
        gd['w_n'] = gendyn.w_n(d3['n_inl'], d3['a_in'], d3['l_n'], d3['p_2'], d3['gtype_n'])
        gd['w_g'] = gendyn.w_g(d3['w_to'])
        gd['w_e'] = gendyn.w_e(d3['n_e'], d3['w_eng'])
        gd['w_ai'] = gendyn.w_ai(d3['n_inl'], d3['l_d'], d3['a_inl'], d3['p_2'], d3['gtype_ai1'], d3['gtype_ai2'])
        gd['w_fs'] = gendyn.w_fs(d3['w_f'], d3['w_supp'], d3['gtype_fs1'], d3['gtype_fs2'])
        gd['w_ec'] = gendyn.w_ec(d3['l_f'], d3['n_e'], d3['gtype_ec'], d3['b'])
        gd['w_ess'] = gendyn.w_ess(gd['w_e'], d3['gtype_ess'])
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

        ret = ""
        ret += " GENERAL DYNAMICS" + "\n" + " ------------------------------" + "\n"

        var = ['w_w', 'w_tail', 'w_f', 'w_n', 'w_g', 'w_ai', 'w_e', 'w_fs', 'w_ec', 'w_ess', 'w_fc', 'w_hydr', 'w_els', 'w_i', 'w_api', 'w_ox', 'w_apu', 'w_fur', 'w_bc', 'w_aux', 'w_pt']

        compvar = dict(zip(self.components, var))

        if cunit == True:
            k_ret = 1
            s_ret = "lb"
        else:
            k_ret = 0.453592
            s_ret = "kg"

        struct_group = ['wing', 'tail', 'fuselage', 'nacelle', 'landing gear', 'air induction']
        prop_group = [ 'engine', 'fuel system', 'engine controls', 'engine starting system']
        equip_group = ['flight controls', 'hydraulic/pneumatic', 'electrical', 'instr./avio./elec.', 'AC/pressure/anti-ice', 'oxygen system', 'APU', 'furnishing', 'baggage', 'auxiliary gear', 'paint']

        flag_struct = True
        flag_prop = True
        flag_equip = True

        for component in self.components:
            if self.cb_dict[component].GetValue() == True:
                if component in struct_group:
                    if flag_struct == True:
                        ret += " STRUCTURES GROUP\n"
                        flag_struct = False
                if component in prop_group:
                    if flag_prop == True:
                        ret += " PROPULSION GROUP\n"
                        flag_prop = False
                if component in equip_group:
                    if flag_equip == True:
                        ret += " EQUIPMENT GROUP\n"
                        flag_equip = False

                ret += "\t " + component + " (" + compvar[component] + ")" + ": " + str(round(k_ret*gd[reference[component]], 2)) + " " + s_ret +  "\n"
            else:
                del gd[compvar[component]]

        if self.cb_dict[component].GetValue() == True:
            ret += " ..................................\n" + " TOTAL: " + str(round(k_ret*sum(gd.values()), 2)) + " " + s_ret + "\n\n"

        return ret, gd

    def load_xml(self, d3):
        utype = ['in', 'out', 'turbojet', 'turbofan', 'rootnoafter', 'rootafter', 'jet', 'turboprops', 'piston', 'jetcp', 'jetp', 'jete', 'turboprop', 'flat', 'curved', 'belowmd', 'abovemd', 'below', 'above', 'self', 'nonself', 'aviation', 'jp4', 'no', 'yes', 'business', 'short', 'long']

        ltype = ['Inlets in', 'Inlets elsewhere', 'Turbojet', 'Turbofan', 'Non-afterburning', 'Afterburning', 'Jet', 'Turboprop', 'Piston', 'Single/double jet engine', 'Four or more jet engine', 'Electric', 'Turboprop, pneumatic', 'Flat cross sections', 'Curved cross sections', 'M_D below 1.4', 'M_D above 1.4', 'Below 1,500 shp', 'Above 1,500 shp', 'Self-sealing bladder cells', 'Non-self sealing bladder cells', 'Aviation gasoline', 'JP-4', 'Without preload provisions', 'With preload provisions', 'Business', 'Short', 'Long']

        type_too = dict(zip(utype, ltype))

        ktype = ['gtype_f', 'gtype_n', 'gtype_ai1', 'gtype_ai2', 'gtype_prop', 'gtype_fs1', 'gtype_fs2', 'gtype_ec', 'gtype_ess', 'gtype_pc', 'gtype_fur', 'gtype_bc']

        mtype = ['fuselage type', 'nacelle type', 'duct type', 'air induction type', 'propeller type', 'fuel system type', 'fuel type', 'engine controls type', 'engine s.s. type', 'propeller controls type', 'furnishing type', 'baggage type']

        type_moo = dict(zip(ktype, mtype))

        for key, value in d3.iteritems():
            if 'gtype' in key:
                self.gtype[type_moo[key]].SetValue((type_too[value]))
            else:
                self.tc_dict[key].SetValue(str(value))

    def select_all(self, evt):
        label = evt.GetEventObject().GetValue()

        if label:
            for key, value in self.cb_dict.iteritems():
                value.SetValue(True)
        else:
            for key, value in self.cb_dict.iteritems():
                value.SetValue(False)


####################################################################
###################################################################


class DemoFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Weviation")

        self.Maximize(True)

        # menubar
        EXPORT = wx.NewId()
        EXPORT_XML = wx.NewId()
        EXPORT_TXT = wx.NewId()
        LOAD_XML = wx.NewId()

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()

        fileMenu.Append(LOAD_XML, '&Load XML file')
        imp = wx.Menu()
        imp.Append(EXPORT_XML, 'Export as &XML file')
        imp.Append(EXPORT_TXT, 'Export as &text file')
        fileMenu.AppendMenu(EXPORT, '&Export', imp)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.load_button, id=LOAD_XML)
        self.Bind(wx.EVT_MENU, self.export_button, id=EXPORT_XML)
        self.Bind(wx.EVT_MENU, self.export_text, id=EXPORT_TXT)

        self.panel = wx.Panel(self)

        # tabs
        self.notebook = wx.Notebook(self.panel)

        self.tabOne = TabTorenbeek(self.notebook)
        self.notebook.AddPage(self.tabOne, "Torenbeek")

        self.tabTwo = TabRaymer(self.notebook)
        self.notebook.AddPage(self.tabTwo, "Raymer")

        self.tabThree = TabGeneralDynamics(self.notebook)
        self.notebook.AddPage(self.tabThree, "General Dynamics")

        # calculate button
        btnCalc = wx.Button(self.panel, label='Calculate', size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.calculate_button, btnCalc)

        # method checkbox
        self.cb_tor = wx.CheckBox(self.panel, label='Torenbeek')
        self.cb_ray = wx.CheckBox(self.panel, label='Raymer')
        self.cb_gd = wx.CheckBox(self.panel, label='General Dynamics')

        # clear button
        btnClear = wx.Button(self.panel, label='Clear', size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.clear_button, btnClear)

        # unit button
        self.rb_lb = wx.RadioButton(self.panel, label='lb', style=wx.RB_GROUP)
        self.rb_kg = wx.RadioButton(self.panel, label='kg')

        # data output window
        self.txt1 = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE|wx.TE_READONLY)

        # pie chart tabs
        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.notebook2 = wx.Notebook(self.panel)

        self.tabTor = wx.Panel(self.notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bsizer0 = wx.BoxSizer(wx.VERTICAL)
        self.tabTor.SetSizer(bsizer0)
        self.tabTor.Layout()
        bsizer0.Fit(self.tabTor)
        self.notebook2.AddPage(self.tabTor, "Torenbeek")

        self.tabRay = wx.Panel(self.notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bsizer1 = wx.BoxSizer(wx.VERTICAL)
        self.tabRay.SetSizer(bsizer1)
        self.tabRay.Layout()
        bsizer1.Fit(self.tabRay)
        self.notebook2.AddPage(self.tabRay, "Raymer")

        self.tabGd = wx.Panel(self.notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bsizer2 = wx.BoxSizer(wx.VERTICAL)
        self.tabGd.SetSizer(bsizer2)
        self.tabGd.Layout()
        bsizer2.Fit(self.tabGd)
        self.notebook2.AddPage(self.tabGd, "General Dynamics")

        # bar chart
        self.notebook3 = wx.Notebook(self.panel)

        self.tabBar = wx.Panel(self.notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bsizer3 = wx.BoxSizer(wx.VERTICAL)
        self.tabBar.SetSizer(bsizer3)
        self.tabBar.Layout()
        bsizer3.Fit(self.tabBar)
        self.notebook3.AddPage(self.tabBar, "Bar chart")


        # adding stuff
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)

        hbox0.Add(btnCalc)
        hbox0.Add(self.rb_lb)
        hbox0.Add(self.rb_kg)
        #hbox0.Add(btnLoad)
        #hbox0.Add(btnExport)
        hbox0.Add(self.cb_tor)
        hbox0.Add(self.cb_ray)
        hbox0.Add(self.cb_gd)
        vbox0.Add(hbox0)

        self.vbox1.Add(self.notebook2, 1, wx.ALL|wx.EXPAND, 5)
        self.vbox1.Add(self.notebook3, 1, wx.ALL|wx.EXPAND, 5)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.txt1, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(btnClear)
        vbox2.Add(hbox1)

        sizer.Add(vbox0, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(vbox2, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.vbox1, 1, wx.ALL|wx.EXPAND, 5)

        self.panel.SetSizer(sizer)

        self.Layout()
        self.Centre()
        self.Show()

    def calculate_button(self, evt):
        label = evt.GetEventObject().GetLabel()
        self.tor = None
        self.ray = None
        self.gd = None

        self.ret_tor = None
        self.ret_ray = None
        self.ret_gd = None

        if label == 'Calculate':

            flag_info = True
            self.ret_info = " INFORMATION\n" + "------------------------------\n" + " manufacturer: " + self.info['manufacturer'] + "\n" + " type: " + self.info['type'] + "\n" + " model: " + self.info['model'] + "\n" + " initial service date: " + self.info['sdate'] + "\n\n"


            if self.cb_tor.GetValue() == True:
                if flag_info == True:
                    self.txt1.AppendText(self.ret_info)
                    flag_info = False
                self.ret_tor, self.tor = self.tabOne.calculate_weight(self.rb_lb.GetValue())
                self.txt1.AppendText(self.ret_tor)
                self.piechart(self.tabTor, self.tor)
            else:
                self.ret_tor = None

            if self.cb_ray.GetValue() == True:
                if flag_info == True:
                    self.txt1.AppendText(self.ret_info)
                    flag_info = False
                self.ret_ray, self.ray = self.tabTwo.calculate_weight(self.rb_lb.GetValue())
                self.txt1.AppendText(self.ret_ray)
                self.piechart(self.tabRay, self.ray)
            else:
                self.ret_ray = None

            if self.cb_gd.GetValue() == True:
                if flag_info == True:
                    self.txt1.AppendText(self.ret_info)
                    flag_info = False
                self.ret_gd, self.gd = self.tabThree.calculate_weight(self.rb_lb.GetValue())
                self.txt1.AppendText(self.ret_gd)
                self.piechart(self.tabGd, self.gd)
            else:
                self.ret_ray = None

            self.barchart(self.tabBar, self.tor, self.ray, self.gd)

            self.Layout()
            self.Fit()
            self.Update()
            #self.Refresh()

    def clear_button(self, evt):
        self.txt1.SetValue("")
        self.ret_tor = None
        self.ret_ray = None
        self.ret_gd = None


    def export_button(self, evt):
        root = ET.Element("output")

        info = ET.SubElement(root, "info")
        for key, value in self.info.iteritems():
            item = ET.SubElement(info, key)
            item.text = value

        if self.tor != None:
            torenbeek = ET.SubElement(root, "torenbeek")
            for key, value in self.tor.iteritems():
                item = ET.SubElement(torenbeek, key)
                item.text = str(round(value, 2))

        if self.ray != None:
            raymer = ET.SubElement(root, "raymer")
            for key, value in self.ray.iteritems():
                item = ET.SubElement(raymer, key)
                item.text = str(round(value, 2))

        if self.gd != None:
            gd = ET.SubElement(root, "general_dynamics")
            for key, value in self.gd.iteritems():
                item = ET.SubElement(gd, key)
                item.text = str(round(value, 2))

        tree = ET.ElementTree(root)
        tree.write("output.xml", pretty_print=True)

        with open("output.xml", 'r+') as f:
            content = f.read()
            f.seek(0,0)
            if self.rb_lb.GetValue() == True:
                unit = 'lb'
            else:
                unit = 'kg'

            line = "<!-- Output of the weight estimation method(s), in " + unit + ". -->"
            f.write(line.rstrip('\r\n') + '\n\n' + content)

        dial = wx.MessageDialog(None, 'Export completed', 'Info', wx.OK)
        dial.ShowModal()


    def export_text(self, evt):
        try:
            os.remove("output.txt")
        except OSError:
            pass

        with open("output.txt", 'w') as f:
            f.write(self.ret_info)

        if self.ret_tor != None:
            with open("output.txt", 'a') as f:
                f.write(self.ret_tor)

        if self.ret_ray != None:
            with open("output.txt", 'a') as f:
                f.write(self.ret_ray)

        if self.ret_gd != None:
            with open("output.txt", 'a') as f:
                f.write(self.ret_gd)

        dial = wx.MessageDialog(None, 'Export completed', 'Info', wx.OK)
        dial.ShowModal()




    def piechart(self, panel, rc):
        self.rc = rc

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(panel, -1, self.figure)
        labels = self.rc.keys()
        sizes = self.rc.values()
        cs=cm.Set1(np.arange(len(labels))/float(len(labels)))
        self.axes.pie(sizes, colors=cs, autopct='%.2f%%')
        self.axes.axis('equal')
        fontP = FontProperties()
        fontP.set_size('small')
        #self.axes.legend(labels, loc=2)
        #self.axes.legend(labels, loc=9, bbox_to_anchor=(0.5, -0.1))
        self.axes.legend(labels, prop=fontP , bbox_to_anchor=(0.05, 1))
        #sizer = panel.GetSizer()
        #sizer = self.tabTor
        #sizer.Add(self.canvas)

        #self.Layout()


    def barchart(self, panel,  tor, ray, gd):
        a = []

        if self.rb_lb.GetValue() == True:
            unit = 'lb'
            k_unit = 1
        else:
            unit = 'kg'
            k_unit = 0.453592

        if tor != None:
            tot_tor = k_unit*sum(tor.values())
            a.append(tot_tor)
        if ray != None:
            tot_ray = k_unit*sum(ray.values())
            a.append(tot_ray)
        if gd != None:
            tot_gd = k_unit*sum(gd.values())
            a.append(tot_gd)

        x = range(len(a))

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(panel, -1, self.figure)
        barlist = self.axes.bar(x, a, align='center')

        lbl = ['Torenbeek', 'Raymer', 'General Dynamics']
        self.axes.set_ylabel('Estimated weight [' + unit + ']')
        self.axes.set_xticks(x, lbl)

        c = ['r', 'g', 'b']

        for i, item in enumerate(a):
            barlist[i].set_color(c[i])


    def load_button(self, evt):
        d1, d2, d3, self.info = p.parse_xml()
        self.tabOne.load_xml(d1)
        self.tabTwo.load_xml(d2)
        self.tabThree.load_xml(d3)


if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame()
    app.MainLoop()
