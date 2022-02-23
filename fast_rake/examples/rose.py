from fast_rake import Rake
from pprint import pprint

text = (
    "Compatibility of systems of linear constraints over the set of "
    "natural numbers. Criteria of compatibility of a system of linear "
    "Diophantine equations, strict inequations, and nonstrict inequations "
    "are considered. Upper bounds for components of a minimal set of "
    "solutions and algorithms of construction of minimal generating sets "
    "of solutions for all types of systems are given. These criteria and "
    "the corresponding algorithms for constructing a minimal supporting "
    "set of solutions can be used in solving all the considered types of "
    "systems and systems of mixed types."
)

# default arguments are shown
smart_rake = Rake(
    stopword_name="smart",
    custom_stopwords=None,
    max_kw=None,
    ngram_range=None,
    top_percent=1.0,
    kw_only=False,
)

kw = smart_rake(text)
pprint(kw)
