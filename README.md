# `fast-rake`

`fast-rake` is library for keyword extraction built to efficiently process large
collections of text. By using optimized regular expressions for stopwords 

The Rapid Automatic Keyword Extraction (RAKE) algorithm is 
an efficient, unsupervised method for which many implementations exist.
See [Rose, S., et al., (2010)](https://onlinelibrary.wiley.com/doi/10.1002/9780470689646.ch1) 
for a detailed description.

## Features

- Use of optimized regular expressions for splitting sentences into phrasal quantities.
  Included are optimized stopword lists from *google*, *nltk*, *scikit-learn*, and *SMART*.
  
- Allows for custom stopword lists to augment the built-in stop words.
  
- Python-specific optimizations to speed each step of the algorithm.
  
- No dependencies.

## Test & Install
If `pytest` is installed, tests can be via:

```bash
python -m pytest -v
```

To install:
```bash
python setup.py install
```

## Examples

The implementation uses `__call__`:
```
>>> from fast_rake.rake import Rake
>>>
>>> # default arguments are shown
>>> smart_rake = Rake(stopword_name="smart", custom_stopwords=None, max_kw=None, ngram_range=None, top_percent=1.0, kw_only=False)
>>>
>>> text = "My lifeboat is full of eels."
>>> smart_rake(text)
[('lifeboat', 1.0), ('full', 1.0), ('eels', 1.0)]
```

Custom stop word list with "smart" stopwords:
```
>>> smart_rake = Rake(stopword_name="smart", custom_stopwords=["full"])
>>> smart_rake(text)
[('lifeboat', 1.0), ('eels', 1.0)]
```

Here the `ngram_range` cannot be satisfied triggering a RuntimeWarning.
An empty list is returned:
```
>>> smart_rake = Rake(stopword_name="smart, ngram_range=(2, 3))
smart_rake(text)
RuntimeWarning: No keywords for ngram_range (2, 3) Returning empty list.
[]
```

Change the ngram_range to (1, 3) to avoid an empty list:
```
>>> smart_rake = Rake(stopword_name="smart, ngram_range=(1, 3), kw_only=True)
>>> smart_rake(text)
['lifeboat', 'full', 'eels']
```

Find the top 1% keywords:
```
>>> smart_rake = Rake(stopword_name="smart, top_percent=0.01, kw_only=True)
>>> smart_rake(text)
['lifeboat']
```

## Example Use Case
The test set was 511 BBC News "sport" articles 
from [BBC-Dataset-News-Classification]("https://github.com/suraj-deshmukh/BBC-Dataset-News-Classification/blob/master/dataset/data_files/sport")
(not included). `examples/bbc_news.py` represents a typical use case of 
finding keywords for each file in a collection. Timing for 10 runs are averaged.

```
bbc_news.py -i ~/BBC-Dataset-News-Classification-master/dataset/data_files/sport

num files : 511  avg time (10 runs) : 0.0018 secs / file
```

# License
MIT License

Copyright (c) 2017 - 2021, Chris Skiscim

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


