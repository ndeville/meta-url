import os

from dotenv import load_dotenv
load_dotenv()
PROJECTS_FOLDER = os.getenv("PROJECTS_FOLDER")

import sys
sys.path.append(f"{PROJECTS_FOLDER}/indeXee")

# from check_ip import check_ip
import my_utils

# print(f"\n{os.path.basename(__file__)} loaded -----------\n")

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from collections import namedtuple

# Driver management / Chrome
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# driverpath = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

from dotenv import dotenv_values
config = dotenv_values(".env")
driverpath = config['CHROMEDRIVER']

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

def main(url,test=False,v=False):

    ip = my_utils.check_my_ip()
    if not ip: # False == using VPN
        print(f"{loc} #{ln()} ❌ EXPOSED crawling {url} (true IP used). STOP.")
    else: # True == using my IP
        print(f"{loc} #{ln()} ✅ PROTECTED crawling {url}")

    if v:
        print(f"        NOTE: {loc}.main returns a namedtuple with .url and .soup\n")

    soup_tuple = namedtuple('soup_dict', ['url', 'soup'])


    if v: 
        print(f"\n{loc} #{ln()}: Processing {url=}")

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
    
    driver.set_page_load_timeout(25)
    driver.get(url)
    driver.implicitly_wait(10) # not working??
    htmltext = driver.page_source
    driver.quit()

    soup = BeautifulSoup(htmltext, 'html.parser')

    if v:
        print(f"from {loc}: {soup}")

    output = soup_tuple(url=url, soup=soup)

    return output

# test = main('http://baleencap.com/')


# print(f"{test.url=}")
# print()
# print(f"{test.soup=}")



from datetime import datetime
import os
ts_file = f"{datetime.now().strftime('%y%m%d-%H%M')}"
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"\n---------- {ts_time} starting {os.path.basename(__file__)}")
import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
PROJECTS_FOLDER = os.getenv("PROJECTS_FOLDER")

import sys
sys.path.append(f"/Users/{PROJECTS_FOLDER}/indeXee")


import pprint
pp = pprint.PrettyPrinter(indent=4)

####################
# SCRIPT_TITLE

# IMPORTS (script-specific)



# GLOBALS



count_total = 0
count = 0
count_row = 0

test = True
v = True # verbose mode


# FUNCTIONS



# MAIN




########################################################################################################

if __name__ == '__main__':
    print('\n\n-------------------------------')
    print(f"\n{count_total=}")
    print(f"{count=}")
    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'\n{os.path.basename(__file__)} finished in {run_time/60} minutes.\n')
    else:
        print(f'\n{os.path.basename(__file__)} finished in {run_time}s.\n')