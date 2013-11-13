#!/usr/bin/env python
import wx
import threading
import tarsnap as ts


class TarFrame(wx.Frame):
	"""We simply derive a new class of Frame."""
	def __init__(self, parent, title):
		# Initialize things
		wx.Frame.__init__(self, parent, title=title, size=(500,500))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar()
		self.tarsnap = ts.TarSnap()
		filemenu = wx.Menu()

		# File options
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

		# Tarsnap options
		tarsnap_menu = wx.Menu()
		list = tarsnap_menu.Append(wx.ID_ANY, "&List Archives", " List all your current tarsnap archives")
		stats = tarsnap_menu.Append(wx.ID_ANY, "&Print Stats", "Print current stats")
		stats_for = tarsnap_menu.Append(wx.ID_ANY, "&Print Stats for", "Print stats for a user")

		# Create menu bar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		menuBar.Append(tarsnap_menu, "&Tarsnap")
		self.SetMenuBar(menuBar)

		# File menu events
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

		# Tarsnap menu events
		self.Bind(wx.EVT_MENU, lambda event: self.TarsnapCommand(event, ts.LIST), list)
		self.Bind(wx.EVT_MENU, lambda event: self.TarsnapCommand(event, ts.STATS), stats)
		self.Bind(wx.EVT_MENU, lambda event: self.TarsnapCommand(event, ts.STATS,
			archive="icarus-2013-11-11"), stats_for)

		# Threading events
		self.Bind(EVT_THREAD, self.OnFinishedCommand)

		self.Show(True)

	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "A Tarsnap GUI", "About Tarsnap GUI", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExit(self, e):
		self.Close(True)

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
		self.control.SetValue(e.GetValue())


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
app.MainLoop()