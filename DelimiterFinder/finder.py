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
        """
        self.ignore_chars = ignore_chars


    ### public methods ###

    def find(self, data, is_path=False, num_samples=5, new_line_sep="\n"):
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

        num_samples: int, default=5
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

        # normalize the posterior by dividing by the marginal likelihood
        for delim in self.posterior.keys():
            self.posterior[delim] /= marginal_likelihood
        
        # get MAP estimate
        delim = max(self.posterior, key=self.posterior.get)
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
        assert type(data) == str or type(data)== list, 'data must be str or list'
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
                    if os.path.exists(data): warnings.warn("""The given string appears to be a valid file path, 
                                                              yet the `is_path` parameter was set to False. 
                                                              Set `is_path` to True for file paths.""")

                data = data.split(new_line_sep, num_samples)

        data = data[:num_samples]
        return data