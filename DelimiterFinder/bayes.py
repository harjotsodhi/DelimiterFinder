class Inference(object):

	def fit(self, data, candidates):
		"""
		Fit the model using sequential Bayesian updating.

		Parameters:
		-----------
		data: list
		    List with each element as a row of data.
		
		candidates: dict or collections.Counter
		    Each candidate delimiter as a key and number of occurences as values.

		Attributes:
		-----------
		posterior: dict
	            The posterior probability of each candidate delimiter.
		"""
		header = data.pop(0)
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

		# keep track of the two hypotheses: MAP and the alternative (next "most likely")
		self.hypotheses = {"map":{"delim":str(), "prob":0}, "alternative":{"delim":str(),"prob":0}}
		# normalize the posterior by dividing by the marginal likelihood
		for delim in self.posterior.keys():
		    self.posterior[delim] /= marginal_likelihood
		    # update MAP and alternative if a higher posterior probability is found 
		    if self.posterior[delim] > self.hypotheses["map"]["prob"]:
		    	# swap the MAP and alternative
		        self.hypotheses["alternative"].update(self.hypotheses["map"])
		        # update the MAP
		        self.hypotheses["map"].update({"delim":delim, "prob":self.posterior[delim]})
		    elif self.posterior[delim] > self.hypotheses["alternative"]["prob"]:
		    	# update the alternative
		        self.hypotheses["alternative"].update({"delim":delim, "prob":self.posterior[delim]})


	def predict(self):
		"""
		Return the maximum a posteriori probability (MAP) estimate.

		Returns:
		--------
		delim: str
	            The maximum a posteriori probability (MAP) estimate.
		"""
		return self.hypotheses['map']['delim']


	def test_hypothesis(self):
		"""
		Conduct Bayesian hypothesis testing to identify the Bayes factor.
		
		Returns:
		--------
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
		try:
		    bayes_factor = self.hypotheses['map']['prob']/self.hypotheses['alternative']['prob']
		except ZeroDivisionError:
		    bayes_factor = float('inf')
		return bayes_factor
