# MIT License
# Copyright (c) 2017 - 2021, Chris Skiscim
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
import functools
import logging
from collections import defaultdict
from itertools import chain
from typing import Pattern, Iterator, List, Tuple

import fast_rake.optimized_stop_list as stops

logger = logging.getLogger(__name__)

PERIOD = "."


def add(x: float, y: float) -> float:
    return x + y


def is_number(s: str) -> bool:
    try:
        float(s) if PERIOD in s else int(s)
        return True
    except ValueError:
        return False


def separate_words(text: str, splitter: Pattern) -> List[str]:
    return [
        w.strip()
        for w in splitter.split(text)
        if w.strip() and not is_number(w)
    ]


def split_sentences(text: str, sentence_delimiters: Pattern) -> List[str]:
    return sentence_delimiters.split(text)


def gen_cand_keywords(sentence_list: list, stopword_re: Pattern) -> Iterator:
    return chain.from_iterable(
        [stops.split_on_stopwords(s, stopword_re) for s in sentence_list]
    )


def calc_word_scores(
    phrase_list: list, splitter: Pattern
) -> Tuple[dict, list]:
    word_frequency = defaultdict(int)
    word_degree = defaultdict(int)
    phrase_words = list()

    for phrase in phrase_list:
        word_list = [
            w.strip()
            for w in splitter.split(phrase)
            if w.strip() and not is_number(w)
        ]
        word_list_degree = len(word_list) - 1
        phrase_words.append((phrase, word_list))

        for word in word_list:
            word_frequency[word] += 1
            word_degree[word] += word_list_degree  # orig.

    for wf in word_frequency:
        word_degree[wf] = word_degree[wf] + word_frequency[wf]

    word_score = {
        w: word_degree[w] / word_frequency[w] for w in word_frequency
    }
    return word_score, phrase_words


def calc_cand_keyword_scores(phrase_words: list, word_score: dict) -> dict:
    kw_score = dict()
    for phrase, word_list in phrase_words:
        if not word_list:
            continue
        candidate_score = functools.reduce(
            add, [word_score[word] for word in word_list]
        )
        kw_score[phrase] = candidate_score
    return kw_score
