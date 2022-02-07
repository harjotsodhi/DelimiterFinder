import random 
import string

random.seed(42)
delim_chars = '!#$%&\\()*+,-./:;<=>?@[]^_`{}~\t'

def gen_data(num_delims, num_samples=20):
	cases = {}
	# for single or multi char delimiters
	if num_delims > 1:
		# form multi char delimiters based on the delim_chars list
		candidates = [''.join(random.choices(delim_chars, k=num_delims)) for _ in range(len(delim_chars))]
	else:
		# try each symbol from the delim_char list as a single delimiter
		candidates = delim_chars

	for d in candidates:
	    data = []
	    num_cols,num_rows = random.randint(3,50), num_samples
	    charlist = string.ascii_letters+delim_chars+string.digits
	    for i in range(num_rows):
	        row = []
	        # form elements N elements to populate row i
	        for j in range(num_cols):
	            # decide if char or null (besides first row)
	            b = '1'
	            if i > 0:
	            	b = random.choices(['0','1'], weights=[0.25,0.75], k=1)[0]
	            if b == '0':
	                row.append(d)
	            else:
	                num_chars = random.randint(1,50)
	                chars = random.choices(charlist, k=num_chars)
	                # remove current delim from generated element
	                chars = ''.join(chars).replace(d, '')+d
	                row.append(chars)
	        row = ''.join(row)
	        data.append(row)
	    cases[d] = data
	return cases