"""
usage: bbc_mp.py

Multiprocessing example

optional arguments:
  -h, --help            show this help message and exit
  -d {bbc,20newsgroups}, --dataset {bbc,20newsgroups}
                        One of ('bbc', '20newsgroups')
  -t TOP_DIR, --top-dir TOP_DIR
                        BBC dataset top level directory
  -n NJOBS, --njobs NJOBS
                        number of jobs; the default (-1) uses all available
                        CPUs.
"""
# MIT License
# Copyright (c) 2017-2022, Chris Skiscim
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------
# BBC News data is available at
# https://github.com/suraj-deshmukh/BBC-Dataset-News-Classification
import logging

from joblib import Parallel, delayed

import fast_rake.examples.data_readers as reader
from fast_rake import Rake

logger = logging.getLogger(__name__)

rake_kw = Rake(stopword_name="smart", top_percent=1.0, kw_only=True)


def rake_extractor(doc):
    return rake_kw(doc)


def run_dataset(dataset, top_dir, njobs):
    if dataset == "bbc":
        idx2docid = list()

        # local generator to iterate over docs only
        def bbc_docs():
            for doc, docid in reader.gen_bbc_title_text(top_dir):
                idx2docid.append(docid)
                yield doc
        doc_iterable = bbc_docs()
    elif dataset == "20newsgroups":
        docs, idx2docid = reader.read_20newsgroups(cats=None)
        doc_iterable = docs
    else:
        raise ValueError(f"no dataset '{dataset}'")

    doc_kws = Parallel(n_jobs=njobs, prefer="processes", verbose=9)(
        delayed(rake_extractor)(doc) for doc in doc_iterable
    )
    return idx2docid, doc_kws


if __name__ == "__main__":
    from argparse import ArgumentParser
    import os
    import time

    allowed = ("bbc", "20newsgroups")

    parser = ArgumentParser(
        description="Multiprocessing example", usage="bbc_mp.py"
    )
    parser.add_argument(
        "-d",
        "--dataset",
        choices=allowed,
        dest="dataset",
        help="One of " + str(allowed),
    )
    parser.add_argument(
        "-t",
        "--top-dir",
        dest="top_dir",
        help="BBC dataset top level directory"
    )
    parser.add_argument(
        "-n",
        "--njobs",
        dest="njobs",
        default=-1,
        type=int,
        help="number of jobs; the default (-1) uses all available CPUs.",
    )
    args = parser.parse_args()
    if args.dataset == "bbc" and not os.path.isdir(args.top_dir):
        raise ValueError(f"no directory named {args.top_dir}")

    print(f"running dataset: {args.dataset}")
    start = time.time()
    _, kws = run_dataset(args.dataset, args.top_dir, args.njobs)
    elapsed = time.time() - start
    print(
        "\nnum docs: {:,}  time: {:0.5f} secs  rate {:0.2f} docs/sec".format(
            len(kws), elapsed, len(kws) / elapsed
        )
    )
