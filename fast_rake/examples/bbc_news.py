"""
usage: bbc_news.py [-h] [-i INPUT_DIR]

speed test

optional arguments:
  -h, --help    show this help message and exit
  -i INPUT_DIR


BBC News data is available at

https://github.com/suraj-deshmukh/BBC-Dataset-News-Classification

Subdirectory:

BBC-Dataset-News-Classification-master/dataset/data_files/sport

"""
import os
import time

from fast_rake.rake import Rake


def bbc_news(input_dir):
    n_runs = 10
    rake = Rake(stopword_name="smart")
    times = 0.0

    f_list = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    num_files = len(f_list)

    for run in range(n_runs):
        for test_file in f_list:
            with open(test_file, encoding="utf-8", errors="ignore") as f:
                text = f.read()
            start = time.time()
            _ = rake(text)
            times += time.time() - start
        print("run {:>2d}".format(run + 1))
    print(
        "\nnum docs : {:,}  avg time / doc ({} runs) : {:0.4f} secs / doc".format(  # noqa
            num_files, n_runs, times / (n_runs * num_files)
        )
    )


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="speed test")
    parser.add_argument("-i", dest="input_dir")
    args = parser.parse_args()
    bbc_news(args.input_dir)
