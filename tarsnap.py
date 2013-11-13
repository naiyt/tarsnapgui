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

class TarSnap():
	"""docstring for TarSnap"""
	def __init__(self, debug=True):
		self.archives = None
		self.stats = None

	def run_command(self, command, **kwargs):
		if command == LIST:
			if self.archives is None:
				self.archives = self._list()
			return self.archives

		elif command == STATS:
			self.stats = self._stats(**kwargs)
			return self.stats

		elif command == EXCLUDE:
			return self._exclude(**kwargs)

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

	def _exclude(self, **kwargs):
		raise NotImplemented("Not yet implemented")

	def _create(self, **kwargs):
		raise NotImplemented("Not yet implemented")


	def _execute(self, command):
		"""
		Consolidating the actual execution here, in case we decide to use a different subprocess,
		and for error handling/timeouts from TarSnap
		"""

		return check_output(command, shell=True) # TODO - Error handling here, timeouts, exceptions