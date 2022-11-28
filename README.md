# metaURL
Fetch metadata from URL

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
            'clean_url',  # str / inline 
            'clean_root_url', # str / inline
            'domain', # str / inline
            'slug', # str / inline
            'header', # str / find_header
            'title', # str / find_title
            'name', # str / find_name
            'description', # str
            'tags', # list / find_tags (method tbc)
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
            'logo', # bin / find_logo (Clearbit)
            'whois', # tbc / whois (optional)
            'team', # list / NLP PERSON on team page
            ]
            )
```