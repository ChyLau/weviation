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
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)

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
        tabOne.SetBackgroundColour("Gray")
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
                          size=(1000,800)
                          )
        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5,5)

        text1 = wx.StaticText(panel, label="Input data")
        sizer.Add(text1, pos=(0,0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)

        line1 = wx.StaticLine(panel)
        sizer.Add(line1, pos=(1,0), span=(1,1), flag=wx.EXPAND|wx.BOTTOM, border=10)

        notebook = NotebookDemo(panel)
        sizer.Add(notebook, pos=(2,0), span=(1,1), flag=wx.EXPAND|wx.BOTTOM, border=5)

        text2 = wx.StaticText(panel, label="Output pie chart")
        sizer.Add(text2, pos=(0,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)

        line2 = wx.StaticLine(panel)
        sizer.Add(line2, pos=(1,2), span=(1,1), flag=wx.EXPAND|wx.BOTTOM, border=10)

        output = OutputData(panel)
        sizer.Add(output, pos=(2,2), span=(1,1), flag=wx.EXPAND|wx.BOTTOM, border=5)

        text3 = wx.StaticText(panel, label="Output data")
        sizer.Add(text3, pos=(3,2), flag=wx.LEFT, border=15)

        line3 = wx.StaticLine(panel)
        sizer.Add(line3, pos=(4,2), span=(1,1), flag=wx.EXPAND|wx.BOTTOM, border=10)

        tc1 = wx.TextCtrl(panel)
        sizer.Add(tc1, pos=(5,2), span=(1, 1), flag=wx.EXPAND)

        panel.SetSizer(sizer)
        self.Layout()

        self.Show()


if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MainFrame()
    app.MainLoop()
