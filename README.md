# metaURL
Fetch metadata from URL

[Project notes](https://notes.nicolasdeville.com/projects/metaurl/)

Work in progress.  

Use should be as follow:

``` python
from meta_url import meta

url = 'https://...'

x = meta(url)

print(x.title)
print(x.slug)
print(x.twitter)
etc...
```

Output: namedtuple with    

- clean URL with path
- root website (ie without path)
- domain
- slug
- header
- title
- name
- summary
- tags
- emails
- email patterns
- phone
- facebook
- twitter
- linkedin
- youtube
- tiktok
- country(ies)
- logo
- whois data