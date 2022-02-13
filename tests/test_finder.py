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
		s = "col1,col_2,col_3\ncol1,col_2,col_3\ncol1,col_2,col_3"
		f = Finder()
		# suppress printing warnings here (tested earlier) 
		warnings.filterwarnings("ignore")
		f.find(s)
		self.assertEqual({',': 0.5, '_': 0.5}, f.posterior)

	def test_read_str(self):
		s = "col1,col2,col3\na,b,c\nd,e,f"
		f = Finder()
		f.find(s)
		s = 123,456,789
		with self.assertRaises(TypeError):
			f.find(s)

	def test_read_list(self):
		s = ["col1,col2,col3","a,b,c","d,e,f"]
		f = Finder()
		f.find(s)
		s = {"col1,col2,col3","a,b,c","d,e,f"}
		with self.assertRaises(TypeError):
			f.find(s)

	def test_read_path(self):
		f = Finder()
		f.find("tests/example.txt", is_path=True, num_samples=10)
		with self.assertRaises(FileNotFoundError):
			f.find("tests/does_not_exist.txt", is_path=True)

	def test_ignore_chars(self):
		pass

	def test_ispath(self):
		pass

	def test_num_samples(self):
		pass