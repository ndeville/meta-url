import os

# print(f"\n{os.path.basename(__file__)} loaded -----------\n")

keywords_to_remove = [
    '.pdf',
    'protection',
    'login',
    'portfolio',
    'news',
    'founder',
    'jobs',
    'investor',
    'fintech',
    'frequently',
    'insights',
    'faq',
    'mentor',
    'headliner',
]

add_keywords_to_remove = [
        'javascript',
]

# get line numbers
from inspect import currentframe
def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno


# domain utils
import tldextract

# def domain_from_url(url):
    
#     o = tldextract.extract(url)
#     domain = f"{o.domain}.{o.suffix}".lower()
#     if 'www.' in domain:
#         domain = domain.replace('www.','')
#     return domain

def domain_name_from_url(url):
    # import tldextract
    o = tldextract.extract(url)
    domain_name = o.domain.lower()
    if 'www.' in domain_name:
        domain_name = domain_name.replace('www.','')
    return domain_name



def internal(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print()
        print(f"get.links.internal #{get_linenumber()}: {url=}")

    domain_name = domain_name_from_url(url)
    if v: 
        print(f"get.links.internal #{get_linenumber()}: domain_name: {domain_name}")
    
    set_links = set()

    links = soup.find_all('a')

    if v:
        print(f"\nget.links.internal #{get_linenumber()}: {len(links)} links found:")
    for l in links:
        if v:
            print(f"\nget.links.internal #{get_linenumber()}: {l}")
            
        try:
            href = l['href']
            if v:
                print(f"get.links.internal #{get_linenumber()}: {type(href)} {href=}")
            if not any(ele in href for ele in keywords_to_remove):

                if domain_name in href and not href.startswith('/'): # NOT if href startswith as some links will be on a different (sub)domain
                    link = href.strip()
                    set_links.add(link)
                    if v:
                        print(f"get.links.internal #{get_linenumber()}: ADDED {link}")
                else:
                    if v:
                        print(f"get.links.internal #{get_linenumber()}: REMOVED {href} - {domain_name} not in.")

                if href.startswith('/'):
                    link = f"{url}{href.strip()}"
                    set_links.add(link)
                    if v:
                        print(f"get.links.internal #{get_linenumber()}: ADDED {link}")
            else:
                if v:
                    print(f"get.links.internal #{get_linenumber()}: REMOVED {href} - blacklist")
            
        except:
            if v:
                print(f"get.links.internal #{get_linenumber()}: ------ERROR with {l}")
            continue

    set_links = set(sorted(set_links))

    if v:
        print(f"\n---\nget.links.internal #{get_linenumber()}: \nRETURNED set of all INTERNAL links ({len(set_links)}):\n{set_links}.\n---\n")

    return set_links



def all(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    keywords_to_remove = keywords_to_remove + [
        'javascript',
    ]

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\nget.links.all #{get_linenumber()}: {url=}\n")
    
    set_links = set()

    links = soup.find_all('a')

    if v:
        print(f"\nget.links.all #{get_linenumber()}: {len(links)} links found:\n")
    for l in links:
        if v:
            print(f"\nget.links.all #{get_linenumber()}: {l}")
            
        try:
            href = l['href']
            if v:
                print(f"get.links.all #{get_linenumber()}: {type(href)} {href=}")
            if not any(ele in href for ele in keywords_to_remove):

                if not href.startswith('/'):
                    link = href.strip()

                if href.startswith('/'):
                    link = f"{url}{href.strip()}"

                set_links.add(link)
                if v:
                    print(f"get.links.all #{get_linenumber()}: +++ADDED {link}\n\n")
            else:
                print(f"get.links.all #{get_linenumber()}: ---REMOVED {href} - blacklist\n\n")
            
        except:
            print(f"get.links.all #{get_linenumber()}: ------ERROR with {l}\n\n")
            continue

    list_links = list(set_links)

    if v:
        print(f"\n---\nget.links.all #{get_linenumber()}: \nRETURNED list of ALL links ({len(list_links)}):\n{list_links}.\n---\n")

    return list_links


def socials(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    from collections import namedtuple

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\nget.links.socials #{get_linenumber()}: {url=}\n")

    social_names = [
        'twitter',
        'linkedin',
        'facebook',
        'instagram',
        'youtube',
        'medium',
        'github',
        'tiktok',
    ]
    
    socials = namedtuple('Socials', social_names)

    links = soup.find_all('a')

    for l in links:
        try:
            link = l['href']
            # if v:
            #     print(f"\nget.links.socials #{get_linenumber()}: checking {l}")

            if ("twitter.com" in link) and ("intent" not in link) and ('share' not in link) and ("status" not in link) and ("hashtag" not in link):
                if v:
                    print(f"+++ADDED TWITTER {link}")
                socials.twitter = link

            elif ("linkedin.com" in link):
                if v:
                    print(f"+++ADDED LINKEDIN {link}")
                socials.linkedin = link

            elif ("facebook.com" in link) and ("facebook.com/share" not in link):
                if v:
                    print(f"+++ADDED FACEBOOK {link}")
                socials.facebook = link

            elif ("instagram.com" in link):
                if v:
                    print(f"+++ADDED INSTAGRAM {link}")
                socials.instagram = link

            elif ("youtube.com" in link) and ("youtube.com/watch" not in link):
                if v:
                    print(f"+++ADDED YOUTUBE {link}")
                socials.youtube = link

            elif ("medium.com" in link):
                if v:
                    print(f"+++ADDED MEDIUM {link}")
                socials.medium = link

            elif ("github.com" in link):
                if v:
                    print(f"+++ADDED GITHUB {link}")
                socials.github = link

            elif ('tiktok.com'  in link) and ('video' not in link):
                if v:
                    print(f"+++ADDED TIKTOK {link}")
                socials.tiktok = link
            
            # x = person(first='Nic', last='Deville')
        except:
            if v:
                print(f"\nget.links.socials #{get_linenumber()}: ------ERROR with {l}\n")
            continue

    # Cleanup: None where no value

    if not isinstance(socials.twitter, str):
        socials.twitter = None
    if not isinstance(socials.linkedin, str):
        socials.linkedin = None
    if not isinstance(socials.facebook, str):
        socials.facebook = None
    if not isinstance(socials.instagram, str):
        socials.instagram = None
    if not isinstance(socials.youtube, str):
        socials.youtube = None
    if not isinstance(socials.medium, str):
        socials.medium = None
    if not isinstance(socials.github, str):
        socials.github = None
    if not isinstance(socials.tiktok, str):
        socials.tiktok = None

    if v:
        print(f"\n---\nget.links.socials #{get_linenumber()}: NOTE: returns namedtuple of SOCIAL links: {','.join(social_names)}.\n---\n")

    return socials


def files(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    keywords_to_remove = keywords_to_remove + [
        'javascript',
    ]

    file_extensions = (
        '.pdf',
        '.doc',
        '.docx',
        '.xls',
        '.xlsx',
        '.ppt',
        '.pptx',
        '.txt',
        '.csv',
        '.zip',
        '.rar',
        '.7z',
        '.tar',
        '.gz',
        '.tgz',
    )

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\nget.links #{get_linenumber()}: {url=}\n")
    
    set_links = set()

    links = soup.find_all('a')

    # links_files = [x['href'] for x in links if x['href'].endswith(file_extensions)]
    # if v:
    #     print(f"\n{len(links_files)} file links found:\n")
    #     for lf in links_files:
    #         print(f"{lf}")
    #     print()

    for l in links:
        # if v:
        #     print(f"\n#{get_linenumber()}: {l}")
            
        try:
            href = l['href']

            if href.endswith(file_extensions):
                if not any(ele in href for ele in keywords_to_remove):
                    if not href.startswith('/'):
                        link = href.strip()

                    if href.startswith('/'):
                        link = f"{url}{href.strip()}"

                    set_links.add(link)
                    if v:
                        print(f"+++ADDED {link}\n\n")
                else:
                    print(f"---REMOVED {href} - blacklist\n\n")
            else:
                print(f"---REMOVED {href} - wrong extension\n\n")
            
        except:
            print(f"------ERROR with {l}\n\n")
            continue

    list_links = list(set_links)

    if v:
        print(f"\n---\nget.links.files #{get_linenumber()}: \nRETURNED list of all FILES links ({len(list_links)}):\n{list_links}.\n---\n")

    return list_links

########################################################################################################

if __name__ == '__main__':

    url = "https://www.balderton.com/"

    from get.soup import main as get_soup_tuple

    soup_tuple = get_soup_tuple(url)
    # soup = soup_tuple.soup
    # url = soup_tuple.url

    links = all(soup_tuple)

    print(f"\nlinks returned:\n")
    for link in links:
        print(link)
        print()

    # print()
    # print()
    # print('-------------------------------')
    # print(f"{os.path.basename(__file__)}")
    # print()
    # print(f"{count=}")
    # print()
    # print('-------------------------------')
    # run_time = round((time.time() - start_time), 1)
    # if run_time > 60:
    #     print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    # else:
    #     print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    # print()