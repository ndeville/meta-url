import os
import spacy
# import tldextract

# print(f"\n{os.path.basename(__file__)} loaded -----------\n")

keywords_to_remove = [
    '.pdf',
    'controller',
    'faq',
    'fintech',
    'founder',
    'frequently',
    'headliner',
    'insights',
    'investor',
    'jobs',
    'login',
    'mentor',
    'news',
    'portfolio',
    'protection',
]

to_remove = [
    'Advisor', 
    'Analyst', # TODO: add logic to exclude person fully
    'CIO', # TODO: add logic to exclude person fully
    'Advisor', # TODO: add logic to exclude person fully
    'Office',
    'Associate',
    'Finance',
    'Budget',
    'Marketing',
]

to_clean = [
            '\n',
            '\uf054',
            '\"',
            '→',
            '+',
            '”',
            '@',
            '×',
            '—',
            '’',
            '“',
            '2021',
            'Accounting',
            'Advisor',
            'Africa',
            'Area',
            'Assistant',
            'Associate',
            'Bio',
            'Board',
            'Business',
            'CCO',
            'CEO',
            'COO',
            'CTO',
            'Chief',
            'Comittee',
            'Companies',
            'Compliance',
            'Connect',
            'Controller',
            'Countries',
            'Director',
            'Entrepreneurial',
            'Executive',
            'Former',
            'Founder',
            'Founding',
            'Fund',
            'General',
            'HR',
            'Head',
            'Interning',
            'Investment',
            'Investor',
            'Linkedin',
            'Manager',
            'Managing',
            'Member',
            'Network',
            'Operating',
            'Operations',
            'Paris',
            'Partner',
            'President',
            'Principal',
            'Recognized',
            'Relations',
            'SENIOR',
            'Senior',
            'Shanghai',
            'Sales',
            'Scientific',
            'Senior',
            'Specialist',
            'Storefront',
            'Strategic',
            'Talent',
            'Team',
            'Venture',
            'Vice',
]

add_keywords_to_remove = [
        'javascript',
]

### Supporting Functions

# script name
loc = "get/team"
# get line numbers
from inspect import currentframe
def ln(): # print line numbers with f"{ln()}"
    cf = currentframe()
    return cf.f_back.f_lineno


def clean_string(string):
    global to_clean

    # TODO: extract to CSV / add \n separately


    for item in to_clean:
        if item in string:
            string = string.replace(item, ' ')

    return string.strip()


### MAIN

def main(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    global to_clean
    global to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\n---\n{loc} #{ln()}: parsing {url}\n")

    set_people_found = set()

    text = soup.get_text()

    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)

    # if v:
    #     print(f"\nents:\n")
    count_person = 0
    if v:
        print(f"\n{loc} #{ln()}: {len(doc.ents)} entities in doc.ents:\n")
    for ent in doc.ents:
        
        label = ent.label_

        if v:
            print(f"{loc} #{ln()}: {label} ➤ {ent}")

        if label == 'PERSON':
            count_person += 1
            person = ent.text
            if v:
                print(f"{loc} #{ln()}: {count_person} {repr(person)} ➤ {label}")
            if ' ' in person: # remove single-word names
                if not any(ele in person for ele in keywords_to_remove): # remove people with specific keywords listed in to_remove
                    set_people_found.add(clean_string(person))
                else:
                    print(f"{loc} #{ln()}: ------REMOVING: {person}")

    sorted_list_people_found = sorted(set_people_found)

    if v:
        print(f"\n{loc} #{ln()}: {len(sorted_list_people_found)} records in sorted_list_people_found:")
        for p in sorted_list_people_found:
            print(f"{loc} #{ln()}: {repr(p)}")

    dict_to_return = {}
    for person in sorted_list_people_found:
        dict_to_return[person.title()] = url

    return dict_to_return


########################################################################################################

if __name__ == '__main__':
    
    print()