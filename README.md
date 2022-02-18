# DelimiterFinder

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

```

```

## User Guide

Using **DelimiterFinder** is easy. To get started, simply create an instance of the `Finder` class and pass your data to the `find` method. The example below walks through a simple implementation.

```python
>>> from DelimiterFinder.finder import Finder
>>> # example data
>>> data = "c_1~|~c_2~|~c_3\n1~|~2~|~3\n4~|~~|~\n5~|~~|~6"""
>>> delim_locator = Finder()
>>> delim = delim_locator.find(data)
>>> print(delim)
~|~
>>> print(delim_locator.posterior)
{'_': 0.022, '~|~': 0.977}
>>> print(delim_locator.bayes_factor)
42.66
```

As we can see from the output above, the **DelimiterFinder** was able to identify an unknown three character long delimiter. The `posterior` attribute provides a dictionary with all of the tested candidates delimiters and their associated posterior probabilities. The `bayes_factor` attribute shows us that there is very strong evidence (i.e., a value greater than 10) in favor of the most likely delimiter relative to the second most likely delimiter. All with just 4 rows of data!

Indeed, **DelimiterFinder** can handle much more complicated data than the example given above, with the confidence in the decision made increasing with the number of rows provided. The **DelimiterFinder** has been tested for robustness against hundreds of randomly generated test cases. These tests can be found in the [tests directory](https://github.com/harjotsodhi/DelimiterFinder/tree/main/tests) on GitHub.

## Bayesian Methods

**DelimiterFinder** leverages Bayesian techniques to probabilistically identify unknown delimiters given data. In particular, **DelimiterFinder** fits a model using sequential Bayesian updating.

The model is given as follows:

<p align="center">
    <img src="https://github.com/harjotsodhi/DelimiterFinder/blob/main/eq1.png"\>
</p>
