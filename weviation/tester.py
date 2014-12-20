import wx
import wx.lib.agw.piectrl as PC

class MyFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "PieCtrl Demo")

        panel = wx.Panel(self)

        # create a simple PieCtrl with 3 sectors
        mypie = PC.PieCtrl(panel, -1, wx.DefaultPosition, wx.Size(180,270))

        part = PC.PiePart()

        part.SetLabel("Label 1")
        part.SetValue(300)
        part.SetColour(wx.Colour(200, 50, 50))
        mypie._series.append(part)

        part = PC.PiePart()

        part.SetLabel("Label 2")
        part.SetValue(200)
        part.SetColour(wx.Colour(50, 200, 50))
        mypie._series.append(part)

        part = PC.PiePart()

        part.SetLabel("helloworld label 3")
        part.SetValue(50)
        part.SetColour(wx.Colour(50, 50, 200))
        mypie._series.append(part)

        # create a ProgressPie
        progress_pie = PC.ProgressPie(panel, 100, 50, -1, wx.DefaultPosition,
                                      wx.Size(180, 200), wx.SIMPLE_BORDER)

        progress_pie.SetBackColour(wx.Colour(150, 200, 255))
        progress_pie.SetFilledColour(wx.Colour(255, 0, 0))
        progress_pie.SetUnfilledColour(wx.WHITE)
        progress_pie.SetHeight(20)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer.Add(mypie, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(progress_pie, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_sizer)
        main_sizer.Layout()


# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()
