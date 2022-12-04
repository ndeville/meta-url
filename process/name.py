# process/name

# import spacy
from thefuzz import fuzz, process
import tldextract

import pprint
pp = pprint.PrettyPrinter(indent=4)

"""
name: return a dict with company name based on best match from list from get/name
"""

# from collections import namedtuple
from inspect import currentframe

# Supporting functions

loc = f"process/name"

def ln(): # print line numbers with f"{ln()}"
    cf = currentframe()
    return cf.f_back.f_lineno

# MAIN

if v:
    print(f"\n---\np{loc} #{ln()} STARTING process/name.py")

def main(names, domain, v=False, test=False):
    if v:
        print(f"\n{loc} #{ln()} processing {len(names)} names:")
        pp.pprint(names)

    if len(names) > 0:
        name = process.extractOne(domain, names)[0]
    else:
        name = ''

    if v:
        print(f"\n---\n{loc} #{ln()} returning name: {name}")

    return name
