# DelimiterFinder

**DelimiterFinder** is a Python package for probabilistic delimiter detection. It is a fast, efficient, and easy-to-use tool for identifying unknown delimiters within tabular data.

## Key Features

- **Versatile:** Detection of both single and multiple character delimiters.

- **Versatile:** Supports tabular data stored in a variety of formats, including common tabular data format files (e.g., CSV, TSV, TXT) or Python `string` and `list` types.

- **Robustness:** Leverage Bayesian techniques to probabilistically identify unknown delimiters given data.

- **Robustness:** Includes significance testing for all results.

- **Robustness:** Robust to malformed data (not an "all or nothing approach" in the case of malformed rows).

- **Transparency:** Reports posterior probabilities for all identified candidate delimiters.

- **Fast and efficient:** Detect delimiters with a high level of confidence given just 10 rows.