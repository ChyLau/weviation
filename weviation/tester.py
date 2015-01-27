import wx

# Import Matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class MyFrame ( wx.Frame ):

    def __init__( self, parent ):

        # FORM BUILDER OUTPUT
        #########################
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 600,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook2 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel5 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel5.SetSizer( bSizer10 )
        self.m_panel5.Layout()
        bSizer10.Fit( self.m_panel5 )
        self.m_notebook2.AddPage( self.m_panel5, u"Page1", False )
        self.m_panel6 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel6.SetSizer( bSizer11 )
        self.m_panel6.Layout()
        bSizer11.Fit( self.m_panel6 )
        self.m_notebook2.AddPage( self.m_panel6, u"Page2", False )

        bSizer9.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 5 )

        self.SetSizer( bSizer9 )
        self.Layout()

        self.Centre( wx.BOTH )

        #########################

        graph1 = self.create_graph( self.m_panel5, size=(3, 2.255252) )
        graph2 = self.create_graph( self.m_panel6, size=(5.5556, 3.5) )

        ####################

    def create_canvas( self, panel, size ):
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.set_xlim([0,10])
        ax.set_ylim([0,100])
        ax.axis('off')

        fig.set_size_inches( size )  # If this is a float to 3 decimals is causes problems

        canvas = FigureCanvas(panel, -1, fig)
        sizer = panel.GetSizer()
        sizer.Add(canvas)
        return(canvas)

    def create_graph( self, panel, size ):
        canvas = self.create_canvas(panel,size)
        ax = canvas.figure.axes[0]
        xdata = range(1,10)
        ydata = [x*x for x in xdata]
        ax.scatter( xdata, ydata )
        ax.bar( xdata, [100]*9, 0.5, 0, color='red' )
        ax.plot()
        return(ax)


class MyApp(wx.App):
    def OnInit(self):
        main = MyFrame(None)
        main.Show()
        return True

app = MyApp(0)
app.MainLoop()

print('Done')
