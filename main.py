#!/usr/bin/env python
import wx
import threading
import tarsnap as ts

debugging = False

class TarFrame(wx.Frame):
    """ Top level frame. Doesn't know about Tarsnap. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,500))
        self.CreateStatusBar()
        filemenu = wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        # Create menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        # File menu events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Show(True)

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A Tarsnap GUI", "About Tarsnap GUI", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        self.Close(True)


class TarWindow(wx.Panel):
    """ The main panel. Most of the tarsnap interactino should happen here. """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.tarsnap = ts.TarSnap(debugging)

        # Begin loading the tarsnap archive info when the app starts up
        self.TarsnapCommand(None, ts.LIST)
        self.TarsnapCommand(None, ts.STATS)

        grid = wx.GridBagSizer(hgap=5, vgap=5)
        self.archive_label = wx.StaticText(self, label="Loading info on your current archives...")
        self.stats_label = wx.StaticText(self, label="Loading stats for your current archives...")
        grid.Add(self.archive_label, pos=(0,0))
        grid.Add(self.stats_label, pos=(0,2))

        # Buttons and sizing
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.create_button = wx.Button(self, -1, "Create an Archive")
        self.restore_button = wx.Button(self, -1, "Restore an Archive")
        self.stats_button = wx.Button(self, -1, "Stats")
        self.buttons = [self.create_button, self.restore_button, self.stats_button]
        for button in self.buttons:
            self.button_sizer.Add(button, wx.EXPAND)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.button_sizer, 0, wx.EXPAND)
        self.sizer.Add(grid, 0, wx.ALL, 5)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        # Event bound to a returned command
        self.Bind(EVT_THREAD, self.OnFinishedCommand)


        self.Show(True)

    def TarsnapCommand(self, e, command, **kwargs):
        """Create a thread for a tarsnap command"""
        worker = TarsnapThread(self, command, self.tarsnap, **kwargs)
        worker.start()

    def OnFinishedCommand(self, e):
        """
        Run after a succesfull TarSnap command
        TODO - check the eid for the command type, and handle it accordingly in the frame
        Or maybe have them as different event thread types?
        """
        result = e.GetValue()
        if 'archive_list' in result:
            archive_str = "Archives:\n"
            archives = '\n'.join(result['archive_list'])
            self.archive_label.SetLabel(archive_str + archives)
        if 'stats' in result:
            stats_str = "Stats:\n{}".format(result['stats'])
            self.stats_label.SetLabel(stats_str)


myEVT_THREAD = wx.NewEventType()
EVT_THREAD = wx.PyEventBinder(myEVT_THREAD, 1)
class ThreadedEvent(wx.PyCommandEvent):
    """ Event to signal that a tarsnap command has finished """
    def __init__(self, etype, eid, value=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.eid = eid
        self._value = value

    def GetValue(self):
        return self._value


class TarsnapThread(threading.Thread):
    def __init__(self, parent, command, tarsnap, **kwargs):
        threading.Thread.__init__(self)
        self.command = command
        self.tarsnap = tarsnap
        self.kwargs = kwargs
        self._parent = parent

    def run(self):
        self._value = self.tarsnap.run_command(self.command, **self.kwargs)
        evt = ThreadedEvent(myEVT_THREAD, self.command, self._value) # Callback
        wx.PostEvent(self._parent, evt)


app = wx.App(False)
frame = TarFrame(None, 'Tarsnap GUI')
panel = TarWindow(frame)
frame.Show()
app.MainLoop()