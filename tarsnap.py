import config
from subprocess import check_output

CREATE = 0
DELETE = 1
LIST = 2
RESTORE = 3
EXCLUDE = 4
STATS = 5

class NotImplemented(Exception):
	pass

class TarBase():
	def __init__(self):
		pass

	def _execute(self, command):
		"""
		Consolidating the actual execution here, in case we decide to use a different subprocess,
		and for error handling/timeouts from TarSnap
		"""

		return check_output(command, shell=True) # TODO - Error handling here, timeouts, exceptions


class TarSnap(TarBase):
	"""
	Basic TarSnap class. Basically just creates the stats object,
	creates new archives, and lists current ones.

	debug: if set to True, logs info and doesn't actually retrieve data from Tarsnap
	(uses fake, testing data).
	"""
	def __init__(self, debug=True):
		self.archives = None
		self.stats = None
		self.debug = debug

	def run_command(self, command, **kwargs):

		if command == LIST:
			# TODO - will eventually return actual archive objects
			if self.debug:
				self.archives = {"archive_list": ['archive1', 'archive2', 'archive4'] }
			else:
				if self.archives is None:
					archives = self._list()
					self.archives = {"archive_list": archives.split()}
			return self.archives

		elif command == STATS:
			# TODO - will eventually return a stats object
			if self.debug:
				self.stats = {"stats": "Using up all the bandwidth and space!"}
			else:
				self.stats = {"stats": self._stats(**kwargs)} 
			return self.stats

		elif command == CREATE:
			return self._create(**kwargs)

	def _list(self):
		command = config.tarsnap_executable + " --list-archives"
		return self._execute(command)

	def _stats(self, **kwargs):
		command = config.tarsnap_executable + " --print-stats"
		if 'archive' in kwargs:
			command = config.tarsnap_executable + " --print-stats -f " + kwargs['archive']
		return self._execute(command)

	def _create(self, **kwargs):
		raise NotImplemented("Not yet implemented")


class Archive(TarBase):
	""" Archives, that can be deleted, viewed, created, etc. """
	def __init__(self):
		pass


class Stats(TarBase):
	"""
	Class that can generate stats based on an entire account
	or specific archives.
	"""

	def __init__(self):
		pass		
