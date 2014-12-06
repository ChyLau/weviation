import wx
import methods

class TabPanel(wx.ScrolledWindow):
    def __init__(self, parent, dlist):
        """"""
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(5,5)

        self.dlist = dlist
        self.init_tab()


    def init_tab(self):
        hbox = wx.BoxSizer(wx.VERTICAL)

        stxt0 = wx.StaticText(self, label='Components')
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        stxt0.SetFont(font)
        line0 = wx.StaticLine(self)
        hbox.Add(stxt0, 0, wx.ALL, 5)
        hbox.Add(line0, 1, wx.ALL|wx.EXPAND, 5)

        vbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.cball = wx.CheckBox(self, label='select all')
        self.cb0 = wx.CheckBox(self, label='wing')
        self.cb1 = wx.CheckBox(self, label='tail')
        hbox.Add(self.cball, 0)
        self.Bind(wx.EVT_CHECKBOX, self.select_all, self.cball)
        vbox0.Add(self.cb0, 0)
        vbox0.Add(self.cb1, 0)

        hbox.Add(vbox0, 0)

        comp = ['Wing', 'Tail', 'Fuselage', 'Nacelle,..', 'Landing gear,..', 'Engine,..', 'Accessory', 'Air induction']#, 'Exhaust', 'Fuel system', 'Water injection', 'Propeller installation', 'APU', 'Instruments, ...', 'Electrical', 'Air conditioning', 'Oxygen system', 'Furnishing']
        sizer = wx.GridBagSizer(0, 0)
        count = 0
        j = 0
        clist = [0, 9, 15, 22, 25, 36, 40, 44, ]
        llist = [x+1 for x in clist]
        self.t = {}

        for i in xrange(len(self.dlist) + len(clist)*2):
            if i in llist:
                line = wx.StaticLine(self)
                sizer.Add(line, pos=(i,0), span=(1,4), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)
            elif i in clist:
                stxt2 = wx.StaticText(self, label=comp[j])
                font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
                stxt2.SetFont(font)
                sizer.Add(stxt2, pos=(i, 0), flag=wx.TOP, border=10)
                j += 1
            else:
                stxt = wx.StaticText(self, label=self.dlist[count])
                txt = wx.TextCtrl(self, wx.ID_ANY, "")
                self.t[self.dlist[count]] = txt
                sizer.Add(stxt, pos=(i,0))
                sizer.Add(txt, pos=(i, 1))
                count += 1


        rb1 = wx.RadioButton(self, label='kg')
        rb2 = wx.RadioButton(self, label='lb')
        rb3 = wx.RadioButton(self, label='m')
        rb4 = wx.RadioButton(self, label='ft')
        rb5 = wx.RadioButton(self, label='m^2')
        rb6 = wx.RadioButton(self, label='ft^2')
        rb7 = wx.RadioButton(self, label='deg')
        rb8 = wx.RadioButton(self, label='rad')

        sizer.Add(rb1, pos=(2, 2))
        sizer.Add(rb2, pos=(2, 3))

        sizer.Add(rb3, pos=(3, 2))
        sizer.Add(rb4, pos=(3, 3))

        sizer.Add(rb7, pos=(4, 2))
        sizer.Add(rb8, pos=(4, 3))

        sizer.Add(rb3, pos=(5, 2))

        sizer.Add(rb4, pos=(5, 3))

        sizer.Add(rb5, pos=(7, 2))
        sizer.Add(rb6, pos=(7, 3))

        hbox.Add(sizer, 0, wx.ALL, 5)
        self.SetSizer(hbox)

    def calculate_weight(self):

        d1 = {}
        for key, value in self.t.iteritems():
            if value.GetValue() is not u'':
                d1[key] = float(value.GetValue())

        torenbeek = methods.Torenbeek()
        tor = {}

        ret = ""

        if self.cb0.GetValue() == True:
            tor['w_w'] = torenbeek.w_w(d1['w_g'], d1['b_ref'], d1['Lambda_1/2'], d1['b'], d1['n_ult'], d1['S_w'], d1['t_r'], 'si')
            ret += str(tor['w_w']) + "\n"

        if self.cb1.GetValue() == True:
            ret += "OK\n"

        return ret

    def select_all(self, evt):
        label = evt.GetEventObject().GetValue()

        if label:
            self.cb0.SetValue(True)
            self.cb1.SetValue(True)



class DemoFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Weviation",
                          size=(1200,800)
                          )

        tlist = ['w_g','b_ref', 'Lambda_1/2', 'b', 'n_ult', 'S_w', 't_r', 'S_v', 'S_h', 'Lambda_h', 'Lambda_v', 'V_D', 'l_t', 'b_f', 'h_f', 'S_G', 'P_to', 'a_m', 'b_m', 'c_m', 'd_m', 'a_n', 'b_n', 'c_n', 'd_n', 'W_to', 'n_e', 'W_e', 'w_fto', 'l_d', 'n_i', 'a_i', 'a_ex', 'T_to', 'n_ft', 'v_ft','v_wt','n_p','b_p','d_p','W_ba','W_DE','R_D','P_el','l_pax','n_pax','W_ZF']

        panel = wx.Panel(self)

        # tabs
        notebook = wx.Notebook(panel)

        self.tabOne = TabPanel(notebook, tlist)
        notebook.AddPage(self.tabOne, "Torenbeek")

        self.tabTwo = TabPanel(notebook, tlist)
        notebook.AddPage(self.tabTwo, "Raymer")

        self.tabThree = TabPanel(notebook, tlist)
        notebook.AddPage(self.tabThree, "General Dynamics")

        # calculate button
        btnCalc = wx.Button(panel, label='Calculate', size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.calculate_button, btnCalc)

        # method checkbox
        cb_tor = wx.CheckBox(panel, label='Torenbeek')
        cb_ray = wx.CheckBox(panel, label='Raymer')
        cb_gd = wx.CheckBox(panel, label='General Dynamics')

        # data output window
        self.txt1 = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)


        # adding stuff
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)

        hbox0.Add(btnCalc)
        hbox0.Add(cb_tor)
        hbox0.Add(cb_ray)
        hbox0.Add(cb_gd)
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
            self.txt1.SetValue(self.tabOne.calculate_weight())



if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame()
    app.MainLoop()
