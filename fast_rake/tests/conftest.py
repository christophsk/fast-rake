# flake8: noqa
# pylint: skip-file

import pytest
import logging

from fast_rake.rake import Rake

log_fmt = "[%(asctime)s %(levelname)-8s] [%(filename)s:%(lineno)s"
log_fmt += " - %(funcName)s()] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_fmt)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def supported_stops():
    rake = Rake()
    return rake.supported_stopwords


@pytest.fixture(scope="session")
def rake_smart():
    return Rake(stopword_name="smart")


@pytest.fixture(scope="session")
def rake_nltk():
    return Rake(stopword_name="nltk")


@pytest.fixture(scope="session")
def rake_google():
    return Rake(stopword_name="google")


@pytest.fixture(scope="session")
def rake_sklearn():
    return Rake(stopword_name="sklearn")


@pytest.fixture(scope="session")
def all_rake_objects():
    return rake_nltk, rake_google, rake_smart, rake_sklearn


@pytest.fixture(scope="session")
def text():
    return "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types."  # noqa


# This is taken from the Rose et al. article and constitutes a known answer.
@pytest.fixture(scope="session")
def nltk_all():
    return [
        ("minimal generating sets", 8.666666666666666),
        ("linear Diophantine equations", 8.5),
        ("minimal supporting set", 7.666666666666666),
        ("minimal set", 4.666666666666666),
        ("linear constraints", 4.5),
        ("natural numbers", 4.0),
        ("strict inequations", 4.0),
        ("nonstrict inequations", 4.0),
        ("Upper bounds", 4.0),
        ("mixed types", 3.666666666666667),
        ("corresponding algorithms", 3.5),
        ("considered types", 3.166666666666667),
        ("set", 2.0),
        ("types", 1.6666666666666667),
        ("considered", 1.5),
        ("algorithms", 1.5),
        ("Compatibility", 1.0),
        ("systems", 1.0),
        ("Criteria", 1.0),
        ("compatibility", 1.0),
        ("system", 1.0),
        ("components", 1.0),
        ("solutions", 1.0),
        ("construction", 1.0),
        ("given", 1.0),
        ("criteria", 1.0),
        ("constructing", 1.0),
        ("used", 1.0),
        ("solving", 1.0),
    ]


@pytest.fixture(scope="session")
def smart_all():
    return [
        ("minimal generating sets", 8.666666666666666),
        ("linear Diophantine equations", 8.5),
        ("minimal supporting set", 7.666666666666666),
        ("minimal set", 4.666666666666666),
        ("linear constraints", 4.5),
        ("natural numbers", 4.0),
        ("strict inequations", 4.0),
        ("nonstrict inequations", 4.0),
        ("Upper bounds", 4.0),
        ("mixed types", 3.666666666666667),
        ("considered types", 3.166666666666667),
        ("set", 2.0),
        ("types", 1.6666666666666667),
        ("considered", 1.5),
        ("Compatibility", 1.0),
        ("systems", 1.0),
        ("Criteria", 1.0),
        ("compatibility", 1.0),
        ("system", 1.0),
        ("components", 1.0),
        ("solutions", 1.0),
        ("algorithms", 1.0),
        ("construction", 1.0),
        ("criteria", 1.0),
        ("constructing", 1.0),
        ("solving", 1.0),
    ]


@pytest.fixture(scope="session")
def google_all():
    return [
        ("constructing a minimal supporting set", 20.0),
        ("a minimal set", 10.0),
        ("minimal generating sets", 9.666666666666666),
        ("linear Diophantine equations", 8.5),
        ("a system", 5.333333333333334),
        ("linear constraints", 4.5),
        ("natural numbers", 4.0),
        ("strict inequations", 4.0),
        ("nonstrict inequations", 4.0),
        ("Upper bounds", 4.0),
        ("mixed types", 3.666666666666667),
        ("corresponding algorithms", 3.5),
        ("solutions can", 3.333333333333333),
        ("considered types", 3.166666666666667),
        ("set", 3.0),
        ("types", 1.6666666666666667),
        ("considered", 1.5),
        ("algorithms", 1.5),
        ("solutions", 1.3333333333333333),
        ("Compatibility", 1.0),
        ("systems", 1.0),
        ("Criteria", 1.0),
        ("compatibility", 1.0),
        ("components", 1.0),
        ("construction", 1.0),
        ("given", 1.0),
        ("criteria", 1.0),
        ("used", 1.0),
        ("solving", 1.0),
    ]


@pytest.fixture(scope="session")
def sklearn_all():
    return [
        ("minimal generating sets", 8.666666666666666),
        ("linear Diophantine equations", 8.5),
        ("minimal supporting set", 7.666666666666666),
        ("minimal set", 4.666666666666666),
        ("linear constraints", 4.5),
        ("natural numbers", 4.0),
        ("strict inequations", 4.0),
        ("nonstrict inequations", 4.0),
        ("Upper bounds", 4.0),
        ("mixed types", 3.666666666666667),
        ("corresponding algorithms", 3.5),
        ("considered types", 3.166666666666667),
        ("set", 2.0),
        ("types", 1.6666666666666667),
        ("considered", 1.5),
        ("algorithms", 1.5),
        ("Compatibility", 1.0),
        ("systems", 1.0),
        ("Criteria", 1.0),
        ("compatibility", 1.0),
        ("components", 1.0),
        ("solutions", 1.0),
        ("construction", 1.0),
        ("given", 1.0),
        ("criteria", 1.0),
        ("constructing", 1.0),
        ("used", 1.0),
        ("solving", 1.0),
    ]


@pytest.fixture(scope="session")
def all_ans():
    return nltk_all, google_all, sklearn_all, smart_all


@pytest.fixture(scope="session")
def med_text_expected():
    return [
        ("inducible tissue-specific knockout model", 16.0),
        ("received bone marrow transplants", 15.066666666666666),
        ("smooth muscle gene expression", 14.857142857142858),
        ("femoral artery wire injury", 14.333333333333334),
        ("receive bone marrow transplants", 14.066666666666666),
        ("smooth muscle cells mediates", 13.957142857142857),
        ("decreasing resident smc migration", 13.5),
        ("vascular smooth muscle cells", 12.957142857142857),
        ("neointima formation occurs frequently", 12.722222222222221),
        ("inducible ppar3 knockout mice", 12.041666666666666),
    ]


@pytest.fixture(scope="session")
def med_text():
    return "The goal of this project is to define the role of peroxisome proliferator-activated receptor (PPAR)3 activation in neointima formation. Neointima formation occurs frequently after angioplasty and causes significant morbidity; vascular smooth muscle cells (SMCs) are key cells during neointima formation. We will study the effects of two clinically available agents on SMC biology and neointima formation. PPAR3 is a ligand-activated nuclear receptor that has been shown to have beneficial effects on vascular disorders. We will compare the effects of two agents: pioglitazone (activates PPAR3 only) and bexarotene (an RXR agonist which activates PPAR3, PPAR1, PPAR4, LXR, and FXR). Our hypothesis is that PPAR3 activation specifically in smooth muscle cells (SMC) will reduce neointima formation by decreasing resident SMC migration and proliferation as well as SMC-derived chemokine production and subsequent recruitment of bone marrow-derived cells. We believe both pioglitazone and bexarotene will be effective but bexarotene may be more effective due to activation of other nuclear receptors. In Aim One, we will compare the effects of pioglitazone to bexarotene on SMCs. We will measure changes in proliferation, cytokine production, and smooth muscle gene expression. In Aim Two, we will determine if the agents affect levels of microRNAs crucial to maintaining SMC phenotype, such as miR- 143, miR-145, and miR-221. In Aim Three, we will examine the effects of the agents in vivo during femoral artery wire injury. To track recruitment of bone-marrow derived cells to the site of arterial injury, all mice will receive bone marrow transplants from a GFP positive donor. After wire injury, mice will be analyzed at multiple time points. Along with neointima size, we will measure production of chemokines (IL-6, MCP-1, SDF-11, and KC), recruitment of bone marrow-derived cells and macrophages, and cellular proliferation. We also plan to study the role of PPAR3 activation specifically in smooth muscle cells during neointima formation. Using an inducible tissue-specific knockout model, we will deplete PPAR3 in smooth muscle cells after mice have received bone marrow transplants from GFP positive donors. Inducible PPAR3 knockout mice and control mice will receive therapy with either pioglitazone, bexarotene or control and be subjected to femoral artery wire injury. At multiple time points, neointima size will again be measured. All mice used in Aim 3B will have the R26R reporter allele in which smooth muscle cells are labeled with 2-galactosidase. Since we can measure both bone marrow derived and resident SMCs, we will determine the relative contribution each cell type makes to the neointima. We will also be able to determine if PPAR3 specifically in smooth muscle cells mediates the effects of bexarotene or pioglitazone."  # noqa


@pytest.fixture(scope="session")
def long_text():
    text_content = """
    Sources tell us that Google is acquiring Kaggle, a platform that
    hosts data science and machine learning competitions. Details about
    the transaction remain somewhat vague , but given that Google is hosting
    its Cloud Next conference in San Francisco this week, the official announcement
    could come as early    as tomorrow.  Reached by phone, Kaggle co-founder
    CEO Anthony Goldbloom declined to deny that the
    acquisition is happening. Google itself declined 'to comment on rumors'.
    Kaggle, which has about half a million data scientists on its platform,
    was founded by Goldbloom    and Ben Hamner in 2010. The service got an
    early start and even though it has a few competitors    like DrivenData,
    TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its
    specific niche. The service is basically the de facto home for running data science
    and machine learning    competitions.  With Kaggle, Google is buying one of the largest
    and most active communities for    data scientists - and with that, it will get increased
    mindshare in this community, too    (though it already has plenty of that thanks to Tensorflow
    and other projects).    Kaggle has a bit of a history with Google, too, but that's pretty recent.
    Earlier this month,    Google and Kaggle teamed up to host a $100,000 machine learning competition
    around classifying    YouTube videos. That competition had some deep integrations with the
    Google Cloud Platform, too.    Our understanding is that Google will keep the service running -
    likely under its current name.    While the acquisition is probably more about Kaggle's community
    than technology, Kaggle did build    some interesting tools for hosting its competition and 'kernels',
    too. On Kaggle, kernels are    basically the source code for analyzing data sets and developers can
    share this code on the    platform (the company previously called them 'scripts').  Like similar
    competition-centric sites,    Kaggle also runs a job board, too. It's unclear what Google will do
    with that part of the service.    According to Crunchbase, Kaggle raised $12.5 million (though PitchBook
    says it's $12.75) since its    launch in 2010. Investors in Kaggle include Index Ventures, SV Angel,
    Max Levchin, Naval Ravikant,    Google chief economist Hal Varian, Khosla Ventures and Yuri Milner
    """
    return text_content.replace("\n", " ")
