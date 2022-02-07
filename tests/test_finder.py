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
		# suppress printing warnings here (tested later) 
		warnings.filterwarnings("ignore")
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

	def test_bayes_factor(self):
		s = "col1,col2,col3\n1,2,3\n4,5,6"
		f = Finder()
		f.find(s)
		self.assertEqual(float('inf'), f.bayes_factor)
		s = "col1,col_2,col_3\ncol1,col_2,col_3\ncol1,col_2,col_3"
		f = Finder()
		# suppress printing warnings here (tested earlier) 
		warnings.filterwarnings("ignore")
		f.find(s)
		self.assertEqual(1., f.bayes_factor)

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