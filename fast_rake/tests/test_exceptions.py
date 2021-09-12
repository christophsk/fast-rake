import pytest
from fast_rake.rake import Rake


def test_bad_sw():
    with pytest.raises(ValueError):
        Rake(stopword_name="foo")


@pytest.mark.parametrize("bad_text", [12345, "", "  "])
def test_illegal_text(rake_google, bad_text):
    assert len(rake_google(bad_text)) == 0


def test_empty_custom_stopwords():
    with pytest.raises(ValueError):
        Rake(stopword_name="smart", custom_stopwords=[])
