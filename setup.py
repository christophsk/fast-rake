# flake8: noqa
# pylint: skip-file

from os import path
from setuptools import setup, find_packages

__version__ = None
exec(open("fast_rake/version.py").read())

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()
    LONG_DESCRIPTION_TYPE = "text/markdown"

setup(
    name="fast-rake",
    version=__version__,
    python_requires=">=3.6",
    packages=find_packages(exclude=["test*"]),
    include_package_data=False,
    zip_safe=False,
    url="",
    download_url="",
    license="MIT",
    author="C Skiscim",
    author_email="",
    description="fast-rake: Optimized Keyword Extraction using RAKE",
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    keywords="keywords keyword-extraction rake nlp optimized",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
    ],
)
