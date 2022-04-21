import logging
import os
import re
from fnmatch import fnmatch

from sklearn.datasets import fetch_20newsgroups

nl_re = r"\n{1,}"
dash_re = r"[-_]{2,}"
space = " "
remove_20ng = ("headers", "footers", "quotes")

logger = logging.getLogger(__name__)


def _clean(text):
    text = re.sub(nl_re, space, text)
    return text.strip()


def walk_dirs(top_dir, filepat="*.txt"):
    for root, dirs, files in os.walk(top_dir, topdown=True):
        for f in files:
            if fnmatch(f, filepat):
                yield os.path.join(root, f)


def bbc_title_text(path_walker):
    for text_file in path_walker:
        with open(text_file, encoding="utf-8", errors="ignore") as fp:
            txt = fp.readlines()
        head, tail = os.path.split(text_file)
        tail = re.sub("\\.\\w+", "", tail)
        id_class = os.path.split(head)[-1]
        title = _clean(txt[0])
        docid = "-".join([id_class, tail, title])
        txt = space.join(txt[1:])
        txt = _clean(txt)
        if txt:
            yield docid, txt


def gen_bbc_title_text(top_dir, pat="*.txt"):
    bbc_walk = walk_dirs(top_dir, filepat=pat)
    for docid, text in bbc_title_text(bbc_walk):
        yield docid, text


def read_bbc_news(top_dir):
    """
    Read the BBC news corpus at `file_path`. The document ID is title
    (first line) and the document body are all subsequent lines.

    Args:
        top_dir (str): top-level directory holding the `.txt` files

    Returns:
        tuple(list, list)

    """
    docs = list()
    idx2docid = list()
    for docid, text in gen_bbc_title_text(top_dir):
        idx2docid.append(docid)
        docs.append(text)
    return docs, idx2docid


def read_20newsgroups(cats):
    remove = ("headers", "footers", "quotes")
    newsgroup_data = fetch_20newsgroups(
        subset="train", remove=remove, categories=cats, return_X_y=False
    )
    docs = list()
    target_names = list(newsgroup_data.target_names)
    idx2docid = list()
    dn = 0
    for doc, target in zip(newsgroup_data.data, newsgroup_data.target):
        doc = re.sub(nl_re, space, doc)
        doc = re.sub(dash_re, space, doc)
        doc = doc.strip()
        if not doc:
            continue
        docs.append(doc)
        dn += 1
        tn = "-".join([target_names[target], str(dn)])
        idx2docid.append(tn)
    return docs, idx2docid
