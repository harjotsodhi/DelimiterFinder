# DelimiterFinder
[![PyPI version](https://badge.fury.io/py/DelimiterFinder.svg)](https://badge.fury.io/py/DelimiterFinder)
[![codecov](https://codecov.io/gh/harjotsodhi/DelimiterFinder/branch/main/graph/badge.svg?token=N86QL890PL)](https://codecov.io/gh/harjotsodhi/DelimiterFinder)

**DelimiterFinder** is a Python package for probabilistic delimiter detection. It is a fast, efficient, and easy-to-use tool for identifying unknown delimiters within tabular data.

## Key Features

- **Versatile:** Detection of both single and multiple character delimiters.

- **Versatile:** Supports tabular data stored in a variety of formats, including common tabular data format files (e.g., CSV, TSV, TXT) or Python `string` and `list` types.

- **Robustness:** Leverages Bayesian techniques to probabilistically identify unknown delimiters given data.

- **Robustness:** Includes significance testing for all results.

- **Robustness:** Robust to malformed data (not an "all or nothing approach" in the case of malformed rows).

- **Transparency:** Reports posterior probabilities for all identified candidate delimiters.

- **Fast and efficient:** Detect delimiters with a high level of confidence given just 10 rows.

## Installation

Install the latest released version from [PyPI](https://pypi.org/project/DelimiterFinder/).

```
pip install DelimiterFinder
```

## User Guide

Using **DelimiterFinder** is easy. To get started, simply create an instance of the `Finder` class and pass your data to the `find` method. The example below walks through a simple implementation.

```python
>>> from DelimiterFinder.finder import Finder
>>> # example data
>>> data = "c_1~|~c_2~|~c_3\n1~|~2~|~3\n4~|~~|~\n5~|~~|~6"""
>>> # create instance of Finder and fit to data
>>> delim_locator = Finder()
>>> delim = delim_locator.find(data)
>>> # check the most likely delimiter
>>> print(delim)
~|~
>>> # check the probabilities for each delimiter
>>> print(delim_locator.posterior)
{'_': 0.022, '~|~': 0.977}
>>> # check the results of the significance test
>>> print(delim_locator.bayes_factor)
42.66
```

As we can see from the output above, the **DelimiterFinder** was able to identify an unknown three character long delimiter. The `posterior` attribute provides a dictionary with all of the tested candidates delimiters and their associated posterior probabilities. The `bayes_factor` attribute shows us that there is very strong evidence (i.e., a value greater than 10) in favor of the most likely delimiter relative to the second most likely delimiter. All with just 4 rows of data!

Indeed, **DelimiterFinder** can handle much more complicated data than the example given above, with the confidence in the decision made increasing with the number of rows provided. The **DelimiterFinder** has been tested for robustness against hundreds of randomly generated test cases. These tests can be found in the [tests directory](https://github.com/harjotsodhi/DelimiterFinder/tree/main/tests) on GitHub.

## Bayesian Methods

### Inference

**DelimiterFinder** leverages Bayesian techniques to probabilistically identify unknown delimiters given data. In particular, **DelimiterFinder** fits a model using sequential Bayesian updating.

The model is given as follows:

<p align="center">
    <img src="https://github.com/harjotsodhi/DelimiterFinder/raw/main/eq1.png"\>
</p>

Here, theta is a finite set of candidate delimiters. Candidate delimiters are all contiguous strings of valid (i.e., not in the given `ignore_chars` list) non-alphanumeric characters in the first row of data (assumed to be the header) The prior for these candidate delimiters is given by their relative frequencies. The variable X represents a row of data. The likelihood is the proportion of the number of columns in the header and number of columns in the given row of data, assuming delimiter theta is the true delimiter. Since this is a discrete distribution with a finite number of candidates delimiters, the denominator (normalization constant) is the sum over all thetas of the likelihood times prior.

The model is updated sequentially over M rows of data as follows:

<p align="center">
    <img src="https://github.com/harjotsodhi/DelimiterFinder/raw/main/eq2.png"\>
</p>

The posterior probabilities from row N are used as priors in row N+1. This is implemented sequentially for all rows 1...N...M. Finally, the maximum a posteriori probability (MAP) estimate is taken to be the delimiter.

<p align="center">
    <img src="https://github.com/harjotsodhi/DelimiterFinder/raw/main/eq3.png"\>
</p>

### Hypothesis Testing

A Bayesian hypothesis test is used to evaluate the significance of the most likely delimiter. The framework for this hypothesis test is as follows: hypothesis one is that the delimiter with the highest posterior probability (MAP estimate) is the true delimiter, and hypothesis two is that the delimiter with the second highest posterior probability is the true delimiter. The more likely hypothesis one is than hypothesis two, the more confident we are with the model's choice for most likely delimiter.

To conduct this hypothesis test, we will calculate the Bayes factor, which is the ratio of likelihood between the two hypotheses.

<p align="center">
    <img src="https://github.com/harjotsodhi/DelimiterFinder/raw/main/eq4.png"\>
</p>

The following rules are used to determine the significance of the results given the Bayes factor:

	1.) Bayes factor = 1: no evidence.
	2.) 1 < Bayes factor < 3: weak evidence.
	3.) 3 < Bayes factor < 10: substantial evidence.
	4.) Bayes factor > 10: strong evidence.
	5.) Bayes factor < 1: not possible in this hypothesis test.

	Source: Jeffreys, Harold (1998) [1961]. The Theory of Probability (3rd ed.). Oxford, England. p. 432.

**DelimiterFinder** will raise a warning if the Bayes factor for the chosen delimiter is less than 3. Increasing the number of rows or adding unwanted characters to the `ignore_chars` list will generally increase the Bayes factor.
