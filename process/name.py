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

def clean_name(name, v=False):
    if v:
        print(f"\n---\np{loc} #{ln()} cleaning name: {name}")

    name = name.strip()

    keywords_to_remove = [
        'AG',
        'LLC',
        'Ltd',
    ]

    for k in keywords_to_remove:
        if k in name:
            name = name.replace(k, "")

    if v:
        print(f"\n---\np{loc} #{ln()} returning name: {name}")

    name = name.strip()

    return name

# MAIN

keywords_to_remove = [
    "We're",
]

def main(names, domain, v=False, test=False):
    if v:
        print(f"\n---\np{loc} #{ln()} processing {len(names)} names:")
        pp.pprint(names)

    root_domain = tldextract.extract(domain).domain.lower()

    if len(names) > 0:
        # create dict of concatenated names and names, to compare with domain
        dict_names = {}
        for name in names:
            # clean names first
            for k in keywords_to_remove:
                if k in name:
                    name = name.replace(k, "")
            # create compare names for each
            compare_name = name.replace(' ','')
            compare_name = compare_name.lower().strip()
            # add to dict
            dict_names[compare_name] = name

        # get list of compare names
        list_compare_names = [x for x in dict_names.keys()]
        if v:
            print(f"\n{loc} #{ln()} list_compare_names:")
            pp.pprint(list_compare_names)
    
        # use thefuzzy to extract key of best match between list_compare_names and root_domain
        compare_name_found = process.extractOne(root_domain, list_compare_names)
        if v:
            print(f"\n{loc} #{ln()} compare_name_found: {compare_name_found}")

        # thefuzzy returns list, so name is first item
        name = clean_name(dict_names[compare_name_found[0]])
    else:
        name = ''

    if v:
        print(f"\n---\np{loc} #{ln()} returning name: {name}")

    return name
