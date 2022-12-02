import spacy
from thefuzz import fuzz, process
import tldextract

from inspect import currentframe
def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

### Supporting Functions

def domain_name_from_url(url):
    # import tldextract
    o = tldextract.extract(url)
    domain_name = o.domain.lower()
    if 'www.' in domain_name:
        domain_name = domain_name.replace('www.','')
    return domain_name

### MAIN

def main(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    text = soup.get_text()

    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)

    ###
    ## ADD LOGIC TO GET FROM metas.title or metas.site_name
    ## pass get.metadata object to get.name
    ####

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


    root_name = domain_name_from_url(url)

    if len(list_orgs) > 0:
        org_name = process.extractOne(root_name, list_orgs)[0]
    else:
        org_name = None
        
    if v:
        print(f"\nget.name #{get_linenumber()}: {org_name=}")
    
    return org_name
    

    # text = soup.get_text()

    # nlp = spacy.load("en_core_web_trf")
    # doc = nlp(text)

    # list_orgs = []
    # list_countries_found = []

    # if v:
    #     print(f"\nents:\n")
    # for ent in doc.ents:
    #     label = ent.label_
    #     if label == 'ORG' or label == 'PRODUCT':
    #         if v:
    #             print(f"{ent.text} ➤ {ent.label_}")
    #             print()
    #         list_orgs.append(ent.text)
    #     if label == 'GPE':
    #         if v:
    #             print(f"{repr(ent.text)} ➤ {ent.label_}")
    #         if ent.text in list_countries_ref:
    #             list_countries_found.append(ent.text)
    #         if v:
    #             print()

    # if len(list_orgs) > 0:
    #     org = process.extractOne(root_name, list_orgs)[0]
    # else:
    #     org = None

    # if len(list_countries_found) > 0:
    #     country = list_countries_found[0]
    # else:
    #     country = None
        
    # print(f"\n#{org=}")
    # print(f"\n#{country=}")





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