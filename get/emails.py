# get.emails

import re

### Supporting Functions

import pprint
pp = pprint.PrettyPrinter(indent=4)

# script name
loc = "get/emails"

# get line numbers
from inspect import currentframe
def ln():
    """
    print line numbers with f"{ln()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

### MAIN

### NOTE
### use mailto: tag + regex to get emails

add_keywords_to_remove = [
    'dataprotection',
]

def main(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\n---\n{loc} #{ln()}: parsing {url}")

    set_emails = set() # start with set to avoid duplicates

    # with regex

    text = soup.get_text()

    email_regex= "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

    matches = re.findall(email_regex, text)
    if v:
        print(f"\n{loc} #{ln()} matches: {matches}")

    if len(matches) > 0:
        for match in matches:
            if not any(ele in match for ele in add_keywords_to_remove):
                set_emails.add(match.strip().lower())

    # with mailto: tag / NECESSARY?

    # links = soup.find_all('a')

    # if v:
    #     print(f"\nget.links.internal #{ln()}: {len(links)} links found:")
    # for l in links:
    #     if v:
    #         print(f"\nget.links.internal #{ln()}: {l}")
            
    #     try:
    #         href = l['href']

    # mailtos = re.findall('<a href="mailto:(.*?)">', html)


    # prepare to return

    # move to dict to append email.src
    dict_emails_to_return = {}
    for e in set_emails:
        dict_emails_to_return[e] = url

    # sorted_list_people_found = sorted(set_emails)

    if v:
        print(f"\n{loc} #{ln()} dict_emails_to_return: {dict_emails_to_return}")
        pp.pprint(dict_emails_to_return)

    # list_emails = list(set_emails).sort()
    # dict_emails_to_return = sorted(dict_emails_to_return)

    if v and len(dict_emails_to_return) > 0:
        print(f"\n---\n{loc} #{ln()}: \nRETURNED dict of all EMAILS from {url} ({len(dict_emails_to_return)}):\n{dict_emails_to_return}.\n---\n")

    return dict_emails_to_return