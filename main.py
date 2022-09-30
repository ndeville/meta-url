####################
# metaURL: generate metadata from a URL
# project notes: https://notes.nicolasdeville.com/projects/metaurl/
# Work In Progress

import os

import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
USER = os.getenv("USER") # probably no need here
driverpath = os.getenv("CHROMEDRIVER") # in .env file CHROMEDRIVER=/Users/user/path/to/my/chromedriver

from urllib import request
from urllib.parse import urlparse
import tldextract
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import scrapee
from collections import namedtuple
import pymsgbox
import pickle

### while building / debugging:
from test_urls import test_list
list_to_test = test_list()
### while building / debugging:
from inspect import currentframe
def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno
### while building / debugging:
def separator(count=50, lines=3, symbol='='):
    line = f"{symbol * count}" + '\n'
    separator = f"\n{line * lines}"
    print(separator)
### while building / debugging:
import pprint
pp = pprint.PrettyPrinter(indent=4)
### while building / debugging:
count = 0
count_row = 0
# for pickling soup for tests:
import sys
sys.setrecursionlimit(10000)

############

### namedtuple to be returned
meta_url = namedtuple('metaURL', 
            [
            'clean_url',  # str
            'root_website_url', # str
            'domain', # str
            'slug', # str
            'header', # str
            'title', # str
            'name', # str
            'description', # str
            'tags', # list
            'emails', # list
            'twitter',
            'facebook',
            'youtube',
            # 'linkedin',
            'tiktok',
            'countries', # list
            'logo', # tbc
            ]
            )

# separators between name and description in headers and titles
name_summary_split = [
    '|',
    ':',
    '-',
    '·',
    ]

### WORKING
def clean_url(url: str) -> str:
    from urllib.parse import urlparse
    purl = urlparse(url)
    scheme = purl.scheme + '://' if purl.scheme else ''
    concatenation = f'{scheme}{purl.netloc}{purl.path}'
    if concatenation.endswith('/'): # remove trailing slash
        final_url = concatenation[:-1]
    else:
        final_url = concatenation
    return final_url

### WORKING
def root_url(url):
    o = urlparse(url)
    root_website = f"{o.scheme}//{o.hostname}".lower()
    return root_website

### WORKING
def domain_from_url(url):
    o = tldextract.extract(url)
    domain = f"{o.domain}.{o.suffix}".lower()
    if 'www.' in domain:
        domain = domain.replace('www.','')
    return domain

### WORKING
def slug_from_url(url):
    o = tldextract.extract(url)
    domain_name = o.domain.lower()
    if 'www.' in domain_name:
        domain_name = domain_name.replace('www.','')
    return domain_name

### TODO need to rework this. Use at all, or only with Selenium?
def metadata_from_url_request(url, v=False):
    try:
        html = request.urlopen(url).read().decode('utf8')
        if test:
            print(f"\n{separator()}\n{html=}")

        try:
            soup = BeautifulSoup(html, "html.parser")
            if test:
                print(f"\n{separator()}\n{soup=}")

            try:
                title = soup.title.text
                if '\n' in title:
                    title = title.replace('\n', ' ').strip()
                if v:
                    print(f"\n{separator()}\n{get_linenumber()} {title=}")

                try:
                    header = soup.find('h1').text
                    if '\n' in header:
                        header = header.replace('\n', ' ').strip()
                    if v:
                        print(f"{separator()}\n{get_linenumber()} {header=}")

                except Exception as e:
                    print(f"\n{get_linenumber()} h1 ERROR: {e}")
                    name = title
            
            except Exception as e:
                print(f"\n{get_linenumber()} title ERROR: {e}")

        except Exception as e:
            print(f"\n{get_linenumber()} soup ERROR: {e}")

    except Exception as e:
        print(f"\n{get_linenumber()} html ERROR: {e}")

def name_from_metadata(metadata):

    

    ### TODO need to rework this
    for split_char in name_summary_split:
        if split_char in name:
            parts = name.split(split_char)
            name = parts[0].strip()
            title = parts[1].strip()
    print(f"Not done yet")

def metadata_from_url_selenium(url, v=False, test=False):

    if v:
        print(f"\n#{get_linenumber()} starting metadata_from_url_selenium with {url}")

    def process_soup(soup):

        # empty placeholders / to ensure return if fail
        # emails = ''
        # twitter = ''
        # facebook = ''
        # youtube = ''
        # linkedin = ''
        # tiktok = ''
        # countries = ''
        title = ''
        name = ''
        description = ''

        metas = [x for x in soup.find_all('meta') if x.get('property')]
        if v:
            print(f"\n#{get_linenumber()} metas:\n")
            pp.pprint(metas)
        
        result = [{x.get('property'): x.get('content')} for x in metas] # list of dicts
        if v:
            print(f"\n#{get_linenumber()} result:")
            pp.pprint(result)
            print()

        for og in result:
            if 'og:title' in og:
                title = og['og:title']
            if 'og:description' in og:
                description = og['og:description']
            if 'og:site_name' in og:
                name = og['og:site_name']

        dict_metadata_from_selenium = {
            # 'emails': emails,
            # 'twitter': twitter,
            # 'facebook': facebook,
            # 'youtube': youtube,
            # 'linkedin': linkedin,
            # 'tiktok': tiktok,
            # 'countries': countries,
            'title': title,
            'description': description,
            'name': name,
        }

        return dict_metadata_from_selenium

    if test:
        pickle_dump = f"test/soup-{slug_from_url(url)}.pkl"
        with open(pickle_dump, "rb") as tp:
            print(f"\n{get_linenumber()} TEST: LOADING FROM PICKLE FILE: {pickle_dump}\n")
            soup = pickle.load(tp)
            output = process_soup(soup)
    else:
        print(f"\n{get_linenumber()} RUNNING LIVE SCRAPING OF {url}\n")
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')

        s = Service(driverpath)
        web = Chrome(service=s,options=chrome_options)
        web.get(url)
        xml = web.page_source
        # if test:
        #     print(f"\n#{get_linenumber()} {xml=}")
        web.quit()
        soup = BeautifulSoup(xml, features='html.parser')

        # pickle.dump(soup, f"test/soup-{slug_from_url(url)}.pkl")
        with open(f"test/soup-{slug_from_url(url)}.pkl", 'wb') as pf:
            pickle.dump(soup, pf)

        output = process_soup(soup)

    return output

def scrape_url(url, v=False, test=False):

    result = scrapee.scrapee_homepage(url, v=v, test=test)

    dict_data_from_scrape = {
        'emails': result['emails'],
        'twitter': result['socials']['twitter'],
        'facebook': result['socials']['facebook'],
        'youtube': result['socials']['youtube'],
        # 'linkedin': result['emails'], # need to add logic in scrapee
        'tiktok': result['socials']['tiktok'],
        'countries': result['locations'],
    }

    return dict_data_from_scrape


def metadata_from_url_request(url, v=False, test=False):
    global name_summary_split
    header = ''
    title = ''
    domain = domain_from_url(url)
    try:
        html = request.urlopen(url).read().decode('utf8')
        # if test:
        #     print(f"\n{html=}")

        try:
            soup = BeautifulSoup(html, "html.parser")
            # if test:
            #     print(f"\n{soup=}")

            try:
                title = soup.title.text
                if '\n' in title:
                    title = title.replace('\n', ' ').strip()
                raw_title = title
                if v:
                    print(f"\n{get_linenumber()} {title=}")

                try:
                    header = soup.find('h1').text
                    if '\n' in header:
                        header = header.replace('\n', ' ').strip()
                    if v:
                        print(f"{get_linenumber()} {header=}")
                    if header in title:
                        header = domain
                    name = title
                    summary = header
                    for split_char in name_summary_split:
                        if split_char in name:
                            parts = name.split(split_char)
                            name = parts[0].strip()
                            summary = parts[1].strip()
                    if v:
                        print(f"{get_linenumber()} {name=}")
                        print(f"{get_linenumber()} {summary=}")

                except Exception as e:
                    print(f"\n{get_linenumber()} h1 ERROR: {e}")
                    name = title
            
            except Exception as e:
                print(f"\n{get_linenumber()} title ERROR: {e}")

        except Exception as e:
            print(f"\n{get_linenumber()} soup ERROR: {e}")

    except Exception as e:
        print(f"\n{get_linenumber()} html ERROR: {e}")
    
    dict_metadata_from_request = {
        'header': header,
        'title': title,
    }

    return dict_metadata_from_request

def meta(url, v=False, test=False):
    global meta_url
    global name_summary_split
    url = url.strip()
    if url.startswith('http'):

        print(f"\n{get_linenumber()} meta test = {test}\n")

        metadata = metadata_from_url_selenium(url, v=v, test=test) # name / title / description

        scrape = scrape_url(url, v=v, test=test) # emails / twitter / facebook / youtube / tiktok / countries

        request_result = metadata_from_url_request(url, v=v, test=test) # header / title

        output = meta_url(
            clean_url = clean_url(url),
            root_website_url = root_url(url),
            domain = domain_from_url(url),
            slug = slug_from_url(url),
            header = request_result['header'],
            title = metadata['title'],
            name = metadata['name'],
            description = metadata['description'],
            tags = '',
            emails = scrape['emails'],
            twitter = scrape['twitter'],
            facebook = scrape['facebook'],
            youtube = scrape['youtube'],
            # linkedin = metadata_from_url_selenium(url, v)['linkedin'],
            tiktok = scrape['tiktok'],
            countries = scrape['countries'],
            logo = '', # type tbc
            )

        if v:
            print(f"\n#{get_linenumber()} {output=}")

        return output

    else:
        msg174 = f"{url} is not a valid URL."
        print(msg174)
        pymsgbox.alert(msg174)

### TESTS

### Global Variable

test = True # for testing
v = False # verbose mode

# output = metadata_from_url_selenium(test_url, v=v)
# output = scrapee.scrapee_homepage(test_url)
# output = scrapee.scrapee_twitter_from_homepage(test_url)
# output = scrapee.scrapee(test_url,max_error_count=10)

for url in list_to_test:
    print(separator())
    test_url = url
    print(f"\n#{get_linenumber()} {test_url=}")

    output = meta(test_url, v=v, test=test)

    print(f"\n{get_linenumber()} output:\n")
    pp.pprint(output._asdict())
    print()
    print(f"len(output) = {len(output)}")
    print(f"type(output) = {type(output)}")
    print()
    print(f"#{get_linenumber()} clean_url \t\t\t{output.clean_url=}")
    print(f"#{get_linenumber()} root_url \t\t\t{output.root_website_url=}")
    print(f"#{get_linenumber()} domain_from_url \t\t{output.domain=}")
    print(f"#{get_linenumber()} slug_from_url \t\t{output.slug=}")
    print(f"#{get_linenumber()} metadata_from_url_request \t{output.header=}")
    print(f"#{get_linenumber()} metadata_from_url_selenium {output.title=}")
    print(f"#{get_linenumber()} metadata_from_url_selenium {output.name=}")
    print(f"#{get_linenumber()} metadata_from_url_selenium {output.description=}")
    print(f"#{get_linenumber()} TODO \t\t\t{output.tags=}")
    print(f"#{get_linenumber()} scrape_url \t\t{output.emails=}")
    print(f"#{get_linenumber()} scrape_url \t\t{output.twitter=}")
    print(f"#{get_linenumber()} scrape_url \t\t{output.facebook=}")
    print(f"#{get_linenumber()} scrape_url \t\t{output.youtube=}")
    print(f"#{get_linenumber()} scrape_url \t\t{output.tiktok=}")
    print(f"#{get_linenumber()} scrape_url \t\t{output.countries=}")
    print(f"#{get_linenumber()} scrape_url \t\t{output.logo=}")

########################################################################################################

if __name__ == '__main__':
    print('-------------------------------')
    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    else:
        print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    print()