# metaURL
Fetch metadata from URL (using Selenium)

[Project notes](https://notes.nicolasdeville.com/projects/metaurl/)

Work in progress.  

# Requirements

- Selenium: for headless browser
- BeautifulSoup: for web scraping
- SpaCY: for NLP (identification of people, places and organisations)

# Usage

``` python
from meta_url import meta

url = 'https://...'

x = meta(url)
```

Output: 

``` python
### namedtuple to be returned
namedtuple('metaURL', 
            [
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
            )
```

# Notes on fields to return

## `team`

- NLP library `Spacy` does a good job at finding PERSON entities. 
- list needs to be extracted from a page with `team`, `about` or similar in the URL OR a section on the home page with `team` in div (to avoid capturing people from other companies, eg recommendations).    

## `countries`

- will return multiple countries in many cases 
- can return US region (eg `CA`) / need to implement logic for that
- URLs with `/legal`, `/privacy`, etc.. are a good place to get that information re HQ BUT includes often references to jurisdictions (eg EU for GDPR) / need to figure out logic

## `emails`

- need to blacklist emails with prefix including `dpo`, `gdpr`, etc.. to narrow down on main generic email address

## `name`

- company name is best extracted in homepage footer or `/legal`/`/privacy` type pages.
- needs to be identified based on root domain matching using `thefuzz` library (`from thefuzz import fuzz`)

## `tags`

- need to find best solution to identify keywords from homepage only

## `contact_pages`

- any page on the domain with `contact` in the URL, else use homepage.   

## `email_pattern`

- this can only be identified if a non-generic email address (ie person email) is present on the website. 




Open-source project originated as part of work at [BtoBSales.EU](https://btobsales.eu)