from tarsnap import Archive
from subprocess import check_output
import unittest
import time

"""
TODO: Tests to implement:
--Archive object created properly
--Can create new archives
--Can delete archives
--Can get archive stats
--Can restore archives

"""

class TestArchives(unittest.TestCase):
	def setUp(self):
		name = 'tarsnapgui-test-{}'.format(int(time.time()))
		check_output('touch /home/nate/source/tarsnap/test.txt', shell=True)
		# TODO - replace this with a test for actually creating an archive
		check_output('tarsnap -c -f {} /home/nate/source/tarsnap/test.txt'.format(name), shell=True)
		self.archive = Archive(name)

	def tearDown(self):
		self.archive.delete()

	def test_archive_stats(self):
		self.archive.stats()

	def test_archive_listing_files(self):
		self.archive.list_files()


if __name__ == '__main__':
	unittest.main()