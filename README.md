# `fast-rake`

`fast-rake` is library for keyword extraction built to efficiently process large
collections of text. The performance gains derive from using optimized regular expressions
for stop words and a few Python-specific optimizations.

The Rapid Automatic Keyword Extraction (RAKE) algorithm is described in
[Rose, S., et al., (2010)](https://onlinelibrary.wiley.com/doi/10.1002/9780470689646.ch1).

## Features

- Use of optimized regular expressions for splitting sentences into phrasal quantities.
  Included are optimized stopword lists from *google*, *nltk*, *scikit-learn*, and *SMART*.
  
- Allows for custom stopword lists to augment the built-in stop words.
  
- Python-specific optimizations to speed each step of the algorithm.
  
- Safe for multiprocessing (see `examples/bbc_mp.py`).

## Test & Install

To install:
```bash
python setup.py install
```

If `pytest` is installed, tests can be run via:

```bash
python -m pytest -v
```

## Examples
The following example is from Rose, et al.:
> Compatibility of systems of linear constraints over the set of natural numbers. 
> Criteria of compatibility of a system of linear Diophantine equations, strict 
> inequations, and nonstrict inequations are considered. Upper bounds for 
> components of a minimal set of solutions and algorithms of construction of 
> minimal generating sets of solutions for all types of systems are given. 
> These criteria and the corresponding algorithms for constructing a minimal 
> supporting set of solutions can be used in solving all the considered types of 
> systems and systems of mixed types.


The implementation uses `__call__`:
```
>>> from fast_rake import Rake
>>>
>>> # default arguments are shown
>>> smart_rake = Rake(stopword_name="smart", custom_stopwords=None, max_kw=None, ngram_range=None, top_percent=1.0, kw_only=False)
>>>
>>> text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types." 
>>> kw = smart_rake(text)
```
The resulting list, `kw`:
```bash
[
        ("minimal generating sets", 8.666666666666666),
        ("linear Diophantine equations", 8.5),
        ("minimal supporting set", 7.666666666666666),
        ("minimal set", 4.666666666666666),
        ("linear constraints", 4.5),
        ("natural numbers", 4.0),
        ("strict inequations", 4.0),
        ("nonstrict inequations", 4.0),
        ("Upper bounds", 4.0),
        ("mixed types", 3.666666666666667),
        ("considered types", 3.166666666666667),
        ("set", 2.0),
        ("types", 1.6666666666666667),
        ("considered", 1.5),
        ("Compatibility", 1.0),
        ("systems", 1.0),
        ("Criteria", 1.0),
        ("compatibility", 1.0),
        ("system", 1.0),
        ("components", 1.0),
        ("solutions", 1.0),
        ("algorithms", 1.0),
        ("construction", 1.0),
        ("criteria", 1.0),
        ("constructing", 1.0),
        ("solving", 1.0),
    ]
```

**N.B.** 
The algorithm is case-sensitive. In this example, both
*Compatibility* and *compatibility* are considered separate keywords.

If the `ngram_range` cannot be satisfied, *i.e.*, there are no keywords
for the lower end of `ngram_range`, a `RuntimeWarning` is raised and
an empty list is returned. In the above example, `ngram_range=(4, 5)` raises
a warning, *viz.*,
```bash
fast_rake/rake.py:189: RuntimeWarning: No keywords for ngram_range (4, 5). Returning empty list.
  warnings.warn(msg, RuntimeWarning)
```

## Example Use Case
The dataset are 2,225 BBC News articles 
from [BBC-Dataset-News-Classification]("https://github.com/suraj-deshmukh/BBC-Dataset-News-Classification/blob/master/dataset/data_files/sport")
(not included). `examples/bbc_news.py` represents a typical use case of 
finding keywords for each file in a collection.

```
bbc_news.py -i ~/BBC-Dataset-News-Classification-master/dataset/data_files/sport
run  1, time for 2,225 documents: 4.92681 secs

num docs: 2,225  avg num_runs=1  451.61 docs/sec
```
Of course, this is an *embarrassingly parallel* task amenable to multiprocessing.
`bbc_mp.py` demonstrates using `joblib` as the backend. This achieves a ~10x reduction in 
processing time (YMMV):
```
bbc_mp.py --dataset bbc --top-dir BBC-Dataset-News-Classification/dataset/data_files --njobs -1
running dataset: bbc
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 8 concurrent workers.
[Parallel(n_jobs=-1)]: Done   2 tasks        | elapsed:    0.2s
[Parallel(n_jobs=-1)]: Done  16 tasks        | elapsed:    0.2s
[Parallel(n_jobs=-1)]: Done  45 tasks        | elapsed:    0.3s
[Parallel(n_jobs=-1)]: Done 120 tasks        | elapsed:    0.3s
[Parallel(n_jobs=-1)]: Done 408 tasks        | elapsed:    0.3s
[Parallel(n_jobs=-1)]: Done 1528 tasks       | elapsed:    0.4s
[Parallel(n_jobs=-1)]: Done 2092 tasks       | elapsed:    0.4s
[Parallel(n_jobs=-1)]: Done 2168 tasks       | elapsed:    0.5s
[Parallel(n_jobs=-1)]: Done 2210 out of 2225 | elapsed:    0.5s remaining:    0.0s
[Parallel(n_jobs=-1)]: Done 2225 out of 2225 | elapsed:    0.5s finished

num docs: 2,225  time: 0.46857 secs  rate 4748.480 docs/sec
```

# License
Copyright &copy; 2022 Chris Skiscim. All rights reserved.

MIT License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


