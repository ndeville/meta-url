# metaURL
Fetch metadata from URL (using Selenium)

[Project notes](https://notes.nicolasdeville.com/projects/metaurl/)

Work in progress.  

Use should be as follow:

``` python
from meta_url import meta

url = 'https://...'

x = meta(url)
```

Output shoud be: 

``` python
### namedtuple to be returned
namedtuple('metaURL', 
            [
            'clean_url',  # str / inline (WORKING)
            'clean_root_url', # str / inline (WORKING)
            'domain', # str / inline (WORKING)
            'slug', # str / inline (WORKING)
            'header', # str / find_header
            'title', # str / find_title
            'name', # str / find_name
            'description', # str
            'tags', # list / find_tags (optional for now, method tbc)
            'contact_pages', # list / find_contact_pages
            'emails', # list / find_emails
            'phone', # string / find_phone
            'email_patterns', # list / find_email_patterns (method tbc)
            'twitter', # list / find_socials (WORKING)
            'facebook', # str / find_socials (WORKING)
            'youtube', # str / find_socials (WORKING)
            'linkedin', # str / find_socials
            'tiktok', # str / find_socials
            'countries', # list / find_countries
            'logo', # bin / find_logo (working w/ Clearbit)
            'whois', # tbc / whois (optional)
            'team', # list / NLP PERSON on team page (TODO priority)
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
