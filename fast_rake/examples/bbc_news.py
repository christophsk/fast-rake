"""
usage: bbc_news.py [-h] [-i INPUT_DIR] [-n NRUNS]

BBC news example

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input-dir INPUT_DIR
                        top level directory for BBC news
  -n NRUNS, --nruns NRUNS
                        number of runs
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

import time

import fast_rake.examples.data_readers as readers
from fast_rake import Rake


def bbc_news(input_dir, n_runs):
    rake = Rake(stopword_name="smart")

    times = 0.0
    num_files = 0
    for run in range(n_runs):
        num_files = 0
        start_l = time.time()
        for _, doc in readers.gen_bbc_title_text(input_dir):
            _ = rake(doc)
            num_files += 1
        loop_t = time.time() - start_l
        times += loop_t
        print(
            "run {:>2d}, time for {:,} documents: {:0.5f} secs".format(
                run + 1, num_files, loop_t
            )
        )
    print(
        "\nnum docs: {:,}  num_runs={:,}  rate {:0.2f} docs/sec".format(
            num_files, n_runs, (n_runs * num_files) / times
        )
    )


if __name__ == "__main__":
    import sys

    from argparse import ArgumentParser

    parser = ArgumentParser(description="BBC news example")
    parser.add_argument(
        "-i",
        "--input-dir",
        dest="input_dir",
        help="top level directory for BBC news",
    )
    parser.add_argument(
        "-n",
        "--nruns",
        dest="nruns",
        default=1,
        type=int,
        help="number of runs",
    )
    args = parser.parse_args()

    sys.exit(bbc_news(args.input_dir, n_runs=args.nruns))
