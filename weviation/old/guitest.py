import wx

class Frame1(wx.Frame):
    def __init__(self, parent, mytitle):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle)
        self.SetBackgroundColour("green")
        # pass frame1 to frame2 as instance self
        self.frame2 = Frame2(None, 'Frame1', self)

        # create input widgets
        self.button1 = wx.Button(self, wx.ID_ANY, label='Frame2')
        self.button2 = wx.Button(self, wx.ID_ANY, label='Button2')
        self.button3 = wx.Button(self, wx.ID_ANY, label='Button3')
        # bind mouse event to an action
        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)

        # use a box sizer to lay out widgets
        sizer_v = wx.BoxSizer(wx.VERTICAL)
        # Add(widget, proportion, flag, border)
        sizer_v.Add(self.button1, 0, flag=wx.ALL, border=10)
        sizer_v.Add(self.button2, 0, flag=wx.ALL, border=10)
        sizer_v.Add(self.button3, 0, flag=wx.ALL, border=10)
        self.SetSizer(sizer_v)

        # size the frame so all the widgets fit
        self.Fit()

    def button1Click(self, event):
        """button1 has been left clicked"""
        # self is instance frame1
        self.Hide()
        self.frame2.Show()


class Frame2(wx.Frame):
    def __init__(self, parent, mytitle, frame1):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle)
        self.SetBackgroundColour("brown")
        self.frame1 = frame1

        # create input widgets
        self.button1 = wx.Button(self, wx.ID_ANY, label='Frame1')
        self.button2 = wx.Button(self, wx.ID_ANY, label='Button2')
        self.button3 = wx.Button(self, wx.ID_ANY, label='Button3')
        # bind mouse event to an action
        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)
        # responds to exit symbol x on frame2 title bar
        self.Bind(wx.EVT_CLOSE, self.button1Click)

        # use a box sizer to lay out widgets
        sizer_v = wx.BoxSizer(wx.VERTICAL)
        # Add(widget, proportion, flag, border)
        sizer_v.Add(self.button1, 0, flag=wx.ALL, border=10)
        sizer_v.Add(self.button2, 0, flag=wx.ALL, border=10)
        sizer_v.Add(self.button3, 0, flag=wx.ALL, border=10)
        self.SetSizer(sizer_v)

        # size the frame so all the widgets fit
        self.Fit()

    def button1Click(self, event):
        """button1 has been left clicked"""
        # self is instance frame2
        self.Hide()
        self.frame1.Show()


app = wx.App()
# create a MyFrame instance and show the frame
frame1 = Frame1(None, 'Frame1')
frame1.Show()
app.MainLoop()
