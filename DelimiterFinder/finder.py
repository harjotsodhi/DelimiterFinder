import os
import re
import warnings
from collections import Counter



class Finder(object):
    def __init__(self, ignore_chars=None):
        """
        Parameters:
        -----------
        ignore_chars: list, default=None
            List of non-alphanumeric characters which should
            not be considered candidate delimiters.
        
        Attributes:
        -----------
        posterior: dict
            The posterior probability of each candidate delimiter.

        bayes_factor: float
            Evidence in favor of the most likely delimiter (MAP)
            relative to the second most likely delimiter.
                
                1) bayes_factor == 1: no evidence.
                2) 1 < bayes_factor < 3: weak evidence.
                3) 3 < bayes_factor < 10: substantial evidence.
                4) bayes_factor > 10: strong evidence.
                5) bayes_factor < 1: not possible in this hypothesis test.

                Source: Jeffreys, Harold (1998) [1961]. The Theory of Probability (3rd ed.). Oxford, England. p. 432.
        """
        warnings.simplefilter("always")
        self.ignore_chars = ignore_chars


    ### public methods ###

    def find(self, data, is_path=False, num_samples=20, new_line_sep="\n"):
        """
        Parameters:
        -----------
        data: str, list
            The input data either as a single string with
            each row separated by `new_line_sep` or a list 
            where each element is a row.

            Alternatively, a path to a text file (e.g., .TXT, .CSV)
            may be passed, in which case, the `is_path` parameter
            should be set to "True"

        is_path: bool, default='False'
            An indicator for whether the value passed to the `data`
            parameter is a file path.

        num_samples: int, default=20
            Number of rows to sample for inference.
        
        new_line_sep: str, default='\n'
            The new line separator for the rows in the data.
        
        Returns:
        --------
        delim: str
            The maximum a posteriori probability (MAP) estimate.
        """
        data = self._format_data(data, is_path, num_samples, new_line_sep)
        rowOne = data.pop(0)
        # create regex expression for identifying valid delimiter characters.
        alphanum, end = r"[^a-zA-Z0-9", " ]+"
        if not self.ignore_chars: self.ignore_chars = []
        re_pattern = re.compile(alphanum+"".join(self.ignore_chars)+new_line_sep+end)
        # match all contiguous strings of valid non-alphanumeric characters     
        matches = re.findall(re_pattern, rowOne)
        candidates = Counter(matches)

        # sequential Bayesian updating over N rows of data
        priors = {}
        self.posterior = {}
        total = sum(candidates.values())
        for row in data:
            marginal_likelihood = 0
            for delim in candidates:
                # initial prior is the probability of observing delimiter `m` in the rowOne
                if delim not in priors:
                    priors[delim] = candidates[delim]/total

                # likelihood is the proportion of number of columns b/w the rowOne and row `n`
                p0, pn = len(rowOne.split(delim)), len(row.split(delim))
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

        # keep track of the two hypotheses: h1 (MAP) and h0 (next "most likely")
        h0, pr0 = "", 0
        h1, pr1 = "", 0
        # normalize the posterior by dividing by the marginal likelihood
        for delim in self.posterior.keys():
            self.posterior[delim] /= marginal_likelihood
            # update h1 and h0 if a higher posterior probability is found 
            if self.posterior[delim] > pr1:
                h0,pr0 = h1,pr1
                h1,pr1 = delim,self.posterior[delim]
            elif self.posterior[delim] > pr0:
                h0,pr0 = delim,self.posterior[delim]

        # calculate the Bayes factor
        try:
            self.bayes_factor = pr1/pr0
        except ZeroDivisionError:
            self.bayes_factor = float('inf')

        # display warning if the calculated Bayes factor for the MAP is less than 3
        if self.bayes_factor < 3:
            warnings.warn("Evidence in favor of the most likely delimiter is weak (Bayes factor = {0:.2f}). Try increasing the num_samples or adding characters to the ignore_chars list in order to obtain more conclusive results.".format(self.bayes_factor), 
                          stacklevel=2)
        
        # get MAP estimate
        delim = h1
        return delim


    ## private methods ##

    @staticmethod
    def _format_data(data, is_path, num_samples, new_line_sep):
        """
        Parameters:
        -----------
        data: str, list, path
            The input data either as a single string with
            each row separated by `new_line_sep` or a list 
            where each element is a row.

            Alternatively, a path to a text file (e.g., .TXT, .CSV)
            may be passed, in which case, the `is_path` parameter
            should be set to "True"

        is_path: bool
            An indicator for whether the value passed to the `data`
            parameter is a file path.

        num_samples: int
            Number of rows to sample for inference.

        new_line_sep: str
            The new line separator for the rows in the data.
        
        Returns:
        --------
        data: list
            A list of length `num_samples` where each element is a row.
        """
        if type(data) != str and type(data) != list:
            raise TypeError('data must be str or list')

        # convert data into list of strings (if applicable)
        if type(data) == str:
            # get data from path
            if is_path:
                with open(data, 'r') as f:
                    data = [next(f) for _ in range(num_samples)]
            # get data from non-path string
            else:
                # quick check to see if `is_path` should have been used
                if len(data) < 1000:
                    if os.path.exists(data): warnings.warn("The given string appears to be a valid file path, yet the `is_path` parameter was set to False. Set `is_path` to True for file paths.")

                data = data.split(new_line_sep, num_samples)

        data = data[:num_samples]
        return data