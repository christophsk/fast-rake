"""
Single stop word
"""
import pytest

from fast_rake import Rake


@pytest.mark.parametrize("stop_name", ["google", "nltk", "sklearn", "smart"])
def test_custom_stopword(text, stop_name):
    custom_stopwords = ["minimal", "linear"]
    rake = Rake(stopword_name=stop_name, custom_stopwords=custom_stopwords)
    kw = rake(text)
    assert True not in [
        stop_word in k for k, _ in kw for stop_word in custom_stopwords
    ]
