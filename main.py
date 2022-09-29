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

### while building / debugging:
from inspect import currentframe
def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

def separator(count=50, lines=3, symbol='='):
    separator = f"{symbol * count}" + '\n'
    separator = f"\n{separator * lines}"
    print(separator)

import pprint
pp = pprint.PrettyPrinter(indent=4)

count = 0
count_row = 0

### Global Variable

test = True # for testing
v = True # verbose mode

test_url = os.getenv("test_url") # to avoid pushing test url to Github / replace os.getenv with value
if v:
    print(f"\n#{get_linenumber()} {test_url=}")

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
            'summary', # str
            'tags', # list
            'emails', # list
            'twitter',
            'facebook',
            'youtube',
            'linkedin',
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
    return f'{scheme}{purl.netloc}{purl.path}'

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
            summary = parts[1].strip()
    print(f"Not done yet")

def metadata_from_url_selenium(url, v=False):
    if v:
        print(f"\n#{get_linenumber()} starting metadata_from_url_selenium with {url}")

    # empty placeholders / to ensure return if fail
    emails = ''
    twitter = ''
    facebook = ''
    youtube = ''
    linkedin = ''
    tiktok = ''
    countries = ''

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
    # if test:
    #     print(f"\n#{get_linenumber()} {soup=}")
    metas = [x for x in soup.find_all('meta') if x.get('property')]
    if v:
        print(f"\n#{get_linenumber()} metas:\n")
        pp.pprint(metas)
    
    result = [{x.get('property'): x.get('content')} for x in metas] # list of dicts
    if v:
        print(f"\n#{get_linenumber()} {result=}")

    dict_metadata_from_selenium = {
        'emails': emails,
        'twitter': twitter,
        'facebook': facebook,
        'youtube': youtube,
        'linkedin': linkedin,
        'tiktok': tiktok,
        'countries': countries,

    }

    return dict_metadata_from_selenium

def metadata_from_url_request(url, v=False):
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

def meta(url, v=False):
    global meta_url
    global name_summary_split
    url = url.strip()
    if url.startswith('http'):

        metadata = metadata_from_url_selenium(url)

        output = meta_url(
            clean_url = clean_url(url),
            root_website_url = root_url(url),
            domain = domain_from_url(url),
            slug = slug_from_url(url),
            header = metadata_from_url_request(url, v)['header'],
            title = metadata_from_url_request(url, v)['title'],
            name = '',
            summary = '',
            tags = '',
            emails = metadata_from_url_selenium(url, v)['emails'],
            twitter = metadata_from_url_selenium(url, v)['twitter'],
            facebook = metadata_from_url_selenium(url, v)['facebook'],
            youtube = metadata_from_url_selenium(url, v)['youtube'],
            linkedin = metadata_from_url_selenium(url, v)['linkedin'],
            tiktok = metadata_from_url_selenium(url, v)['tiktok'],
            countries = metadata_from_url_selenium(url, v)['countries'],
            logo = '', # type tbc
            )

        if v:
            print(f"\n#{get_linenumber()} {output=}")

        return output

    else:
        msg174 = f"{url} is not a valid URL."
        print(msg174)
        pymsgbox.alert(msg174)


output = meta(test_url)

if test:
    print(f"\n{get_linenumber()} output:\n")
    pp.pprint(output._asdict())
    print()
    print(f"len(output) = {len(output)}")
    print(f"type(output) = {type(output)}")

########################################################################################################

if __name__ == '__main__':
    print('-------------------------------')
    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    else:
        print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    print()