# Install

```
pip3 install git+git://github.com/marti-1/apex.git@v0.3.0
```
## Philosophy

* [Mathematica](https://en.wikipedia.org/wiki/Wolfram_Mathematica) like API for scientific computing. It should be easy to do trivial things e.g.: group list by a function, import a CSV file, map a list in parallel, convert any date as a string into a DateTime object and etc.
* Names of the functions imported should not clash with the standard Python library, so that it would be always possible to do `from apex import *` and avoid typing module prefixes e.g. `ap.plot` and instead just `plot`.
* For data structures use Python default ones and `nd.arrays`. Fuck anything to do with DataFrames and Pandas.
* Support immutability.
