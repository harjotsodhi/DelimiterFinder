import unittest
from tests import generate_data as gd
from DelimiterFinder.finder import Finder


class TestFinder(unittest.TestCase):

	def test_single_delim(self):
		num_samples = 10
		data = gd.gen_data(num_delims=1, num_samples=num_samples)
		f = Finder(num_samples=num_samples)
		for delim in data.keys():
			self.assertEqual(delim, f.find(data[delim]))

	def test_multi_delim(self):
		num_samples = 20
		data = gd.gen_data(num_delims=3, num_samples=num_samples)
		f = Finder(num_samples=num_samples)
		for delim in data.keys():
			print(delim)
			self.assertEqual(delim, f.find(data[delim]))

	def test_uncertain(self):
		pass

	def test_posterior(self):
		pass

	def test_read_str(self):
		pass

	def test_read_list(self):
		pass

	def test_read_path(self):
		pass

	def test_ignore_chars(self):
		pass

	def test_ispath(self):
		pass

	def test_num_samples(self):
		pass