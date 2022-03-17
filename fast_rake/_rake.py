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
import logging
import operator
import re
import warnings
from typing import List, Tuple

import fast_rake.optimized_stop_list as stops
import fast_rake.rake_alg as alg
import fast_rake.version as v

logger = logging.getLogger(__name__)


class Rake:
    """
    The typical use case is to use a base stopword list and optionally add
    custom stop words. Options to limit the size and nature of the returned
    keywords are documented below.

    The algorithm is implemented using `__call__` with a non-empty string
    (the document) as it's only argument.

     Args:
         stopword_name (str): one of ("google", "nltk", "sklearn", "smart");
            Default: "smart"

         custom_stopwords (list(str)|None): stopwords to add to the selected
            `stopword_name`; Default: None

        max_kw (int|None): number of keywords to return; if None, `top_percent`
            is used; Default: None

        ngram_range (tuple|None): keywords satisfying this range are ranked; if
            None, keywords of any length are ranked; Default: None.

        top_percent (float|None): fraction of the number of keywords returned;
            If None, max_kw is used NB: max_kw cannot be None in this case;
            Default: 1.0

    Raises:
        ValueError if arguments are incorrect

    Examples:
        >>> from fast_rake.rake import Rake
        >>>
        >>> rake = Rake(stopword_name="smart", custom_stopwords=None)
        >>>
        >>> text = "My lifeboat is full of eels."
        >>> rake(text)
        [('lifeboat', 1.0), ('full', 1.0), ('eels', 1.0)]
        >>>
        >>> # with custom stop word list
        >>> rake = Rake(stopword_name="smart", custom_stopwords=["full"])
        >>> rake(text)
        [('lifeboat', 1.0), ('eels', 1.0)]
        >>>
        >>> # ngram_range of (1, 3)
        >>> rake = Rake(ngram_range=(1, 3))
        >>> rake(text)
        [('lifeboat', 1.0), ('eels', 1.0)]
        >>>
        >>> # find the top 1% keywords
        >>> rake = Rake(top_percent=0.01)
        >>> rake(text)
        [('lifeboat', 1.0)]
    """

    __version__ = v.__version__

    def __init__(
        self,
        stopword_name: str = "smart",
        custom_stopwords: List = None,
        max_kw: int = None,
        ngram_range: tuple = None,
        top_percent: float = 1.0,
        kw_only: bool = False,
    ) -> None:

        self.supported_stopwords = ("google", "nltk", "sklearn", "smart")
        logger.info(
            "{} version {}".format(self.__class__.__name__, self.__version__)
        )

        if stopword_name not in self.supported_stopwords:
            msg = "Unsupported `stopword_name`; got {}. ".format(stopword_name)
            msg += "Please use one of {}".format(self.supported_stopwords)
            raise ValueError(
                "unknown `stopword_name`; got {}".format(stopword_name)
            )
        cs_len = 0
        if custom_stopwords is not None:
            if not custom_stopwords:
                raise ValueError("custom stopword list is empty")
            cs_len = len(custom_stopwords)
        if max_kw is not None:
            max_kw = int(max_kw)
            if max_kw < 1:
                msg = "invalid value for max_kw, got {}".format(max_kw)
                raise ValueError(msg)
        elif top_percent is not None:
            if not 0.0 < top_percent <= 1.0:
                msg = "top_percent must be between 0 and 1, got {}".format(
                    top_percent
                )
                raise ValueError(msg)

        self._stop_words_re = stops.load_stopwords(
            stopword_name, custom_stopwords, no_trailing=True,
        )
        logger.info("        stopword_name : {}".format(stopword_name))
        logger.info("num custom stop words : {:,}".format(cs_len))

        self.ngram_range = ngram_range
        self.max_kw = max_kw
        self.kw_only = kw_only
        self.top_percent = top_percent
        self.stop_words = stopword_name
        self.custom_stopwords = custom_stopwords

        if self.ngram_range is not None:
            if self.ngram_range[1] < self.ngram_range[0]:
                raise ValueError("improper ngram_range")

        # be faithful to the original implementation
        self._word_splitter = re.compile("[^a-zA-Z0-9_\\+\\-/]")
        self._sentence_splitter = re.compile(
            "[.!?,;:\t\\\\\"\\(\\)\\'\u2019\u2013]|\\s\\-\\s"
        )

    def __call__(self, input_text: str) -> List[Tuple[str, float]]:
        """
        Extract and rank the keywords from `input_text`.

        Args:
            input_text (str): Text from which keywords will be extracted and
                ranked.

        Returns:
           List[Tuple[str, float]]

        Raises:
            RuntimeWarning
        """
        if not isinstance(input_text, str):
            msg = "input_text must be type str; returning empty list"
            warnings.warn(msg, UserWarning)
            return []

        if not input_text.strip():
            msg = "input_text is empty; returning empty list"
            warnings.warn(msg, UserWarning)
            return []

        # algorithm begins
        sentence_list = alg.split_sentences(
            input_text, self._sentence_splitter
        )
        phrase_list = alg.gen_cand_keywords(sentence_list, self._stop_words_re)
        if self.ngram_range is not None:
            phrase_list = [
                p
                for p in phrase_list
                if self.ngram_range[0] <= len(p.split()) <= self.ngram_range[1]
            ]
        if not phrase_list:
            ngrams = "({}, {})".format(
                self.ngram_range[0], self.ngram_range[1]
            )
            msg = "No keywords for ngram_range " + ngrams + ". "
            msg += "Returning empty list."
            warnings.warn(msg, UserWarning)
            return []

        word_scores, phrase_words = alg.calc_word_scores(
            phrase_list, self._word_splitter
        )
        keyword_candidates = alg.calc_cand_keyword_scores(
            phrase_words, word_scores
        )
        sorted_keywords = sorted(
            keyword_candidates.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )

        # prepare output
        if self.max_kw is None:
            self.max_kw = max(1, int(len(sorted_keywords) * self.top_percent))
        if self.kw_only:
            return [kw for kw, _ in sorted_keywords[: self.max_kw]]
        else:
            return sorted_keywords[: self.max_kw]
