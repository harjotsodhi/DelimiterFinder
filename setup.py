from setuptools import setup


with open("README.md", "r") as f:
	long_description = f.read()


setup(
	name="DelimiterFinder",
	version="0.0.2",
	author="Harjot Sodhi",
	author_email="harjotsodhi17@gmail.com",
	url="https://github.com/harjotsodhi/DelimiterFinder",
	description="Python package for probabilistic delimiter detection.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=['DelimiterFinder'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Operating System :: OS Independent",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
	]
)