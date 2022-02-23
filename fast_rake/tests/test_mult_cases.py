"""
Corner cases
"""
import pytest

from fast_rake import Rake


@pytest.mark.parametrize(
    "stop_list, case, exp_len, top_p",
    [
        ("nltk", "econtainer", 1, 1.0),
        ("nltk", "econtainers", 1, 1.0),
        ("nltk", "of", 0, 1.0),
        ("nltk", "?", 0, 0.2),
        ("smart", "econtainer", 1, 1.0),
        ("smart", "econtainers", 1, 1.0),
        ("smart", "of", 0, 0.3),
        ("smart", "?", 0, 0.3),
        ("smart", r"\n\t", 0, 0.3),
    ],
)
def test_cases(stop_list, case, exp_len, top_p):
    rake = Rake(stopword_name=stop_list, top_percent=top_p)
    kw = rake(input_text=case)
    assert len(kw) == exp_len, kw


def test_bad_top_p(text):
    with pytest.raises(ValueError):
        Rake(top_percent=-1.0)
