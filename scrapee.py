import json
from bs4 import BeautifulSoup
import re
from pprint import pprint
from urllib.parse import urlparse
import difflib
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
##############
import os
import tldextract

# for pickling soup for tests:
import pickle
import sys
sys.setrecursionlimit(10000)

import pprint
pp = pprint.PrettyPrinter(indent=4)

from inspect import currentframe
def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

from dotenv import load_dotenv
load_dotenv()
CHROMEDRIVER = os.environ.get("CHROMEDRIVER")

s = Service(CHROMEDRIVER)
# Main function to run with a url

def slug_from_url(url):
    o = tldextract.extract(url)
    domain_name = o.domain.lower()
    if 'www.' in domain_name:
        domain_name = domain_name.replace('www.','')
    return domain_name


def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    return set(deletes)

def scrapee_homepage(url, v=False, test=False):
    
    email_regex= "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

    final = {

        "socials": {"instagram":[], "facebook": [], "twitter": [], "youtube": [], 'tiktok': []},
        "emails":[],
        "meta": {},
        "pdfs":{},
        "locations": []

    }

    print(f"\nscrapee_homepage test = {test}\n")

    templinks = []
    links = []

    if test:
        pickle_dump_soup = f"test/soup-{slug_from_url(url)}.pkl"
        print(f"\nscrapee_homepage {get_linenumber()} TEST: LOADING FROM PICKLE FILE: {pickle_dump_soup}\n")
        soup_backup = open(pickle_dump_soup, "rb")
        soup = pickle.load(soup_backup)
        # soup object can now be used after if/else statement

        pickle_dump_htmltext = f"test/htmltext-{slug_from_url(url)}.pkl"
        print(f"\nscrapee_homepage {get_linenumber()} TEST: LOADING FROM PICKLE FILE: {pickle_dump_htmltext}\n")
        htmltext_backup = open(pickle_dump_htmltext, "rb")
        htmltext = pickle.load(htmltext_backup)
        # htmltext object can now be used after if/else statement

    else:
        print(f"\nscrapee_homepage {get_linenumber()} RUNNING LIVE SCRAPING OF {url}\n")
        try:
            print(f"scrapee_homepage {get_linenumber()} Crawling site: ",url)
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
            driver.set_page_load_timeout(20)

            driver.get(url)
            htmltext = driver.page_source
            soup = BeautifulSoup(htmltext, 'html.parser')
            driver.close()
            driver.quit()
        except:
            print(f"scrapee_homepage {get_linenumber()} Error Crawling Site: ", url)
            driver.close()
            driver.quit()
            return final
        # soup = BeautifulSoup(htmltext, 'html.parser')
        # save object as file
        if __name__ == '__main__':
            with open(f"test/soup-{slug_from_url(url)}.pkl", 'wb') as pf:
                pickle.dump(soup, pf)
            with open(f"test/htmltext-{slug_from_url(url)}.pkl", 'wb') as pf:
                pickle.dump(htmltext, pf)

    metas = [x for x in soup.find_all('meta')] 

    metas2 = [{x.get('name'): x.get('content')} for x in metas ]
    meta_f = {}
    for dict in metas2:
        for key in dict:
            if key not in meta_f:
                meta_f[key] = dict[key]

    meta = {}

    for (key,value) in meta_f.items():
        if key != None:
            meta[key] = value

    all_matches = []
    company_title = None
    company_desc = None
    company_twitter = None
    for key in meta:
        if meta[key] == None:
            continue
        if 'twitter' in key and company_twitter == None and '@' in meta[key]:
            company_twitter = meta[key]
        if 'description' in key and company_desc == None:
            company_desc = meta[key]
        if 'title' in key and company_title == None:
            company_title = meta[key]
        if ' ' in meta[key].strip():
            value_list = [value.strip().lower() for value in meta[key].strip().split()]
        else:
            value_list = [meta[key].lower()]
        domain = urlparse(url).netloc
        if domain.split('.')[0] != 'www':
            domain = domain.split('.')[0]
        else:
            domain = domain.split('.')[1]
        final_list = []
        for val in value_list:
            all_edits = edits1(val)
            for edit in all_edits:
                if edit not in final_list:
                    final_list.append(edit)
        for edit in edits1(domain):
            close_matches = difflib.get_close_matches(edit, value_list)
            for match in close_matches:
                if match not in all_matches:
                    all_matches.append(match)

    final["meta"] = meta
    final['meta']['company_name'] = ' '.join(all_matches)
    final['meta']['title'] = company_title
    final['meta']['description'] = company_desc

    # soup = BeautifulSoup(htmltext, 'html.parser').find_all('a')
    soup = soup.find_all('a')
    templinks = [str(link.get('href')) for link in soup]

    for link in templinks:
        if link not in links:
            links.append(link)


    tempemails = []
    emails = []

    #Email finder............
    matches = re.findall(email_regex, htmltext)

    if len(matches) > 0:
        for match in matches:
            tempemails.append(match)
    for e in tempemails:
        if e not in emails and not e.endswith('.'):
            emails.append(e)
        
        #end of email finder

    Country = [
    ('US', 'United States'),
    ('AF', 'Afghanistan'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua And Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BA', 'Bosnia And Herzegowina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CV', 'Cape Verde'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Rep'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', 'Cote D`ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('TP', 'East Timor'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French S. Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'Korea (North)'),
    ('KR', 'Korea (South)'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Laos'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macau'),
    ('MK', 'Macedonia'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia'),
    ('MD', 'Moldova'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('AN', 'Netherlands Antilles'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('RE', 'Reunion'),
    ('RO', 'Romania'),
    ('RU', 'Russian Federation'),
    ('RW', 'Rwanda'),
    ('KN', 'Saint Kitts And Nevis'),
    ('LC', 'Saint Lucia'),
    ('VC', 'St Vincent/Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SH', 'St. Helena'),
    ('PM', 'St.Pierre'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SZ', 'Swaziland'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syrian Arab Republic'),
    ('TW', 'Taiwan'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania'),
    ('TH', 'Thailand'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad And Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('UK', 'United Kingdom'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VA', 'Vatican City State'),
    ('VE', 'Venezuela'),
    ('VN', 'Viet Nam'),
    ('VG', 'Virgin Islands (British)'),
    ('VI', 'Virgin Islands (U.S.)'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('YU', 'Yugoslavia'),
    ('ZR', 'Zaire'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe')
]

    if len(links) > 0:

        for link in links:

                if ("instagram.com" in link) and link not in final["socials"]["instagram"]:
                    
                    final["socials"]["instagram"].append(link)
                elif ("facebook.com" in link) and ("facebook.com/share" not in link) and link not in final["socials"]["facebook"]:
                    if link.startswith("/"): link = "https://"+link
                    final["socials"]["facebook"].append(link)
                elif ("youtube.com" in link) and ("youtube.com/watch" not in link) and link not in final["socials"]["youtube"]:
                    if link.startswith("/"): link = "https://"+link
                    final["socials"]["youtube"].append(link)
                elif ("twitter.com" in link) and ("intent" not in link) and 'share' not in link and ("status" not in link) and "hashtag" not in link and link not in final["socials"]["twitter"]:
                    if link.startswith("/"): link = "https://"+link
                    final["socials"]["twitter"].append(link)
                elif ('tiktok.com'  in link) and ('video' not in link) and link not in final['socials']['tiktok']:   
                    if link.startswith("/"): link = "https://"+link
                    final['socials']['tiktok'].append(link) 
                if ".pdf" in link:
                    pdf_name = link.split("/")[len(link.split("/"))-1]
                    final["pdfs"][pdf_name] = link

    for pair in Country:
        if (pair[1] in htmltext) and pair[0] not in final['locations']:
            final["locations"].append(pair[0])

    #Email finder............
    matches = re.findall(email_regex, htmltext)

    if len(matches) > 0:
        for match in matches:
            tempemails.append(match)
    for e in tempemails:
        if e not in emails and not e.endswith('.'):
            emails.append(e)
        
        #end of email finder

    if company_twitter == None:
        if 'socials' in final:
            if 'twitter' in final['socials'] and final['socials']['twitter'] != []:

                company_twitter = '@' +final['socials']['twitter'][0].split('/')[-1]

    final['meta']['twitter'] = company_twitter  

    if test:
        # and soup object gets closed here
        soup_backup.close()

    if v:
        print(f"\nscrapee_homepage final:")
        pp.pprint(final)

    return final
