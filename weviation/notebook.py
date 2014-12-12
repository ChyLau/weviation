import wx
import methods
import parse as p

class TabPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        """"""
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(5,15)

        self.init_tab()


    def init_tab(self):
        self.parameters = ['marker', 'line', 'w_g', 'w_to', 'marker', 'line','b_ref', 'Lambda', 'b', 'n_ult', 's_w', 't_r', 'marker', 'line', 'htail type', 'vtail type', 's_v', 's_h', 'Lambda_h', 'Lambda_v', 'marker', 'line', 'fuselage type', 'v_d', 'l_t', 'b_f', 'h_f', 's_g', 'marker', 'line', 'p_to', 'marker', 'line', 'main type', 'nose type', 'a_m', 'b_m', 'c_m', 'd_m', 'a_n', 'b_n', 'c_n', 'd_n', 'marker', 'line', 'surface controls type', 'n_e', 'w_e', 'marker', 'line', 'w_fto', 'marker', 'line', 'air induction type', 'l_d', 'n_i', 'a_i', 'marker', 'line', 'ax', 't_to', 'marker', 'line', 'n_ft', 'v_ft', 'marker', 'line', 'v_wt', 'marker', 'line', 'n_p','b_p','d_p', 'marker', 'line', 'w_ba', 'marker', 'line', 'w_de','r_d', 'marker', 'line', 'hydr./elec. type', 'p_el','marker', 'line', 'l_pax', 'marker', 'line', 'oxygen type', 'n_pax', 'marker','line', 'w_zf']

        self.components = ['wing', 'tail', 'fuselage', 'nacelle', 'landing main', 'landing nose', 'surface controls', 'engine', 'accessory', 'air induction', 'exhaust', 'oil/cooler', 'fuel system', 'water injection', 'propeller installation', 'thrust reversers', 'APU', 'instruments', 'hydraulic/lectrical', 'AC/pressure/anti-ice', 'oxygen system', 'furnishing']

        hbox = wx.BoxSizer(wx.VERTICAL)

        stxt0 = wx.StaticText(self, label='Components')
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        stxt0.SetFont(font)
        line0 = wx.StaticLine(self)
        hbox.Add(stxt0, 0, wx.ALL, 5)
        hbox.Add(line0, 1, wx.ALL|wx.EXPAND, 5)

        vbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.cball = wx.CheckBox(self, label='(de)select all')
        hbox.Add(self.cball, 0)
        self.Bind(wx.EVT_CHECKBOX, self.select_all, self.cball)

        self.cb_dict = {}
        # component checkboxes
        for item in self.components:
            cb = wx.CheckBox(self, label=item)
            vbox0.Add(cb, 0)
            self.cb_dict[item] = cb

        hbox.Add(vbox0, 0)

        # component list
        comp_title = ['General', 'Wing', 'Tail', 'Fuselage', 'Nacelle,..', 'Landing gear,..', 'Engine,..', 'Accessory', 'Air induction', 'Exhaust', 'Fuel system', 'Water injection', 'Propeller installation', 'APU', 'Instruments, ...', 'Electrical', 'Air conditioning', 'Oxygen system', 'Furnishing']

        units_im = ['marker', 'line', 'lb', 'lb', 'marker', 'line', 'ft', 'deg', 'ft', '', 'ft^2', 'ft', 'marker', 'line',  '', '', 'ft^2', 'ft^2', 'deg', 'deg', 'marker', 'line', '', 'kts', 'ft', 'ft', 'ft', 'ft^2', 'marker', 'line', 'hp', 'marker', 'line', '', '', '', '', '', '', '', '', '', '', 'marker', 'line', '', '', 'lb', 'marker', 'line', '', 'marker', 'line', '', 'ft', '', 'ft^2', 'marker', 'line', 'ft^2', 'N', 'marker', 'line', '', 'gal', 'marker', 'line', 'gal', 'marker', 'line', '', 'ft', '', 'marker', 'line',  '', 'marker', 'line', 'lb', 'ft', 'marker', 'line', '', 'W', 'marker', 'line', 'ft', 'marker', 'line', '', '', 'marker', 'line', 'ft']

        units_im = ['lb', 'lb', 'ft', 'deg', 'ft', '', 'ft^2', 'ft', 'ft^2', 'ft^2', 'deg', 'deg', 'kts', 'ft', 'ft', 'ft', 'ft^2', 'hp', '', '', '', '', '', '', '', '', '', 'lb', '', 'ft', '', 'ft^2', 'ft^2', 'N', '', 'gal', 'gal', '', 'ft', '',  '', 'lb', 'ft', 'W', 'ft', '', 'ft']

        units_si = ['kg', 'kg', 'm', 'rad', 'm', '', 'm^2', 'm', 'm^2', 'm^2', 'rad', 'rad', 'm/s', 'm', 'm', 'm', 'm^2', '', '', '', '', '', '', '', '', '', '', 'kg', '', 'm', '', 'm^2', 'm^2', '', '', 'L', 'L', '', 'm', '',  '', 'kg', 'm', '', 'm', '', 'm']




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
        self.par_extra = [] # list for units parameters
        self.tc_dict = {} # dict of TextCtrl
        self.ttype = {} # dict of comboboxes
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
                sizer.Add(line, pos=(i,0), span=(1,2), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)
            elif 'type' in item:
                combo = wx.ComboBox(self, choices=combo_type[k], style=wx.CB_READONLY)
                combo_title = wx.StaticText(self, label=item)
                self.ttype[item] = combo
                sizer.Add(combo, pos=(i,1))
                sizer.Add(combo_title, pos=(i, 0))
                k += 1
            else:
                par = wx.StaticText(self, label=item)
                tc = wx.TextCtrl(self, wx.ID_ANY, "")
                self.tc_dict[item] = tc

                sizer.Add(par, pos=(i,0))
                sizer.Add(tc, pos=(i,1))
                if units_im[m] == '':
                    m += 1
                    n += 1
                    continue
                else:
                    rb1 = wx.RadioButton(self, label=units_im[m], style=wx.RB_GROUP)
                    sizer.Add(rb1, pos=(i,2))
                    self.rb_im[item] = rb1
                    self.par_extra.append(item)
                    m += 1
                    if units_si[n] == '':
                        filler = wx.StaticText(self, label='')
                        sizer.Add(filler, pos=(i,3))
                        n += 1
                    else:
                        rb2 = wx.RadioButton(self, label=units_si[n])
                        sizer.Add(rb2, pos=(i,3))
                        self.rb_si[item] = rb2
                        n += 1

        hbox.Add(sizer, 0, wx.ALL, 5)
        self.SetSizer(hbox)

    def calculate_weight(self):

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

        weights = ['w_w', 'w_tail', 'w_f', 'w_n', 'w_ucm', 'w_ucn', 'w_sc', 'w_eni', 'w_acc', 'w_airi', 'w_ext', 'w_oc', 'w_fsi', 'w_wis', 'w_pi', 'w_tr', 'w_apu', 'w_navp', 'w_heu', 'w_api', 'w_ox', 'w_fur']

        # dictionary of weights and components
        reference = {}
        for i, weight in enumerate(weights):
            reference[self.components[i]] = weight

        tor['w_w'] = torenbeek.w_w(d1['w_g'], d1['b_ref'], d1['Lambda'], d1['b'], d1['n_ult'], d1['s_w'], d1['t_r'], d1['tunit_w'])
        tor['w_tail'] = torenbeek.w_htail(d1['s_h'], d1['v_d'], d1['Lambda_h'], d1['ttype_htail']) + torenbeek.w_vtail(d1['s_v'], d1['v_d'], d1['Lambda_v'], d1['ttype_vtail'])
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

        ret = ""
        ret += "TORENBEEK" + "\n" + "------------------------------" + "\n"
        for component in self.components:
            if self.cb_dict[component].GetValue() == True:
                ret += component + ":      " + str(round(tor[reference[component]], 2)) + "\n"

        ret += "total:      " + str(round(sum(tor.values()), 2))
        return ret

    def load_xml(self, d1):
        for key, value in d1.iteritems():
            if 'tunit' not in key:
                if 'ttype' not in key:
                    self.tc_dict[key].SetValue(str(value))

    def select_all(self, evt):
        label = evt.GetEventObject().GetValue()

        if label:
            for key, value in self.cb_dict.iteritems():
                value.SetValue(True)
        else:
            for key, value in self.cb_dict.iteritems():
                value.SetValue(False)



class DemoFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Weviation",
                          size=(1200,800)
                          )

        panel = wx.Panel(self)

        # tabs
        notebook = wx.Notebook(panel)

        self.tabOne = TabPanel(notebook)
        notebook.AddPage(self.tabOne, "Torenbeek")

        self.tabTwo = TabPanel(notebook)
        notebook.AddPage(self.tabTwo, "Raymer")

        self.tabThree = TabPanel(notebook)
        notebook.AddPage(self.tabThree, "General Dynamics")

        # calculate button
        btnCalc = wx.Button(panel, label='Calculate', size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.calculate_button, btnCalc)

        # method checkbox
        self.cb_tor = wx.CheckBox(panel, label='Torenbeek')
        self.cb_ray = wx.CheckBox(panel, label='Raymer')
        self.cb_gd = wx.CheckBox(panel, label='General Dynamics')

        # load xml button
        btnLoad = wx.Button(panel, label='Load XML', size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.load_button, btnLoad)

        # data output window
        self.txt1 = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)


        # adding stuff
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)

        hbox0.Add(btnCalc)
        hbox0.Add(self.cb_tor)
        hbox0.Add(self.cb_ray)
        hbox0.Add(self.cb_gd)
        hbox0.Add(btnLoad)
        vbox0.Add(hbox0)

        sizer.Add(vbox0, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.txt1, 1, wx.ALL|wx.EXPAND, 5)

        panel.SetSizer(sizer)

        self.Layout()
        self.Centre()
        self.Show()

    def calculate_button(self, evt):
        label = evt.GetEventObject().GetLabel()

        if label == 'Calculate':
            if self.cb_tor.GetValue() == True:
                self.txt1.SetValue(self.tabOne.calculate_weight())

    def load_button(self, evt):
        label = evt.GetEventObject().GetLabel()

        if label == 'Load XML':
            d1, d2, d3 = p.parse_xml()
            self.tabOne.load_xml(d1)



if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame()
    app.MainLoop()
