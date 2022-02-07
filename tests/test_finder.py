import unittest
import warnings
from tests import generate_data as gd
from DelimiterFinder.finder import Finder


class TestFinder(unittest.TestCase):

	def test_single_delim(self):
		data = gd.gen_data(num_delims=1)
		f = Finder()
		for delim in data.keys():
			# test each case
			self.assertEqual(delim, f.find(data[delim]))

	def test_multi_delim(self):
		f = Finder()
		for n in [2,3,4,5,6,7]:
			# test each delimiter length suite of cases
			data = gd.gen_data(num_delims=n)
			for delim in data.keys():
				# test each case
				self.assertEqual(delim, f.find(data[delim]))

	def test_uncertain(self):
		s = "col1,col_2,col_3\ncol1,col_2,col_3\ncol1,col_2,col_3"
		f = Finder()
		with self.assertWarns(Warning):
			f.find(s)

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