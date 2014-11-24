import wx
import numpy
import matplotlib

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class TabPanel(wx.Panel):
    """
    This will be the first notebook tab
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        stxt1 = wx.StaticText(self, label="Gross weight")
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        hbox1.Add(stxt1, 0)
        hbox1.Add(txtOne, 0)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        stxt2 = wx.StaticText(self, label="Sweep angle")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")
        hbox1.Add(stxt2, 0)
        hbox1.Add(txtTwo, 0)

        sizer.Add(hbox1, 0, wx.ALL, 5)
        sizer.Add(hbox2, 0, wx.ALL, 5)

        self.SetSizer(sizer)

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

        # Create the first tab and add it to the notebook
        tabOne = TabPanel(self)
        #tabOne.SetBackgroundColour("Gray")
        self.AddPage(tabOne, "Torenbeek")

        # Create and add the second tab
        tabTwo = TabPanel(self)
        self.AddPage(tabTwo, "Raymer")

        # Create and add the third tab

        self.AddPage(TabPanel(self), "General Dynamics")

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

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
    app = wx.PySimpleApp()
    frame = MainFrame()
    app.MainLoop()
