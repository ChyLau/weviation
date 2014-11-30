import wx
import wx.lib.fancytext as ft
import numpy
import matplotlib
import wx.lib.scrolledpanel as scrolled

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class TabTorenbeek(wx.Panel):
    """
    This will be the first notebook tab
    """
    def __init__(self, parent, dlist):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        fgs = wx.FlexGridSizer(len(dlist), 5, 5, 5)
        count = 0
        for i in xrange(len(dlist)*5-1):
            if i % 5 == 0:
                stxt = wx.StaticText(self, label=dlist[count])
                fgs.Add(stxt, 0, 0)
                count += 1
            elif i % 5 == 1:
                txt = wx.TextCtrl(self, wx.ID_ANY, "")
                fgs.Add(txt, 0, 0)
            elif i % 5 == 2:
                rb1 = wx.RadioButton(self, label='kg', style=wx.RB_GROUP)
                fgs.Add(rb1, 0, 0)
            elif i % 5 == 3:
                rb2 = wx.RadioButton(self, label='lb')
                fgs.Add(rb2, 0, 0)
            elif i % 5 == 4:
                ch = ['One', 'Two', 'Three']
                cb = wx.ComboBox(self, choices=ch, style=wx.CB_READONLY)
                fgs.Add(cb, 0, 0)
            else:
                print "ERROR: value i = %d is not assigned." % i

        hbox.Add(fgs, 0, wx.ALL, 5)

        self.SetSizer(hbox)

class TabTest(wx.Panel):
    def __init__(self, parent, dlist):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        hbox = wx.BoxSizer(wx.VERTICAL)

        btn0 = wx.Button(self, label='test', size=(80,30))
        hbox.Add(btn0, 0, 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn0)

        stxt0 = wx.StaticText(self, label='Components')
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        stxt0.SetFont(font)
        line0 = wx.StaticLine(self)
        hbox.Add(stxt0, 0, wx.ALL, 5)
        hbox.Add(line0, 1, wx.ALL|wx.EXPAND, 5)

        vbox0 = wx.BoxSizer(wx.HORIZONTAL)
        cb0 = wx.CheckBox(self, label='wing')
        cb1 = wx.CheckBox(self, label='tail')
        vbox0.Add(cb0, 0)
        vbox0.Add(cb1, 0)

        hbox.Add(vbox0, 0)

        comp = ['Wing', 'Tail', 'Fuselage', 'Nacelle,..', 'Landing gear,..', 'Engine,..', 'Accessory', 'Air induction']#, 'Exhaust', 'Fuel system', 'Water injection', 'Propeller installation', 'APU', 'Instruments, ...', 'Electrical', 'Air conditioning', 'Oxygen system', 'Furnishing']
        sizer = wx.GridBagSizer(0, 0)
        count = 0
        j = 0
        clist = [0, 9, 15, 22, 25, 36, 40, 44, ]
        llist = [x+1 for x in clist]
        for i in xrange(len(dlist) + len(clist)*2):
            if i in llist:
                line = wx.StaticLine(self)
                sizer.Add(line, pos=(i,0), span=(1,2), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)
            elif i in clist:
                stxt2 = wx.StaticText(self, label=comp[j])
                font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
                stxt2.SetFont(font)
                sizer.Add(stxt2, pos=(i, 0), flag=wx.TOP, border=10)
                j += 1
            else:
                stxt = wx.StaticText(self, label=dlist[count])
                txt = wx.TextCtrl(self, wx.ID_ANY, "")
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

    def OnButton(self, evt):
        label = evt.GetEventObject().GetLabel()

        if label == 'test':
            self.tc1.SetValue("OK")


class NotebookDemo(wx.Notebook):
    """
    Notebook class
    """
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )

        tlist_old = ['w<sub>g</sub>','b<sub>ref</sub>', 'Lambda<sub>1/2</sub>', 'b', 'n<sub>ult</sub>', 'S<sub>w</sub>', 't<sub>r</sub>', 'S<sub>v</sub>', 'S<sub>h</sub>', 'Lambda<sub>h</sub>', 'Lambda<sub>v</sub>', 'V<sub>D</sub>', 'l<sub>t</sub>', 'b<sub>f</sub>', 'h<sub>f</sub>', 'S<sub>G</sub>', 'P<sub>to</sub>', 'a<sub>m</sub>', 'b<sub>m</sub>', 'c<sub>m</sub>', 'd<sub>m</sub>', 'a<sub>n</sub>', 'b<sub>n</sub>', 'c<sub>n</sub>', 'd<sub>n</sub>', 'W<sub>to</sub>', 'n<sub>e</sub>', 'W<sub>e</sub>', 'w<sub>fto</sub>', 'l<sub>d</sub>', 'n<sub>i</sub>', 'a<sub>i</sub>', 'a<sub>ex</sub>', 'T<sub>to</sub>', 'n<sub>ft</sub>', 'v<sub>ft</sub>','v<sub>wt</sub>','n<sub>p</sub>','b<sub>p</sub>','d<sub>p</sub>','W<sub>ba</sub>','W<sub>DE</sub>','R<sub>D</sub>','P<sub>el</sub>','l<sub>pax</sub>','n<sub>pax</sub>','W<sub>ZF</sub>']

        tlist = []

        for item in tlist_old:
            temp = item.replace("<sub>", "_")
            newitem = temp.replace("</sub>", "")
            tlist.append(newitem)

        #sp = scrolled.ScrolledPanel(self)
        # Create the first tab and add it to the notebook
        tabOne = TabTest(self, tlist)
        #tabOne.SetBackgroundColour("Gray")
        self.AddPage(tabOne, "Torenbeek")

        # Create and add the second tab
        tabTwo = TabTorenbeek(self, tlist)
        #self.AddPage(tabTwo, "Raymer")

        # Create and add the third tab

        #self.AddPage(TabTorenbeek(self, tlist), "General Dynamics")

        #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()

    def OnPageChanging(self, event):

        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()

class OutputData(wx.Panel):
    """
    Pie chart
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(50, 50))

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        sizes = [15, 30, 45, 10]
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        self.axes.pie(sizes, labels=labels, colors=colors)
        self.axes.axis('equal')
        self.canvas = FigureCanvas(self, -1, self.figure)


class MainFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Weviation",
                          size=(1290,830)
                          )
        self.Centre()
        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # tabs widget
        vbox1 = wx.BoxSizer(wx.VERTICAL)

        text1 = wx.StaticText(panel, label="Input data")
        vbox1.Add(text1, flag=wx.TOP|wx.LEFT, border=15)

        vbox1.Add((-1, 10))

        line1 = wx.StaticLine(panel)
        vbox1.Add(line1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        vbox1.Add((-1, 10))

        notebook = NotebookDemo(panel)
        vbox1.Add(notebook, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        vbox1.Add((-1, 5))

        btn1 = wx.Button(panel, label='Calculate', size=(80,30))
        vbox1.Add(btn1, flag=wx.LEFT, border=10)
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn1)

        # pie chart widget

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        text2 = wx.StaticText(panel, label="Output pie chart")
        vbox2.Add(text2, flag=wx.TOP|wx.LEFT, border=15)

        vbox2.Add((-1, 10))

        line2 = wx.StaticLine(panel)
        vbox2.Add(line2, flag=wx.RIGHT|wx.EXPAND, border=10)

        vbox2.Add((-1, 10))

        output = OutputData(panel)
        vbox2.Add(output, flag=wx.RIGHT, border=10)

        # output widget
        vbox3 = wx.BoxSizer(wx.VERTICAL)

        text3 = wx.StaticText(panel, label="Output data")
        vbox3.Add(text3, flag=wx.TOP|wx.LEFT, border=15)

        vbox3.Add((-1, 10))

        line3 = wx.StaticLine(panel)
        vbox3.Add(line3, flag=wx.RIGHT|wx.EXPAND, border=10)

        vbox3.Add((-1, 10))

        self.tc1 = wx.TextCtrl(panel, style=wx.TE_READONLY)#, style=wx.TE_MULTILINE)
        vbox3.Add(self.tc1, proportion=1, flag=wx.EXPAND)

        # merge pie chart and output data
        vbox4 = wx.BoxSizer(wx.VERTICAL)
        vbox4.Add(vbox2)
        vbox4.Add(vbox3)

        # merge left and right side
        sizer.Add(vbox1, 1, wx.EXPAND)

        sizer.Add(vbox4, 1, wx.EXPAND)

        panel.SetSizer(sizer)
        self.Layout()

        self.Show()

    def OnButton(self, evt):
        label = evt.GetEventObject().GetLabel()

        if label == 'Calculate':
            self.tc1.SetValue("OK")


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
