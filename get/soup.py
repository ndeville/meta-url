import os

from dotenv import load_dotenv
load_dotenv()
PROJECTS_FOLDER = os.getenv("PROJECTS_FOLDER")
SCRAPINGANT_API_KEY = os.getenv("SCRAPINGANT_API_KEY")

import sys
sys.path.append(f"{PROJECTS_FOLDER}/indeXee")

# from check_ip import check_ip
import my_utils

# print(f"\n{os.path.basename(__file__)} loaded -----------\n")

from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from collections import namedtuple
import requests
import http.client

# Driver management / Chrome
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# driverpath = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

from dotenv import dotenv_values
config = dotenv_values(".env")
# driverpath = config['CHROMEDRIVER']
driverpath = os.getenv("CHROMEDRIVER")

# Supporting functions

# script name
loc = f">get/soup"

# get line numbers
from inspect import currentframe
def ln():
    """
    print line numbers with f"{ln()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

# MAIN

# 230414-0735 Old function, using requests

# def main(url,test=False,v=False):

#     # Moved to main script to avoid multiple checks on same run
#     # ip = my_utils.check_my_ip()
#     # if not ip: # False == using VPN
#     #     print(f"{loc} #{ln()} ❌ EXPOSED crawling {url} (true IP used). STOP.")
#     # else: # True == using my IP
#     #     print(f"{loc} #{ln()} ✅ PROTECTED crawling {url}")

#     if v:
#         print(f"        NOTE: {loc}.main returns a namedtuple with .url and .soup\n")

#     soup_tuple = namedtuple('soup_dict', ['url', 'soup'])


#     if v: 
#         print(f"\n{loc} #{ln()}: Processing {url=}")

#     #Selenium
#     s = Service(driverpath)
#     opts = webdriver.ChromeOptions()
#     opts.add_argument("start-maximized") #// https://stackoverflow.com/a/26283818/1689770
#     opts.add_argument("enable-automation")# // https://stackoverflow.com/a/43840128/1689770
#     opts.add_argument("--headless") #// only if you are ACTUALLY running headless
#     opts.add_argument("--no-sandbox")# //https://stackoverflow.com/a/50725918/1689770
#     opts.add_argument("--disable-infobars")# //https://stackoverflow.com/a/43840128/1689770
#     opts.add_argument("--disable-dev-shm-usage")# //https://stackoverflow.com/a/50725918/1689770
#     opts.add_argument("--disable-browser-side-navigation")# //https://stackoverflow.com/a/49123152/1689770
#     opts.add_argument("--disable-gpu")# //https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc
#     opts.add_argument('--log-level=3')
#     opts.add_experimental_option('excludeSwitches', ['enable-logging'])

#     driver = webdriver.Chrome(service=s,options=opts)
#     # driver = webdriver.Chrome(driverpath,options=opts)
    
#     driver.set_page_load_timeout(25)
#     driver.get(url)
#     driver.implicitly_wait(10) # not working??
#     htmltext = driver.page_source
#     driver.quit()

#     soup = BeautifulSoup(htmltext, 'html.parser')

#     if v:
#         print(f"from {loc}: {soup}")

#     output = soup_tuple(url=url, soup=soup)

#     return output






# 230414-0735 New function (ScrapingAnt) / WITHOUT JS rendering == 1 credit

def without_js_rendering(url,test=False,v=False):

    soup_tuple = namedtuple('soup_dict', ['url', 'soup'])

    request_url = 'https://api.scrapingant.com/v2/general'

    # First try with browser=False, 1 credit, no JS rendering
    params = {
        'url': url,
        'x-api-key': SCRAPINGANT_API_KEY,
        'browser': False, # WITHOUT JS rendering / 1 credit
        'proxy_country': 'GB', # default: world
        'return_page_source': True, # default: False
    }

    response = requests.get(request_url, params=params)

    if response.status_code >= 400:

        print(f"⚠️ ❗️ ScrapingAnt says Error {response.status_code}: {response.reason}")

    html_text = response.text

    if v:
        print(f"from {loc}: {html_text}")

    soup = BeautifulSoup(html_text, 'html.parser')

    if url.endswith('/'):
        url = url[:-1]

    output = soup_tuple(url=url, soup=soup)

    return output



# WITH JS rendering == 10 credits

def with_js_rendering(url,test=False,v=False):

    print(f"ℹ️  Trying again with JS rendering (10 credits) as no Title returned in first try.")

    soup_tuple = namedtuple('soup_dict', ['url', 'soup'])

    request_url = 'https://api.scrapingant.com/v2/general'

    # First try with browser=False, 1 credit, no JS rendering
    params = {
        'url': url,
        'x-api-key': SCRAPINGANT_API_KEY,
        'browser': True, # WITH JS rendering / 10 credits
        'proxy_country': 'GB', # default: world
        'return_page_source': True, # default: False
    }

    response = requests.get(request_url, params=params)

    if response.status_code >= 400:

        print(f"⚠️ ❗️ ScrapingAnt says Error {response.status_code}: {response.reason}")

    html_text = response.text

    if v:
        print(f"from {loc}: {html_text}")

    soup = BeautifulSoup(html_text, 'html.parser')

    if url.endswith('/'):
        url = url[:-1]

    output = soup_tuple(url=url, soup=soup)

    return output








# # 230415-0727 Testing with ScrapingAnt Python Client

# from scrapingant_client import ScrapingAntClient, ScrapingantClientException, ScrapingantInvalidInputException

# client = ScrapingAntClient(token=SCRAPINGANT_API_KEY)

# RETRIES_COUNT = 3


# def main(url,test=False,v=False):
#     global client
#     global RETRIES_COUNT

#     soup_tuple = namedtuple('soup_dict', ['url', 'soup'])

#     success = False

#     for retry_number in range(RETRIES_COUNT):

#         try:
#             scrapingant_response = client.general_request(
#                 url,
#             )
#         except ScrapingantInvalidInputException as e:
#             print(f'Got invalid input exception: {{repr(e)}}')
#             break  # We are not retrying if request params are not valid
#         except ScrapingantClientException as e:
#             print(f'Got ScrapingAnt exception {repr(e)}')
#         except Exception as e:
#             print(f'Got unexpected exception {repr(e)} - please report this kind of exceptions by creating a new issue')
#         else:

#             html_text = scrapingant_response.content

#             if v:
#                 print(f"from {loc}: {html_text}")

#             soup = BeautifulSoup(html_text, 'html.parser')

#             output = soup_tuple(url=url, soup=soup)

#             success = True

#             break

#     if success:
#         return output
#     else:
#         return print(f"⚠️ ❗️ ScrapingAnt Error")
