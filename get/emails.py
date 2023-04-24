# get.emails

import re
import tldextract
from bs4 import BeautifulSoup
import os

from dotenv import load_dotenv
load_dotenv()
PROJECTS_FOLDER = os.getenv("PROJECTS_FOLDER")

import sys
sys.path.append(f"{PROJECTS_FOLDER}/indeXee")
import my_utils

import pprint
pp = pprint.PrettyPrinter(indent=4)

### Supporting Functions

# script name
loc = ">get/emails"

# get line numbers
from inspect import currentframe
def ln():
    """
    print line numbers with f"{ln()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

def get_domain_from_url(url):
    o = tldextract.extract(url)
    domain = f"{o.domain}.{o.suffix}".lower()
    if 'www.' in domain:
        domain = domain.replace('www.','')
    return domain

### MAIN

### NOTE
### use mailto: tag + regex to get emails

add_keywords_to_remove = [
    'career', 
    'compliance', 
    'dataprotection', 
    'datenschutz', 
    'dpo', 
    'gdpr', 
    'invest', 
    'legal', 
    'media', 
    'press', 
    'privacy',
    'security',
    'unsubscribe',
    'noreply',
    'no-reply',
    'no_reply',
    'ne-pas-',
    'spam',
    'react',
    ]

false_extensions = (
    'pdf',
    'doc',
    'docx',
    'png',
    'jpg',
    'jpeg',
)

# def find_emails_in_html(soup):
#     # Function to validate email addresses
#     def is_valid_email(email):
#         return bool(re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))

#     # soup = BeautifulSoup(html_text, 'html.parser')
#     email_list = []

#     # Find emails in mailto: links
#     mailto_links = soup.find_all(href=re.compile(r"^mailto:"))
#     for link in mailto_links:
#         email = link['href'].replace("mailto:", "")
#         if is_valid_email(email) and email not in email_list:
#             email_list.append(email)

#     # Find standalone emails in the text
#     standalone_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup)
#     for email in standalone_emails:
#         if is_valid_email(email) and email not in email_list:
#             email_list.append(email)

#     return email_list





def main(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],from_domain=True,v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]
    domain = get_domain_from_url(url)

    if v:
        print(f"\n---\n{loc} #{ln()}: parsing {url} with domain {domain}\n")

    set_emails = set() # start with set to avoid duplicates

    # With regex

    text = soup.prettify()

    # email_regex = r"(?:href=\"mailto:)?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)" ## WORKING
    email_regex = r"(?:href=\"mailto:)?([a-zA-Z0-9_.+-]+(?:@|\(at\))[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

    matches = re.findall(email_regex, text)

    if v:
        print(f"\n{loc} #{ln()} matches: {matches}")

    if len(matches) > 0:
        for match in matches:
            if '(at)' in match:
                match = match.replace('(at)','@')
            if v:
                print(type(match), match)
            email = match.strip().lower()
            parts = email.split('@')
            email_prefix = parts[0]
            email_domain = parts[1]
            if not any(ele in email_prefix for ele in keywords_to_remove) and not email.endswith(false_extensions):
                if from_domain: # get only emails from the same domain
                    if domain in email_domain:

                        # VALIDATE EMAIL FORMAT using my_utils
                        valid_email = my_utils.validate_email_format(email)

                        # Validate function returns cleaned up email if typo, else False if non-valid format
                        if valid_email not in [False, 'False']:
                            set_emails.add(valid_email)
                            if v:
                                print(f"ℹ️  ADDED {email} to set_emails on {url}")
                    else:
                        if v:
                            print(f"ℹ️  SKIPPED {email} with domain {email_domain}")
                else:
                    set_emails.add(email)
                    if v:
                        print(f"ℹ️  ADDED {email} to set_emails on {url}")

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

    # if v:
    #     print(f"\n{loc} #{ln()} dict_emails_to_return: {dict_emails_to_return}")
    #     pp.pprint(dict_emails_to_return)

    # list_emails = list(set_emails).sort()
    # dict_emails_to_return = sorted(dict_emails_to_return)

    if v and len(dict_emails_to_return) > 0:
        print(f"\n---\n{loc} #{ln()}: \nRETURNED dict of all EMAILS from {url} ({len(dict_emails_to_return)}):")
        pp.pprint(dict_emails_to_return)
        print("---\n")

    return dict_emails_to_return