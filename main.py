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

test = False # for testing
v = True # verbose mode

test_url = os.getenv("test_url") # to avoid pushing test url to Github / replace os.getenv with value
if v:
    print(f"\n#{get_linenumber()} {test_url=}")

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

    name_summary_split = [
    '|',
    ':',
    '-',
    '·',
    ]

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

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')

    s = Service(driverpath)
    web = Chrome(service=s,options=chrome_options)
    web.get(url)
    xml = web.page_source
    if test:
        print(f"\n#{get_linenumber()} {xml=}")
    web.quit()
    soup = BeautifulSoup(xml, features='html.parser')
    if test:
        print(f"\n#{get_linenumber()} {soup=}")
    metas = [x for x in soup.find_all('meta') if x.get('property')]
    if v:
        print(f"\n#{get_linenumber()} metas:\n")
        pp.pprint(metas)
    
    return [{x.get('property'): x.get('content')} for x in metas] # list of dicts

output = metadata_from_url_selenium(test_url, v=v)



print(f"\n#{get_linenumber()} output:\n")
pp.pprint(output)

########################################################################################################

if __name__ == '__main__':
    print('-------------------------------')
    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    else:
        print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    print()