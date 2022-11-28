from datetime import datetime
import os
print("----------")
ts_file = f"{datetime.now().strftime('%y%m%d-%H%M')}"
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"{ts_time} starting {os.path.basename(__file__)}")
import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
USER = os.getenv("USER")

import sys
sys.path.append(f"/Users/{USER}/Python/indeXee")

import my_utils
# import grist_BB
# import grist_PE
# import dbee

from inspect import currentframe
def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

import pprint
pp = pprint.PrettyPrinter(indent=4)

count = 0
count_row = 0

test = True
v = False # verbose mode

print(f"{os.path.basename(__file__)} boilerplate loaded -----------\n")
####################
# Get Company Name and Country from URL

### Script-specific imports

# for scraping website text
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import dotenv_values
# for NLP entitites extraction
import spacy
# for fuzzy matching:
from thefuzz import fuzz, process


### Global Variables


config = dotenv_values(".env")
driverpath = config['CHROMEDRIVER']
if v:
    print(f"\n#{get_linenumber()} {driverpath=}\n")
regex_url = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

list_countries_ref = list(my_utils.dict_country)
if v:
    for c in sorted(list_countries_ref):
        print(repr(c))

### Functions


def scrapee_company_details(url,source=None,test=False):
    global v

    root_name = my_utils.domain_name_from_url(url)
    if v:
        print(f"\n#{get_linenumber()} {root_name=}\n")

    #Selenium
    s = Service(driverpath)
    opts = webdriver.ChromeOptions()
    opts.add_argument("start-maximized") #// https://stackoverflow.com/a/26283818/1689770
    opts.add_argument("enable-automation")# // https://stackoverflow.com/a/43840128/1689770
    opts.add_argument("--headless") #// only if you are ACTUALLY running headless
    opts.add_argument("--no-sandbox")# //https://stackoverflow.com/a/50725918/1689770
    opts.add_argument("--disable-infobars")# //https://stackoverflow.com/a/43840128/1689770
    opts.add_argument("--disable-dev-shm-usage")# //https://stackoverflow.com/a/50725918/1689770
    opts.add_argument("--disable-browser-side-navigation")# //https://stackoverflow.com/a/49123152/1689770
    opts.add_argument("--disable-gpu")# //https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc
    opts.add_argument('--log-level=3')
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=s,options=opts)
    # driver = webdriver.Chrome(driverpath,options=opts)
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(25)
    driver.get(url)
    htmltext = driver.page_source
    driver.quit()

    # Try to get Company Name and Country from homepage

    soup = BeautifulSoup(htmltext, 'html.parser')

    text = soup.get_text()

    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)

    list_orgs = []
    list_countries_found = []

    if v:
        print(f"\nents:\n")
    for ent in doc.ents:
        label = ent.label_
        if label == 'ORG' or label == 'PRODUCT':
            if v:
                print(f"{ent.text} ➤ {ent.label_}")
                print()
            list_orgs.append(ent.text)
        if label == 'GPE':
            if v:
                print(f"{repr(ent.text)} ➤ {ent.label_}")
            if ent.text in list_countries_ref:
                list_countries_found.append(ent.text)
            if v:
                print()

    if len(list_orgs) > 0:
        org = process.extractOne(root_name, list_orgs)[0]
    else:
        org = None

    if len(list_countries_found) > 0:
        country = list_countries_found[0]
    else:
        country = None
        
    print(f"\n#{org=}")
    print(f"\n#{country=}")





    # ### TODO: scrape from legal link if not found on homepage

    # #Get all valid links
    # soup = BeautifulSoup(htmltext, 'html.parser').find_all('a')
    # templinks = [str(link.get('href')) for link in soup]
    # links = []
    # for link in templinks:
    #     if link not in links and (link.startswith('http') or link.startswith('www')):
    #         links.append(link)

    # #Check all of the domains of links gathered from the landing page
    # for link in links:
    #     domain = link.strip().split('//')[1].split('/')[0].strip()
    #     for dom in domains:
    #         if dom in domain:
    #             final_data.append(link)
    #         else: continue

    #     return final_data



scrapee_company_details('https://revos.ai/legal/app/privacy.html')


########################################################################################################

if __name__ == '__main__':
    print()
    print()
    print('-------------------------------')
    print(f"{os.path.basename(__file__)}")
    print()
    print(f"{count=}")
    print()
    print('-------------------------------')
    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    else:
        print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    print()