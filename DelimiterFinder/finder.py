import re
from collections import Counter



class Finder(object):
    def __init__(self, ignore_chars=None, num_samples=5):
        """
        Parameters:
        -----------
        ignore_chars: list, default=None
            List of non-alphanumeric characters which should
            not be considered candidate delimiters.
        
        num_samples: int, default=5
            Number of rows to sample for inference.
        
        Attributes:
        -----------
        posterior: dict
            The posterior probability of each candidate delimiter.
        """
        self.ignore_chars = ignore_chars
        self.num_samples = num_samples
    
    
    def find(self, data, new_line_sep="\n"):
        """
        Parameters:
        -----------
        data: str, list
            The input data either as a single string with
            each row separated by `new_line_sep` or a list 
            where each element is a row.
        
        new_line_sep: str, default='\n'
            The new line separator for the rows in the data.
        
        Returns:
        --------
        delim: str
            The maximum a posteriori probability (MAP) estimate.
        """
        # convert data into list of strings (if applicable)
        if type(data) == str:
            data = data.split(new_line_sep, self.num_samples)
        data = data[:self.num_samples]
        header = data.pop(0)
        # create regex expression
        alphanum, end = r"[^a-zA-Z0-9", " ]+"
        if not self.ignore_chars: self.ignore_chars = []
        match_chars = re.compile(alphanum+"".join(self.ignore_chars)+new_line_sep+end)
        # match all contiguous strings of valid non-alphanumeric characters
        matches = re.findall(match_chars, header)
        candidates = Counter(matches)

        # sequential Bayesian updating over N rows of data
        priors = {}
        self.posterior = {}
        total = sum(candidates.values())
        for row in data:
            marginal_likelihood = 0
            for delim in candidates:

                # initial prior is the probability of observing delimiter `m` in the header
                if delim not in priors:
                    priors[delim] = candidates[delim]/total

                # likelihood is the proportion of number of columns b/w the header and row `n`
                p0, pn = len(header.split(delim)), len(row.split(delim))
                if p0 < pn:
                    likelihood = p0 / pn
                else:
                    likelihood = pn / p0

                # unnormalized posterior
                self.posterior[delim] = priors[delim]*likelihood
                # update prior
                priors[delim] = self.posterior[delim]
                # we only need the marginal likelihood w.r.t the last row of data
                marginal_likelihood += self.posterior[delim]

        # normalize the posterior by dividing by the marginal likelihood
        for delim in self.posterior.keys():
            self.posterior[delim] /= marginal_likelihood
        
        # get MAP estimate
        delim = max(self.posterior, key=self.posterior.get)
        return delim