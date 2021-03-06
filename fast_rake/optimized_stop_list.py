# MIT License
# Copyright (c) 2017 - 2022, Chris Skiscim
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
import re
from typing import Pattern


def split_on_stopwords(string: str, stops_re: Pattern) -> list:
    tmp = re.sub(stops_re, "|", string.strip())
    phrases = tmp.split("|")
    return [p.strip() for p in phrases if p.strip()]


def compile_stops_regex(regex: str, no_trailing: bool) -> Pattern:
    if no_trailing:
        regex = r"\b" + regex + r"(?![\w-])"
    else:
        regex = r"\b" + regex + r"\b"
    return re.compile(regex, re.I)


def load_stopwords(
    stop_name: str, customs: list, no_trailing: bool
) -> Pattern:
    if stop_name == "nltk":
        stop_re = nltk_optimized()
    elif stop_name == "google":
        stop_re = google_optimized()
    elif stop_name == "sklearn":
        stop_re = sklearn_optimized()
    elif stop_name == "smart":
        stop_re = smart_optimized()
    else:
        raise ValueError("unsupported name; got {}".format(stop_name))

    if customs:
        stop_re = stop_re[:-1]
        customs_re = "|".join([c for c in customs if c.strip()])
        stop_re += "|" + customs_re + ")"
    return compile_stops_regex(stop_re, no_trailing)


def nltk_optimized() -> str:
    regex = "(?:w(?:h(?:i(?:ch|le)|e(?:re|n)|om?|at|y)|o(?:uldn(?:'t)?|n(?:'t)?)|e(?:re(?:n(?:'t)?)?)?|as(?:n(?:'t)?)?|i(?:ll|th))|h(?:a(?:v(?:e(?:n(?:'t)?)?|ing)|d(?:n(?:'t)?)?|s(?:n(?:'t)?)?)|e(?:r(?:s(?:elf)?|e)?)?|i(?:m(?:self)?|s)|ow)|t(?:h(?:e(?:[ny]|m(?:selves)?|[rs]e|irs?)?|a(?:t(?:'ll)?|n)|rough|ose|is)|o?o)?|a(?:[mst]|re(?:n(?:'t)?)?|bo(?:ut|ve)|gain(?:st)?|n[dy]?|fter|in|ll)?|s(?:h(?:ould(?:n(?:'t)?|'ve)?|an(?:'t)?|e(?:'s)?)|o(?:me)?|ame|uch)?|d(?:o(?:es(?:n(?:'t)?)?|n(?:'t)?|ing|wn)?|id(?:n(?:'t)?)?|uring)?|o(?:u(?:r(?:(?:selve)?s)?|t)|(?:(?:th|v)e)?r|n(?:ce|ly)?|f?f|wn)?|m(?:[ae]|ightn(?:'t)?|ustn(?:'t)?|o(?:re|st)|y(?:self)?)?|b(?:e(?:(?:caus|for)e|(?:twe)?en|ing|low)?|oth|ut|y)|y(?:ou(?:r(?:s(?:el(?:ves|f))?)?|'(?:[rv]e|ll|d))?)?|i(?:t(?:s(?:elf)?|'s)?|s(?:n(?:'t)?)?|n(?:to)?|f)?|f(?:(?:urthe|o)r|rom|ew)|n(?:eedn(?:'t)?|o[rtw]?)|c(?:ouldn(?:'t)?|an)|u(?:n(?:der|til)|p)|ve(?:ry)?|each|just|ll|re)"  # noqa
    return regex


def google_optimized() -> str:
    regex = "(?:w(?:h(?:e(?:re(?:'s)?|n(?:'s)?)|i(?:ch|le)|o(?:'s|m)?|at(?:'s)?|y(?:'s)?)|e(?:'(?:(?:v|r)e|ll|d)|re(?:n't)?)?|o(?:uld(?:n't)?|n't)|as(?:n't)?|ith)|h(?:e(?:r(?:s(?:elf)|e(?:'s)?)?|'(?:[ds]|ll))?|a(?:v(?:e(?:n't)?|ing)|d(?:n't)?|s(?:n't)?)|i(?:m(?:self)?|s)|ow(?:'s)?)|t(?:h(?:e(?:y(?:'(?:[rv]e|ll|d))?|re(?:'s)?|mselves|irs?|se|n)?|a(?:t(?:'s)?|n)|rough|em|ose|is)|o?o)|o(?:u(?:r(?:(?:selve)?s)?|(?:gh)?t)|(?:(?:th|v)e)?r|n(?:c e|ly)?|f?f|wn)|s(?:h(?:e(?:'(?:[ds]|ll))?|ould(?:n't)?|an't)|o(?:me)?|ame|uch)|i(?:t(?:s(?:elf)?|'s)?|'(?:[dm]|ll|ve)|s(?:n't)?|n(?:to)?|f)?|a(?:[mst]|bo(?:ut|ve)|gain(?:st)?|re(?:n't)?|n[dy]?|fter|ll)|b(?:e(?:(?:caus|for)e|(?:twe)?en|ing|low)?|oth|ut|y)|yo(?:u(?:r(?:sel(?:ves|f))?|'(?:[rv]e|ll|d))?| urs)|d(?:o(?:es(?:n't)?|ing|n't|wn)?|id(?:n't)|uring)|m(?:o(?:re|st)|y(?:self)?|ustn't|e)|c(?:ould(?:n't)?|an(?:no|')t)|f(?:(?:urthe|o)r|rom|ew)|u(?:n(?:der|til)|p)|no[rt]?|let's|each|very)"  # noqa
    return regex


def sklearn_optimized() -> str:
    regex = "(?:t(?:h(?:e(?:re(?:(?:upo|i)n|after|fore|by)?|m(?:selves)?|n(?:ce)?|ir|se|y)?|r(?:ough(?:out)?|ee|u)|i(?:[ns]|ck|rd)|o(?:ugh|se)|a[nt]|us)|o(?:[op]|gether|wards?)?|w(?:e(?:lve|nty)|o)|ake|en)|a(?:n(?:y(?:w(?:here|ay)|thing|how|one)?|other|d)?|l(?:on[eg]|though|ready|most|ways|so|l)|m(?:o(?:un(?:gs)?t|ng(?:st)?))?|fter(?:wards)?|bo(?:ut|ve)|gain(?:st)?|r(?:ound|e)|(?:cros)?s|t)?|w(?:h(?:e(?:re(?:a(?:fter|s)|(?:upo|i)n|ver|by)?|n(?:ever|ce)?|ther)|o(?:[ls]e|ever|m)?|i(?:ther|ch|le)|at(?:ever)?|y)|i(?:th(?:out|in)?|ll)|e(?:ll|re)?|ould|as)|s(?:o(?:me(?:t(?:imes?|hing)|(?:wher|on)e|how)?)?|e(?:e(?:m(?:ing|ed|s)?)?|rious|veral)|i(?:(?:nc(?:er)?|d)e|x(?:ty)?)|h(?:o(?:uld|w)|e)|ystem|till|ame|uch)|b(?:e(?:c(?:om(?:es?|ing)|a(?:us|m)e)|fore(?:hand)?|(?:hi|yo)nd|(?:twe)?en|sides?|ing|low)?|ot(?:tom|h)|ack|ill|ut|y)|h(?:e(?:r(?:e(?:(?:upo|i)n|after|by)?|s(?:elf)?)?|nce)?|a(?:s(?:nt)?|ve|d)|i(?:m(?:self)?|s)|ow(?:ever)?|undred)|e(?:ve(?:r(?:y(?:(?:wher|on)e|thing)?)?|n)|l(?:s(?:ewher)?e|even)|i(?:ther|ght)|(?:noug|ac)h|xcept|mpty|tc|g)|f(?:i(?:ft(?:een|y)|r(?:st|e)|ll|nd|ve)|o(?:r(?:mer(?:ly)?|ty)?|u(?:nd|r))|u(?:rther|ll)|ro(?:nt|m)|ew)|m(?:o(?:re(?:over)?|st(?:ly)?|ve)|i(?:ght|ll|ne)|(?:eanwhil)?e|a(?:n?y|de)|u(?:ch|st)|y(?:self)?)|n(?:o(?:t(?:hing)?|w(?:here)?|body|o?ne|r)?|e(?:ver(?:theless)?|ither|xt)|ame(?:ly)?|ine)|o(?:u(?:r(?:(?:selve)?s)?|t)|n(?:c?e|ly|to)?|ther(?:wise|s)?|f(?:ten|f)?|(?:ve)?r|wn)|i(?:[efs]|n(?:t(?:erest|o)|deed|c)?|t(?:s(?:elf)?)?)?|c(?:a(?:n(?:(?:no)?t)?|ll)|o(?:uld(?:nt)?|n)?|ry)|d(?:e(?:scribe|tail)?|o(?:ne|wn)?|u(?:ring|e))|l(?:a(?:tter(?:ly)?|st)|e(?:ast|ss)|td)|y(?:ou(?:r(?:s(?:el(?:ves|f))?)?)?|et)|p(?:er(?:haps)?|(?:ar|u)t|lease)|u(?:n(?:der|til)?|p(?:on)?|s)|g(?:ive|et|o)|r(?:ather|e)|v(?:ery|ia)|keep)"  # noqa
    return regex


def smart_optimized() -> str:
    regex = "(?:a(?:n(?:y(?:w(?:ays?|here)|thing|body|how|one)?|other|d)?|l(?:l(?:ows?)?|on[eg]|though|ready|most|ways|so)|p(?:p(?:r(?:opr|ec)iate|ear)|art)|c(?:cording(?:ly)?|tually|ross)|s(?:k(?:ing)?|sociated|ide)?|r(?:e(?:n't)?|ound)|b(?:o(?:ut|ve)|le)|m(?:ong(?:st)?)?|fter(?:wards)?|w(?:full|a)y|gain(?:st)?|(?:in')?t|vailable|'s)?|t(?:h(?:e(?:re(?:(?:upo|i)n|after|fore|'?s|by)?|y(?:'(?:[rv]e|ll|d))?|m(?:selves)?|n(?:ce)?|irs?|se)?|a(?:n(?:ks?|x)?|t(?:'?s)?)|o(?:rough(?:ly)?|ugh|se)|r(?:ough(?:out)?|ee|u)|i(?:nk|rd|s)|us)?|r(?:y(?:ing)?|ie[ds]|uly)|o(?:gether|wards?|ok?)?|e(?:nds|ll)|w(?:ice|o)|aken?|'s)?|s(?:e(?:e(?:m(?:ing|ed|s)?|ing|n)?|n(?:sible|t)|rious(?:ly)?|cond(?:ly)?|ve(?:ral|n)|l(?:ves|f))|o(?:me(?:t(?:imes?|hing)|wh(?:ere|at)|body|how|one)?|rry|on)?|a(?:y(?:ing|s)?|id|me|w)|h(?:ould(?:n't)?|all|e)|pecif(?:y(?:ing)?|ied)|u(?:[bp]|ch|re)|i(?:nce|x)|till)?|w(?:h(?:e(?:re(?:a(?:fter|s)|(?:upo|i)n|ver|'s|by)?|n(?:ever|ce)?|ther)|o(?:[ls]e|ever|'s|m)?|i(?:ther|ch|le)|at(?:ever|'s)?|y)|e(?:'(?:[rv]e|ll|d)|l(?:come|l)|re(?:n't)?|nt)?|i(?:th(?:out|in)?|ll(?:ing)?|sh)|o(?:n(?:der|'t)|uld(?:n't)?)|a(?:s(?:n't)?|nts?|y))?|c(?:o(?:n(?:s(?:ider(?:ing)?|equently)|tain(?:ing|s)?|cerning)|u(?:ld(?:n't)?|rse)|rresponding|m(?:es?)?)?|a(?:n(?:(?:no|')?t)?|uses?|me)|(?:urrent|lear)ly|ertain(?:ly)?|'(?:mon|s)|hanges)?|h(?:e(?:r(?:e(?:(?:upo|i)n|after|'s|by)?|s(?:elf)?)?|l(?:lo|p)|nce|'s)?|a(?:v(?:e(?:n't)?|ing)|d(?:n't)?|s(?:n't)?|ppens|rdly)|o(?:w(?:beit|ever)?|pefully)|i(?:m(?:self)?|ther|s)?)?|i(?:n(?:d(?:icate[ds]?|eed)|s(?:ofar|tead)|asmuch|ward|ner|to|c)?|t(?:'(?:[ds]|ll)|s(?:elf)?)?|'(?:[dm]|ll|ve)|(?:mmediat)?e|s(?:n't)?|gnored|f)?|e(?:ve(?:r(?:y(?:(?:wher|on)e|thing|body)?)?|n)|x(?:a(?:ctly|mple)|cept)?|n(?:tirely|ough)|i(?:ther|ght)|ls(?:ewher)?e|specially|ach|tc?|du|g)?|n(?:o(?:r(?:mally)?|t(?:hing)?|w(?:here)?|body|ne?|one|vel)?|e(?:ver(?:theless)?|ar(?:ly)?|cessary|ither|eds?|xt|w)|ame(?:ly)?|ine|d)?|o(?:[hr]|u(?:r(?:(?:selve)?s)?|t(?:side)?|ght)|n(?:es?|ce|ly|to)?|ther(?:wise|s)?|f(?:ten|f)?|ver(?:all)?|bviously|k(?:ay)?|ld|wn)?|b(?:e(?:c(?:om(?:es?|ing)|a(?:us|m)e)|fore(?:hand)?|t(?:ween|ter)|l(?:ieve|ow)|s(?:ides?|t)|(?:hi|yo)nd|ing|en)?|rief|oth|ut|y)?|d(?:o(?:wn(?:wards)?|es(?:n't)?|n(?:'t|e)|ing)?|e(?:s(?:cribed|pite)|finitely)|i(?:d(?:n't)?|fferent)|uring)?|m(?:o(?:re(?:over)?|st(?:ly)?)|a(?:(?:inl|n)y|y(?:be)?)|e(?:an(?:while)?|rely)?|u(?:ch|st)|y(?:self)?|ight)?|l(?:a(?:t(?:ter(?:ly)?|e(?:ly|r))|st)|e(?:t(?:'s)?|s[st]|ast)|i(?:ke(?:ly|d)?|ttle)|ook(?:ing|s)?|td)?|u(?:n(?:l(?:ikely|ess)|fortunately|t(?:il|o)|der)?|s(?:e(?:[ds]|ful)?|ually|ing)?|p(?:on)?|ucp)?|f(?:o(?:r(?:mer(?:ly)?|th)?|llow(?:ing|ed|s)|ur)|i(?:fth|rst|ve)|urther(?:more)?|rom|ar|ew)?|p(?:r(?:o(?:bably|vides)|esumably)|l(?:aced|ease|us)|articular(?:ly)?|er(?:haps)?|ossible)?|r(?:e(?:(?:(?:spec|la)tive|a(?:sonab|l))ly|gard(?:(?:les)?s|ing))?|ather|ight|d)?|g(?:o(?:t(?:ten)?|ing|es|ne)?|et(?:ting|s)?|reetings|ive[ns])?|y(?:ou(?:r(?:s(?:el(?:ves|f))?)?|'(?:[rv]e|ll|d))?|e[st])?|v(?:a(?:rious|lue)|i[az]|ery|s)?|k(?:e(?:eps?|pt)|now[ns]?)?|q(?:u(?:it)?e|v)?|j(?:ust)?|z(?:ero)?|x)"  # noqa
    return regex
