import wx
import numpy
import methods
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class Frame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = "Test", pos = wx.DefaultPosition, size = wx.Size( 600,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        sizer = wx.BoxSizer( wx.VERTICAL )

        self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.login = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.notebook.AddPage( self.login, u"Login", False )
        self.entry = wx.ScrolledWindow( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.entry.SetScrollRate( 5, 5 )
        entry_sizer = wx.BoxSizer( wx.VERTICAL )

        self.text = wx.StaticText( self.entry, wx.ID_ANY, u"Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc,", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text.Wrap( 600 )
        entry_sizer.Add( self.text, 1, wx.ALL, 0 )


        self.entry.SetSizer( entry_sizer )
        self.entry.Layout()
        entry_sizer.Fit( self.entry )
        self.notebook.AddPage( self.entry, u"Entry", True )

        sizer.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 0 )


        self.SetSizer( sizer )
        self.Layout()

        self.Centre( wx.BOTH )
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    Frame(None)
    app.MainLoop()
