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
            'clean_url',  # str / inline (working)
            'clean_root_url', # str / inline (working)
            'domain', # str / inline (working)
            'slug', # str / inline (working)
            'header', # str / find_header
            'title', # str / find_title
            'name', # str / find_name
            'description', # str
            'tags', # list / find_tags (optional for now, method tbc)
            'contact_pages', # list / find_contact_pages
            'emails', # list / find_emails
            'phone', # string / find_phone
            'email_patterns', # list / find_email_patterns (method tbc)
            'twitter', # list / find_socials
            'facebook', # str / find_socials
            'youtube', # str / find_socials
            'linkedin', # str / find_socials
            'tiktok', # str / find_socials
            'countries', # list / find_countries
            'logo', # bin / find_logo (working w/ Clearbit)
            'whois', # tbc / whois (optional)
            'team', # list / NLP PERSON on team page (TODO priority)
            ]
            )
```