#!/usr/bin/env python
import wx
import threading
from subprocess import check_output

tarsnap_location = "E:\\cygwin\\bin\\tarsnap.exe"

class MyFrame(wx.Frame):
	"""We simply derive a new class of Frame."""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(500,500))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar()

		filemenu = wx.Menu()

		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

		tarsnap_menu = wx.Menu()
		list = tarsnap_menu.Append(wx.ID_ANY, "&List Archives", " List all your current tarsnap archives")

		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		menuBar.Append(tarsnap_menu, "&Tarsnap")
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.ListArchives, list)
		self.Bind(EVT_THREAD, self.OnFinishedCommand)

		self.Show(True)

	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "A Tarsnap GUI", "About Tarsnap GUI", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExit(self, e):
		self.Close(True)

	def ListArchives(self, e):
		worker = TarsnapThread(self, "--list-archives")
		worker.start()

	def OnFinishedCommand(self, e):
		val = "Current Archives: \n" + e.GetValue()
		self.control.SetValue(val)

myEVT_THREAD = wx.NewEventType()
EVT_THREAD = wx.PyEventBinder(myEVT_THREAD, 1)
class ThreadedEvent(wx.PyCommandEvent):
	""" Event to signal that a tarsnap command has finished """
	def __init__(self, etype, eid, value=None):
		wx.PyCommandEvent.__init__(self, etype, eid)
		self._value = value

	def GetValue(self):
		return self._value

class TarsnapThread(threading.Thread):
	def __init__(self, parent, command, value=None):
		threading.Thread.__init__(self)
		self.command = command
		self._parent = parent
		self._value = value

	def run(self):
		command = tarsnap_location + " " + self.command
		self._value = check_output(command, shell=True)
		evt = ThreadedEvent(myEVT_THREAD, -1, self._value)
		wx.PostEvent(self._parent, evt)


app = wx.App(False)
frame = MyFrame(None, 'Small editor')
app.MainLoop()