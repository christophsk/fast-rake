"""
Test basic functionality
"""
import logging
import pytest
from fast_rake import Rake

logger = logging.getLogger(__name__)


def check(expected, actual, kw_only):
    if kw_only:
        expect = [a for a, _ in expected]
        assert False not in [a in expect for a in actual], actual
    else:
        assert False not in [a in expected for a in actual], actual


@pytest.mark.parametrize("top_p", [1.0, 0.01])
def test_known_stops(
    text, top_p, supported_stops, nltk_all, google_all, sklearn_all, smart_all,
):
    all_ans = (google_all, nltk_all, sklearn_all, smart_all)
    for stop_name, ans in zip(supported_stops, all_ans):
        rake = Rake(stopword_name=stop_name, kw_only=True, top_percent=top_p)
        kw = rake(text)
        if top_p < 1.0:
            assert len(kw) > 0
        else:
            check(ans, kw, True)


def test_ngram_stops(text, supported_stops):
    ng = (2, 2)
    for stop_name in supported_stops:
        rake = Rake(stopword_name=stop_name, ngram_range=ng, kw_only=True)
        kws = rake(text)
        for kw in kws:
            assert ng[0] <= len(kw.split()) <= ng[1]
