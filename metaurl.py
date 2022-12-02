####################
# metaURL: generate metadata from a URL
# public Github repo: https://github.com/ndeville/meta_url
# project notes: https://notes.nicolasdeville.com/projects/metaurl/
# Work In Progress

import os

import time
start_time = time.time()

from collections import namedtuple

from urllib.parse import urlparse
import tldextract

# internal modules
from get.countries import main as get_countries
from get.emails import main as get_emails
from get.links import all as get_all_links
from get.links import internal as get_internal_links
from get.links import socials as get_social_links
from get.links import files as get_files_links
from get.metadata import main as get_metadata
from get.name import main as get_name
from get.soup import main as get_soup
from get.team import main as get_team
from process.emails import main as process_emails
from process.team import main as process_team


### SUPPORTING FUNCTIONS

# get line numbers
from inspect import currentframe
def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

def get_clean_url(url: str) -> str:
    purl = urlparse(url)
    scheme = purl.scheme + '://' if purl.scheme else ''
    concatenation = f'{scheme}{purl.netloc}{purl.path}'
    if concatenation.endswith('/'): # remove trailing slash
        final_url = concatenation[:-1]
    else:
        final_url = concatenation
    return final_url

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

### MAIN

def meta(url,verbose=False,test=False):

    url = url.strip()
    domain = get_domain_from_url(url)

    # Validation of URL / TODO: add logic to handle domains, ie without http..
    if url.startswith('http'):

        if verbose:
            print(f"\n===\nProcessing {url} with domain {domain}\n===\n")

        meta_url_fields = [
            'clean_url',  # str / inline 
            'clean_root_url', # str / inline
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
        # TODO: get.emails
        # TODO: get.logo
        # TODO: get.phone
        # TODO: get.tags
        # TODO: get.whois

        # SOUP

        ## HOMEPAGE

        homepage_soup_tuple = get_soup(url,v=verbose)

        internal_links = get_internal_links(homepage_soup_tuple,v=verbose) # sorted set

        socials = get_social_links(homepage_soup_tuple,v=verbose)

        metadata = get_metadata(homepage_soup_tuple,v=verbose)

        # NAMEDTUPLE TO BE RETURNED
        meta_url = namedtuple('metaURL', meta_url_fields)

        ## NAMEDTUPLE FIELDS

        ### clean_url,  # str / inline 
        clean_url = get_clean_url(url)

        ### clean_root_url, # str / inline
        clean_root_url = get_root_url(url)

        ### contact_pages, # list / from get.links import contact
        contact_pages_keywords = [
            'contact',
            'kontakt',
            'cv',
            'submit',
        ]
        contact_pages = []
        for link in internal_links:
            if any(ele in link for ele in contact_pages_keywords) and domain in link:
                contact_pages.append(link)
                if verbose:
                    print(f"metaurl #{get_linenumber()}: CONTACT page: {link}")
            else:
                if verbose:
                    print(f"metaurl #{get_linenumber()}: NOT a CONTACT page: {link}")

        contact_pages = sorted(set(contact_pages))

        ### countries, # list / get.countries
        countries = []

        ### description, # str / get.metadata
        description = metadata.description

        ### emails, # list / get.emails
        emails_page_keywords = [
            'about',
            'crew',
            'department',
            'operations',
            'people',
            'team',
            'who-we',
            'privacy',
            'terms',
            'legal',
            'data',
        ]
        emails = {}
        emails_links_to_crawl = [x for x in internal_links if domain in x and any(ele in x for ele in emails_page_keywords)]
        print(f"\n\n===\nmetaurl #{get_linenumber()}: crawling {len(emails_links_to_crawl)} internal links for emails.")
        for link in emails_links_to_crawl:
            emails_on_page = get_emails(get_soup(link),v=verbose)
            if len(emails_on_page) > 0:
                for email in emails_on_page:
                    if email not in emails:
                        emails[email] = link
                # emails = emails + emails_on_page
        if verbose:
            print(f"metaurl #{get_linenumber()}: emails: {emails}")

        # sort
        # emails = emails.sort()
        # emails = sorted(emails)
        emails = {key: val for key, val in sorted(emails.items(), key = lambda ele: ele[0])}


        ### email_patterns, # list / find_email_patterns (method tbc)
        email_patterns = [] # appended during processing below

        ### facebook, # str / from get.links import socials
        facebook = socials.facebook

        ### files, # set / get.links.files
        files = set()

        ### h1, # str / get.metadata
        h1 = metadata.h1

        ### keywords, # list / get.metadata
        keywords = metadata.keywords

        ### linkedin, # str / from get.links import socials
        linkedin = socials.linkedin

        ### logo, # str(link) / get.logo
        logo = ''

        ### medium, # str / from get.links import socials
        medium = socials.medium

        ### name, # str / get.name
        name = ''

        ### phone, # string / get.phone
        phone = ''

        ### slug, # str / inline
        slug = get_slug_from_url(url)
        

        ### tags, # list / get.tags (method tbc)
        tags = []

        ### team, # list / get.team
        team_page_keywords = [
            'about',
            'crew',
            'department',
            'operations',
            'people',
            'team',
            'contact',
            'who-we',
        ]
        team_page_link = '' # so homepage doesn't get crawled
        team = set() # to capture the output
        set_team_links_to_crawl = sorted(set(internal_links))
        for link in set_team_links_to_crawl:
            if any(ele in link for ele in team_page_keywords):
                team_page_link = link # so homepage doesn't get crawled
                if verbose:
                    print(f"\n+++\nmetaurl #{get_linenumber()}: Processing TEAM page link: {team_page_link}")
                page_team = get_team(get_soup(team_page_link),v=verbose)
                if verbose:
                    print(f"metaurl #{get_linenumber()}: {len(page_team)} people found on TEAM page: {team_page_link}\n+++\n")
                # catering for multiple team pages
                if len(page_team) > 0:
                    for t in page_team:
                        team.add(t)                    
            else:
                if verbose:
                    print(f"metaurl #{get_linenumber()}: NOT a Team page: {link}")
        if team_page_link == '': # so homepage gets crawled if no team page found
            team_page_link = url
            print(f"\nmetaurl #{get_linenumber()}: Processing Team page link: {team_page_link}\n")
            team = get_team(get_soup(team_page_link),v=verbose)
        if verbose:
            print(f"\nmetaurl #{get_linenumber()}: {len(team)} members found.\n\n")
        
        team = sorted(team)

        ### tiktok, # str / from get.links import socials
        tiktok = socials.tiktok

        ### title, # str / get.metadata
        title = metadata.title

        ### twitter, # list / from get.links import socials
        twitter = socials.twitter
        

        ### whois, # str / get.whois
        whois = ''
        

        ### youtube, # str / from get.links import socials
        youtube = socials.youtube
        

        # PROCESS

        # process emails

        output_processed_emails = process_emails(emails, team, v=verbose)
        emails = output_processed_emails['emails']
        email_patterns = output_processed_emails['email_patterns']

        # process team

        # team = process_team(emails, team, v=verbose)

        # CREATE namedtuple

        meta_url.clean_url = clean_url
        meta_url.clean_root_url = clean_root_url
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

        if verbose:
            print(f"\n---\nmetaurl #{get_linenumber()}: NOTE: metaURL returns namedtuple with following attributes: {','.join(meta_url_fields)}\n")
            print(f"\nCopy/paste the below to print full output:\n---\n")

            print(f"print(f\"\\n\=====================\nOUTPUT:\\n\")")
            for field in meta_url_fields:
                print("print(f\"", f'{field}: ', "{", f'x.{field}', "}", "\\n\")")
            
        return meta_url

    else:
        print(f"metaurl #{get_linenumber()}: ERROR: {url} is not a valid URL")