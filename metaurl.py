####################
# metaURL: generate metadata from a URL
# public Github repo: https://github.com/ndeville/meta_url
# project notes: https://notes.nicolasdeville.com/projects/metaurl/
# Work In Progress

import os

import time
start_time = time.time()

from collections import namedtuple
from collections import OrderedDict

from urllib.parse import urlparse
import tldextract
import requests

# internal modules
from get.countries import main as get_countries
from get.emails import main as get_emails
from get.links import all as get_all_links
from get.links import internal as get_internal_links
from get.links import socials as get_social_links
from get.links import linkedins as get_linkedins
from get.links import twitters as get_twitters
from get.links import files as get_files_links
from get.metadata import main as get_metadata
from get.name import main as get_name
from get.soup import main as get_soup
from get.team import main as get_team
from process.emails import main as process_emails
from process.team import main as process_team
from process.name import main as process_name

### GLOBALS

list_url_crawled = []

### SUPPORTING FUNCTIONS

def sep(count=50, lines=3, symbol='='):
    separator = f"{symbol * count}" + '\n'
    separator = f"\n{separator * lines}"
    print(separator)

# script name
loc = f"metaurl"

# get line numbers
from inspect import currentframe
def ln():
    """
    print line numbers with f"{ln()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

def clean_url(long_url): # same as above, but different call name
    o = urlparse(long_url)
    cleaned = f"{o.scheme}://{o.netloc}"
    if cleaned.endswith('/'):
        cleaned = cleaned[:-1]
    return cleaned

def clean_long_url(long_url):
    o = urlparse(long_url)
    cleaned = f"{o.scheme}://{o.netloc}{o.path}"
    if cleaned.endswith('/'):
        cleaned = cleaned[:-1]
    return cleaned

def get_root_url(url):
    o = urlparse(url)
    root_website = f"{o.scheme}://{o.hostname}".lower()
    return root_website

def get_domain_from_url(url):
    o = tldextract.extract(url)
    domain = f"{o.domain}.{o.suffix}".lower()
    if 'www.' in domain:
        domain = domain.replace('www.','')
    return domain

def get_slug_from_url(url):
    o = tldextract.extract(url)
    domain_name = o.domain.lower()
    if 'www.' in domain_name:
        domain_name = domain_name.replace('www.','')
    return domain_name

# def clean_string(string):
#     TODO clean description / title strings

def check_url(url):
    response = requests.get(url)
    print(f"\nChecked {url}: {response.status_code=}")
    # Reference for requests status codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    if response.status_code == 200:
        print(f"{url} is LIVE")
        return True
    if response.status_code == 403:
        print(f"{url} is Protected / MANUAL CHECK required")
        return True
    if response.status_code == 406:
        print(f"{url} is Not Acceptable / MANUAL CHECK required")
        return True
    else:
        print(f"{url} is DEAD")
        return False

def find_new_url(url):

    if url.startswith("http"):
        extract = tldextract.extract(url)
        domain = f"{extract.domain}.{extract.suffix}"   
    else:
        domain = url

    v1 = f"https://{domain}"
    if check_url(v1):
        return v1
    else:
        v2 = f"https://www.{domain}"
        if check_url(v2):
            return v2
        else:
            v3 = f"http://{domain}"
            if check_url(v3):
                return v3
            else:
                v4 = f"http://www.{domain}"
                if check_url(v4):
                    return v4
                else:
                    return None



### MAIN

def meta(url,root=False,v=False,test=False,return_format=False): # v == verbose
    global list_url_crawled

    url = url.strip()

    # Validation of URL / TODO: add logic to handle domains, ie without http..
    if url.startswith('http'):
        # if long URL is passed (sub-page) and root == True passed as argument, start from homepage.
        if root == True:
            url = clean_url(url)
        domain = get_domain_from_url(url)
    else:
        domain = url
        url = find_new_url(domain)

    if v:
        print(f"\n{loc} #{ln()} ===\nProcessing {url} with domain {domain}\n===\n")

    meta_url_fields = [
        'clean_url',  # str / inline 
        'clean_root_url', # str / inline
        'career_pages', # list / from get.links import career
        'contact_pages', # list / from get.links import contact
        'countries', # list / get.countries
        'description', # str / get.metadata
        'domain', # str / inline
        'emails', # list / get.emails
        'email_patterns', # list / find_email_patterns (method tbc)
        'facebook', # str / from get.links import socials
        'files', # set / get.links.files
        'h1', # str / get.metadata
        'internal_links', # set / get.links.internal
        'keywords', # list / get.metadata
        'linkedin', # str / from get.links import socials
        'linkedins', # list / from get.links import linkedins
        'logo', # bin / get.logo
        'medium', # str / from get.links import socials
        'name', # str / get.name
        'phone', # string / get.phone
        'slug', # str / inline
        'tags', # list / get.tags (method tbc)
        'team', # list / get.team
        'tiktok', # str / from get.links import socials
        'title', # str / get.metadata
        'twitter', # list / from get.links import socials
        'whois', # str / get.whois
        'youtube', # str / from get.links import socials
    ]

    # TODO: get.countries
    # TODO: get.logo
    # TODO: get.phone
    # TODO: get.tags
    # TODO: get.whois

    ## HOMEPAGE

    homepage_soup_tuple = get_soup(url,v=v)
    list_url_crawled.append(url)

    output_internal_links = get_internal_links(homepage_soup_tuple,v=v) # sorted set
    internal_links = output_internal_links['internal_links']
    if v:
        print(f"\n{loc} #{ln()} {internal_links=}")
    emails = output_internal_links['emails']
    if v:
        print(f"\n{loc} #{ln()} {emails=}")

    socials = get_social_links(homepage_soup_tuple,v=v)

    metadata = get_metadata(homepage_soup_tuple,v=v)

    # SOUPS

    emails_page_keywords = [
        'about',
        'company',
        'crew',
        'data',
        'department',
        'impressum',
        'legal',
        'operations',
        'people',
        'privacy',
        'team',
        'terms',
        'who',
    ]

    name_page_keywords = [
        'about',
        'company',
        'data',
        'datenschutz',
        'impressum',
        'legal',
        'privacy',
        'terms',
        'who-we',
    ]

    team_page_keywords = [
        'about',
        'company',
        'contact',
        'crew',
        'department',
        'heroes',
        'operations',
        'people',
        'team',
        'who-we',
    ]

    list_keywords = sorted(set(emails_page_keywords + name_page_keywords + team_page_keywords))

    soup_links = [x for x in internal_links if domain in x and any(ele in x for ele in list_keywords)]

    if v:
        print(f"\n{loc} #{ln()} processing additional soup links: ")
        for sl in soup_links:
            print(f"    {sl}")
    print()

    dict_soup_tuples = {}
    for soup_link in soup_links:
        if soup_link not in list_url_crawled:
            # try statement because sometimes crawl fails only on specific pages, so we try to return the homepage at the very least
            try:
                soup_tuple = get_soup(soup_link,v=v)
                list_url_crawled.append(soup_link)
                dict_soup_tuples[soup_link] = soup_tuple
            except:
                print(f"\n{loc} #{ln()} failed to load: {soup_link} ")
                continue
    # add homepage soup to dict
    dict_soup_tuples[url] = homepage_soup_tuple

    if v:
        print(f"\n{loc} #{ln()} len(dict_soup_tuples): {len(dict_soup_tuples)}\n")

    # NAMEDTUPLE TO BE RETURNED
    meta_url = namedtuple('metaURL', meta_url_fields)

    ## NAMEDTUPLE FIELDS

    ### clean_url,  # str / inline 
    clean_url = clean_long_url(url)

    ### clean_root_url, # str / inline
    clean_root_url = get_root_url(url)

    ### career_pages, # list / from get.links import career
    career_pages_keywords = [
        'career',
        'job',
        'hire',
        'hiring',
        'join',
    ]
    career_pages = []
    for link in internal_links:
        if any(ele in link for ele in career_pages_keywords) and domain in link:
            career_pages.append(link)
            if v:
                print(f"{loc} #{ln()}: career page: {link}")
        else:
            if v:
                print(f"{loc} #{ln()}: NOT a career page: {link}")

    career_pages = sorted(set(career_pages))

    ### contact_pages, # list / from get.links import contact
    contact_pages_keywords = [
        'contact',
        'cv',
        'kontakt',
        'submit',
    ]
    contact_pages = []
    for link in internal_links:
        if any(ele in link for ele in contact_pages_keywords) and domain in link:
            contact_pages.append(link)
            if v:
                print(f"{loc} #{ln()}: CONTACT page: {link}")
        else:
            if v:
                print(f"{loc} #{ln()}: NOT a CONTACT page: {link}")

    contact_pages = sorted(set(contact_pages))

    ### countries, # list / get.countries
    countries = []

    ### description, # returns str from get/metadata
    description = metadata.description

    ### emails, # returns dict from get/emails
    
    # emails_links_to_crawl = [x for x in internal_links if domain in x and any(ele in x for ele in emails_page_keywords)]
    list_emails_soups = [x for x in internal_links if domain in x and any(ele in x for ele in emails_page_keywords)]
    list_emails_soups.append(url) # to add the homepage soup to the list
    # if v:
    #     print(f"\n\n===\n{loc} #{ln()}: crawling {len(emails_links_to_crawl)} internal links for emails:")
    #     for link_emails_to_crawl in emails_links_to_crawl:
    #         print(link_emails_to_crawl)
    #     print()
    for link in list_emails_soups:
        if v:
            print(f"\n{loc} #{ln()}: crawling {link} for emails")
        try:
            soup_emails = dict_soup_tuples[link]
            emails_on_page = get_emails(soup_emails,v=v)
            if v:
                print(f"\n{loc} #{ln()} returned emails_on_page: {emails_on_page}")
            if len(emails_on_page) > 0:
                for email in emails_on_page:
                    if email not in emails:
                        emails[email] = link
        except:
            print(f"{loc} #{ln()} ERROR with getting {link} soup for emails.")
            continue

    # sort
    # emails = {key: val for key, val in sorted(emails.items(), key = lambda ele: ele[0])}
    emails = OrderedDict(sorted(emails.items()))
    if v:
        print(f"{loc} #{ln()}: emails: {emails}")

    ### email_patterns, # list / find_email_patterns (method tbc)
    email_patterns = [] # appended during processing below

    ### facebook, # str / from get.links import socials
    facebook = socials.facebook
    if facebook not in [None, '']:
        facebook = clean_long_url(facebook)

    ### files, # set / get.links.files
    files = set()

    ### h1, # str / get.metadata
    h1 = metadata.h1

    ### keywords, # list / get.metadata
    keywords = metadata.keywords

    ### linkedin, # str / from get.links import socials
    linkedin = socials.linkedin
    if linkedin not in [None, '']:
        linkedin = clean_long_url(linkedin)

    ### logo, # str(link) / get.logo
    logo = ''

    ### medium, # str / from get.links import socials
    medium = socials.medium
    if medium not in [None, '']:
        medium = clean_long_url(medium)

    ### name, # str / get.name
    names = [] # return list of all potential names matches found. Process later with process/name
    # crawl homepage first
    if v:
        print(f"\n{loc} #{ln()} crawling homepage {url} for name")
    names = get_name(homepage_soup_tuple,v=v)
    list_url_crawled.append(url)
    if v:
        print(f"\n{loc} #{ln()}: {names=}")
    
    # name_links_to_crawl = [x for x in internal_links if domain in x and any(ele in x for ele in name_page_keywords)]
    list_name_soups = [x for x in internal_links if domain in x and any(ele in x for ele in name_page_keywords)]
    list_name_soups.append(url) # to add the homepage soup to the list
    # if v:
    #     print(f"\n\n===\n{loc} #{ln()}: crawling {len(name_links_to_crawl)} internal links for name:")
    for link in list_name_soups:
        if v:
            print(f"\n{loc} #{ln()}: crawling {link} for name")
        try:
            soup_name = dict_soup_tuples[link]
            name_on_page = get_name(soup_name,v=v)
            if v:
                print(f"\n{loc} #{ln()} {name_on_page=}")
            if len(name_on_page) > 0:
                for name in name_on_page:
                    names.append(name)
        except:
            print(f"{loc} #{ln()} ERROR with getting {link} soup for company name.")
            continue

    # sort
    # name = {key: val for key, val in sorted(name.items(), key = lambda ele: ele[0])}
    # names = OrderedDict(sorted(names.items()))
    names = sorted(set(names))
    if v:
        print(f"{loc} #{ln()}: {names=}")

    ### phone, # string / get.phone
    phone = ''

    ### slug, # str / inline
    slug = get_slug_from_url(url)

    ### tags, # list / get.tags (method tbc)
    tags = []

    ### team, # list / get.team
    
    # team_page_link = '' # so homepage doesn't get crawled
    team = {} # to capture the output
    linkedins = {} # to capture the output
    twitters = {} # to capture the output
    # set_team_links_to_crawl = sorted(set(internal_links))
    list_team_soups = [x for x in internal_links if domain in x and any(ele in x for ele in team_page_keywords)]
    # list_team_soups.append(url) # to add the homepage soup to the list
    for link in list_team_soups:
        # if any(ele in link for ele in team_page_keywords)
        # team_page_link = link # so homepage doesn't get crawled
        if v:
            print(f"\n+++\n{loc} #{ln()}: Processing TEAM page link: {link}")
        
        try:
            team_page_soup = dict_soup_tuples[link]

            page_team = get_team(team_page_soup,v=v)
            page_linkedins = get_linkedins(team_page_soup,v=v)
            page_twitters = get_twitters(team_page_soup,v=v)
            
            if v:
                print(f"{loc} #{ln()}: {len(page_team)} people found on TEAM page: {link}:")
                print(page_team)
                print(f"{loc} #{ln()}: {len(page_linkedins)} Linkedins found on TEAM page: {link}")
                print(page_linkedins)
            # catering for multiple team pages
            if len(page_team) > 0:
                for k,v in page_team.items():
                    team[k] = v    
            if len(page_linkedins) > 0:
                for linkedin_url,linkedin_src in page_linkedins.items():
                    if linkedin_url not in linkedins:
                        linkedins[linkedin_url] = linkedin_src
            if len(page_twitters) > 0:
                for twitter_url,twitter_src in page_twitters.items():
                    if twitter_url not in twitters:
                        twitters[twitter_url] = twitter_src
            else:
                if v:
                    print(f"{loc} #{ln()}: NOT a Team page: {link}")

        except:
            print(f"{loc} #{ln()} ERROR with getting {link} soup for team members.")
            continue

    if v:
        print(f"\n{loc} #{ln()}: {len(team)} members found:")
        print(f"{team=}")

    # clean team
    team = OrderedDict(sorted(team.items()))
    # clean linkedins
    # remove company linkedin if in / done in get/links.linkedins
    # if linkedin in linkedins:
    #     linkedins = linkedins.pop(linkedin)    
    # remove duplicates    
    clean_linkedins = {}
    for k,v in linkedins.items():
        if k not in clean_linkedins:
            clean_linkedins[k] = v
    linkedins = clean_linkedins

    ### tiktok, # str / from get.links import socials
    tiktok = socials.tiktok

    ### title, # str / get.metadata
    title = metadata.title

    ### twitter, # list / from get.links import socials
    twitter = socials.twitter
    if twitter not in [None, '']:
        twitter = clean_long_url(twitter)

    ### whois, # str / get.whois
    whois = ''
    

    ### youtube, # str / from get.links import socials
    youtube = socials.youtube
    if youtube not in [None, '']:
        youtube = clean_long_url(youtube)

    # PROCESS

    # process emails

    if v:
        print(f"\n\n{sep()}{loc} #{ln()}: PROCESSING EMAILS")

    output_processed_emails = process_emails(emails, team, domain, v=v)
    emails = output_processed_emails['emails']
    if v:
        print(f"\n{loc} #{ln()} {emails=}")
    email_patterns = output_processed_emails['email_patterns']
    if v:
        print(f"\n{loc} #{ln()} {email_patterns=}")
    team = output_processed_emails['team']
    if v:
        print(f"{loc} #{ln()}: team: {team}")

    # process team

    if v:
        print(f"\n\n{sep()}{loc} #{ln()}: PROCESSING team with:")
        print(f"{loc} #{ln()} emails: {emails}")
        print(f"{loc} #{ln()}: team: {team}")
        print(f"{loc} #{ln()}: email_patterns {email_patterns}\n\n")
    team = process_team(emails, team, email_patterns, v=v)

    # process name

    if v:
        print(f"\n\n{sep()}{loc} #{ln()}: PROCESSING names with:")

    name = process_name(names, domain, v=v)

    # CREATE namedtuple

    meta_url.clean_url = clean_url
    meta_url.clean_root_url = clean_root_url
    meta_url.career_pages = career_pages
    meta_url.contact_pages = contact_pages
    meta_url.countries = countries
    meta_url.description = description
    meta_url.domain = domain
    meta_url.emails = emails
    meta_url.email_patterns = email_patterns
    meta_url.facebook = facebook
    meta_url.files = files
    meta_url.h1 = h1
    meta_url.internal_links = internal_links
    meta_url.keywords = keywords
    meta_url.linkedin = linkedin
    meta_url.linkedins = linkedins
    meta_url.logo = logo
    meta_url.medium = medium
    meta_url.name = name
    meta_url.phone = phone
    meta_url.slug = slug
    meta_url.tags = tags
    meta_url.team = team
    meta_url.tiktok = tiktok
    meta_url.title = title
    meta_url.twitter = twitter
    meta_url.twitters = twitters
    meta_url.whois = whois
    meta_url.youtube = youtube


    # # Cleanup: None where no value

    # if not isinstance(socials.twitter, str):
    #     socials.twitter = None
    # if not isinstance(socials.linkedin, str):
    #     socials.linkedin = None
    # if not isinstance(socials.facebook, str):
    #     socials.facebook = None
    # if not isinstance(socials.instagram, str):
    #     socials.instagram = None
    # if not isinstance(socials.youtube, str):
    #     socials.youtube = None
    # if not isinstance(socials.medium, str):
    #     socials.medium = None
    # if not isinstance(socials.github, str):
    #     socials.github = None
    # if not isinstance(socials.tiktok, str):
    #     socials.tiktok = None

    if return_format:
        print(f"\n\n=====\n{loc} #{ln()}: NOTE: metaURL returns namedtuple with following attributes: {','.join(meta_url_fields)}\n")
        print(f"\nCopy/paste the below to print full output:\n---\n")

        print(f"print(f\"\\n\=====================\nOUTPUT:\\n\")")
        for field in meta_url_fields:
            print("print(f\"", f'{field}: ', "{", f'x.{field}', "}", "\\n\")")
        
    if v:
        print(f"\n---\n")
        print(f"\n\n{loc} #{ln()} {len(list_url_crawled)} URLs CRAWLED:\n")
        list_url_crawled = sorted(set(list_url_crawled))
        for url_crawled in list_url_crawled:
            print(f"{url_crawled}")
        print("with duplicates:")
        duplicates = [b for b in list_url_crawled if list_url_crawled.count(b) > 1]
        for d in duplicates:
            print(d)

    # else:
    #     print(f"{loc} #{ln()}: ERROR: {url} is not a valid URL")

    return meta_url



def metadata(url,v=False,test=False,return_format=False):

    url = url.strip()
    domain = get_domain_from_url(url)

    if url.startswith('http'):

        if v:
            print(f"\n===\nProcessing {url} with domain {domain}\n===\n")

        meta_url_fields = [
            'clean_url',  # str / inline 
            'clean_root_url', # str / inline
            'description', # str / get.metadata
            'domain', # str / inline
            'h1', # str / get.metadata
            'name', # str / get.name
            'slug', # str / inline
            'title', # str / get.metadata
        ]

        ## HOMEPAGE ONLY
        homepage_soup_tuple = get_soup(url,v=v)

        ## Metadata
        metadata = get_metadata(homepage_soup_tuple,v=v)

        # # NAMEDTUPLE TO BE RETURNED
        meta_url = namedtuple('metaURL', meta_url_fields)

        # ## NAMEDTUPLE FIELDS

        # ### clean_url,  # str / inline 
        clean_url = clean_long_url(url)

        # ### clean_root_url, # str / inline
        clean_root_url = get_root_url(url)

        ### description, # returns str from get/metadata
        description = metadata.description

        ### h1, # str / get.metadata
        h1 = metadata.h1

        ### keywords, # list / get.metadata
        keywords = metadata.keywords

        ### name, # str / get.name
        names = get_name(homepage_soup_tuple,v=v)
        if v:
            print(f"\n{loc} #{ln()} returned names_on_page: {names}")
        if v:
            print(f"\n\n{sep()}{loc} #{ln()}: PROCESSING names with:")
        name = process_name(names, domain, v=v)

        # ### slug, # str / inline
        slug = get_slug_from_url(url)
    
        ### title, # str / get.metadata
        title = metadata.title

        # CREATE namedtuple

        meta_url.clean_url = clean_url
        meta_url.clean_root_url = clean_root_url
        meta_url.description = description
        meta_url.domain = domain
        meta_url.h1 = h1
        meta_url.keywords = keywords
        meta_url.name = name
        meta_url.slug = slug
        meta_url.title = title


        if return_format:
            print(f"\n\n=====\n{loc} #{ln()}: NOTE: metaURL returns namedtuple with following attributes: {','.join(meta_url_fields)}\n")
            print(f"\nCopy/paste the below to print full output:\n---\n")

            print(f"print(f\"\\n\=====================\nOUTPUT:\\n\")")
            for field in meta_url_fields:
                print("print(f\"", f'{field}: ', "{", f'x.{field}', "}", "\\n\")")
        

        return meta_url

    else:
        print(f"{loc} #{ln()}: ERROR: {url} is not a valid URL")

### Socials only

def socials(url,root=True,v=False,test=False,return_format=False):

    url = url.strip()
    domain = get_domain_from_url(url)

    # if long URL is passed (sub-page) and root == True passed as argument, start from homepage.
    if root == True:
        url = clean_url(url)

    if url.startswith('http'):

        if v:
            print(f"\n===\nProcessing Socials for  {url} with domain {domain}\n===\n")

        url_socials_fields = [
            'facebook', # str / from get.links import socials
            'instagram', # str / from get.links import socials
            'linkedin', # str / from get.links import socials
            'medium', # str / from get.links import socials
            'tiktok', # str / from get.links import socials
            'twitter', # list / from get.links import socials
            'youtube', # str / from get.links import socials
        ]

        # # NAMEDTUPLE TO BE RETURNED
        url_socials = namedtuple('metaURL', url_socials_fields)

        ## HOMEPAGE ONLY
        homepage_soup_tuple = get_soup(url,v=v)

        ## Socials
        socials = get_social_links(homepage_soup_tuple,v=v)

        # CREATE namedtuple

        url_socials.facebook = socials.facebook
        url_socials.instagram = socials.instagram
        url_socials.linkedin = socials.linkedin
        url_socials.medium = socials.medium
        url_socials.tiktok = socials.tiktok
        url_socials.twitter = socials.twitter
        url_socials.youtube = socials.youtube

        if return_format:
            print(f"\n\n=====\n{loc} #{ln()}: NOTE: metaURL returns namedtuple with following attributes: {','.join(url_socials_fields)}\n")
            print(f"\nCopy/paste the below to print full output:\n---\n")

            print(f"print(f\"\\n\=====================\nOUTPUT:\\n\")")
            for field in url_socials_fields:
                print("print(f\"", f'{field}: ', "{", f'x.{field}', "}", "\\n\")")
        

        return url_socials

    else:
        print(f"{loc} #{ln()}: ERROR: {url} is not a valid URL")