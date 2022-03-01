"""
usage: bbc_news.py [-h] [-i INPUT_DIR]

speed test

optional arguments:
  -h, --help    show this help message and exit
  -i INPUT_DIR
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
#
# https://github.com/suraj-deshmukh/BBC-Dataset-News-Classification
#
# Subdirectory:
#
# BBC-Dataset-News-Classification-master/dataset/data_files/sport

import os
import re
import time

from fast_rake import Rake


def bbc_news(input_dir, n_runs=10):
    rake = Rake(stopword_name="smart")
    times = 0.0
    nl = "\n{1,}"
    dot = "."

    f_list = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    num_files = len(f_list)
    print("number of documents {:,}".format(num_files))

    for run in range(n_runs):
        t_run = time.time()
        for test_file in f_list:
            with open(test_file, encoding="utf-8", errors="ignore") as f:
                text = f.read()
            # Specific to BBC News: "\n" => sentence
            text = re.sub(nl, dot, text)
            start = time.time()
            _ = rake(text)
            times += time.time() - start
        print(
            "run {:>2d}, time for {:,} documents: {:0.5f} secs".format(
                run + 1, num_files, time.time() - t_run
            )
        )
    print(
        "\nnum docs : {:,}  avg time/doc ({} runs) : {:0.4f} secs/doc".format(
            num_files, n_runs, times / (n_runs * num_files)
        )
    )


if __name__ == "__main__":
    import sys

    from argparse import ArgumentParser

    parser = ArgumentParser(description="speed test")
    parser.add_argument("-i", dest="input_dir")
    args = parser.parse_args()

    sys.exit(bbc_news(args.input_dir, n_runs=1))
