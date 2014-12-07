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
        self.parameters = ['marker', 'line', 'w_g','b_ref', 'Lambda', 'b', 'n_ult', 's_w', 't_r', 'marker', 'line', 's_v', 's_h', 'Lambda_h', 'Lambda_v', 'marker', 'line', 'v_d', 'l_t', 'b_f', 'h_f', 's_g', 'marker', 'line', 'p_to', 'marker', 'line',  'a_m', 'b_m', 'c_m', 'd_m', 'a_n', 'b_n', 'c_n', 'd_n', 'w_to', 'marker', 'line', 'n_e', 'w_e', 'marker', 'line', 'w_fto', 'marker', 'line', 'l_d', 'n_i', 'a_i', 'marker', 'line', 'ax', 't_to', 'marker', 'line', 'n_ft', 'v_ft', 'marker', 'line', 'v_wt', 'marker', 'line', 'n_p','b_p','d_p', 'marker', 'line', 'w_ba', 'marker', 'line', 'w_de','r_d', 'marker', 'line', 'p_el','marker', 'line', 'l_pax', 'marker', 'line', 'n_pax', 'marker','line', 'w_zf']

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

        """
        self.cb_w = wx.CheckBox(self, label='wing')
        self.cb_t = wx.CheckBox(self, label='tail')
        self.cb_f = wx.CheckBox(self, label='fuselage')
        self.cb_n = wx.CheckBox(self, label='nacelle')
        self.cb_ucm = wx.CheckBox(self, label='landing main')
        self.cb_ucn = wx.CheckBox(self, label='landing nose')
        self.cb_sc = wx.CheckBox(self, label='surface controls')
        self.cb_eni = wx.CheckBox(self, label='engine')
        self.cb_acc = wx.CheckBox(self, label='accessory')
        self.cb_airi = wx.CheckBox(self, label='air induction')
        self.cb_ext = wx.CheckBox(self, label='exhaust')
        self.cb_oc = wx.CheckBox(self, label='oil/cooler')
        self.cb_fsi = wx.CheckBox(self, label='fuel system')
        self.cb_wis = wx.CheckBox(self, label='water injection')
        self.cb_pi = wx.CheckBox(self, label='propeller install.')
        self.cb_tr = wx.CheckBox(self, label='thrust reversers')
        self.cb_apu = wx.CheckBox(self, label='APU')
        self.cb_navp = wx.CheckBox(self, label='instruments')
        self.cb_heu = wx.CheckBox(self, label='hydraulic/electrical')
        self.cb_api = wx.CheckBox(self, label='AC/pressure/anti-ice')
        self.cb_ox = wx.CheckBox(self, label='oxygen system')
        self.cb_fur = wx.CheckBox(self, label='furnishing')
        """
        # component checkboxes list
        #self.cb_comp = [self.cb_w, self.cb_t, self.cb_f, self.cb_n, self.cb_ucm, self.cb_ucn, self.cb_sc, self.cb_eni, self.cb_acc, self.cb_airi, self.cb_ext, self.cb_oc, self.cb_fsi, self.cb_wis, self.cb_pi, self.cb_tr, self.cb_apu, self.cb_navp, self.cb_heu, self.cb_api, self.cb_ox, self.cb_fur]

        # add checkboxes
        """
        for i, cb in enumerate(self.cb_comp):
            vbox0.Add(cb, 0)
        """

        hbox.Add(vbox0, 0)

        # component list
        comp_title = ['Wing', 'Tail', 'Fuselage', 'Nacelle,..', 'Landing gear,..', 'Engine,..', 'Accessory', 'Air induction', 'Exhaust', 'Fuel system', 'Water injection', 'Propeller installation', 'APU', 'Instruments, ...', 'Electrical', 'Air conditioning', 'Oxygen system', 'Furnishing']

        sizer = wx.GridBagSizer(0, 0)
        j = 0 # 'comp' list index
        self.tc_dict = {} # dict of TextCtrl
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
            else:
                par = wx.StaticText(self, label=item)
                tc = wx.TextCtrl(self, wx.ID_ANY, "")
                self.tc_dict[item] = tc
                sizer.Add(par, pos=(i,0))
                sizer.Add(tc, pos=(i,1))

        hbox.Add(sizer, 0, wx.ALL, 5)
        self.SetSizer(hbox)

    def calculate_weight(self):

        d1 = {}

        for key, value in self.tc_dict.iteritems():
            if value.GetValue() is not u'':
                d1[key] = float(value.GetValue())

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
        d1['ttype_htail']= 'fixed'
        d1['ttype_vtail']= 'fuselage'
        d1['ttype_f']= 'main'
        d1['ttype_ucm']= 'low'
        d1['ttype_ucn']= 'low'
        d1['ttype_sc']= 'light'
        d1['ttype_airi']= 'single'
        d1['ttype_heu']= 'utility'
        d1['ttype_ox']= 'below'

        weights = ['w_w', 'w_tail', 'w_f', 'w_n', 'w_ucm', 'w_ucn', 'w_sc', 'w_eni', 'w_acc', 'w_airi', 'w_ext', 'w_oc', 'w_fsi', 'w_wis', 'w_pi', 'w_tr', 'w_apu', 'w_navp', 'w_heu', 'w_api', 'w_ox', 'w_fur']

        # dictionary of weights and components
        reference = {}
        for i, weight in enumerate(weights):
            reference[self.components[i]] = weight

        tor['w_w'] = torenbeek.w_w(d1['w_g'], d1['b_ref'], d1['Lambda'], d1['b'], d1['n_ult'], d1['s_w'], d1['t_r'], 'si')
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
