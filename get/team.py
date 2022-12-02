import os
import spacy
# import tldextract

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

### Supporting Functions

# get line numbers
from inspect import currentframe
def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno


def clean_string(string):

    # TODO: extract to CSV / add \n separately
    to_clean = [
    'Partner',
    'Founder',
    'Founding',
    'Venture',
    'Area',
    '\n',
    'Operating',
    'Recognized',
    'Managing',
    'General',
    'Chief',
    'Director',
    'Executive',
    'Talent',
    'Board',
    'Head',
    'Senior',
    'SENIOR',
    'Operations',
    'Entrepreneurial',
    'Investor',
    'Former',
    'Member',
    'Scientific',
    'CCO',
    'Operations',
    'Manager',
    'CTO',
    'HR',
    'COO',
    'Vice',
    'Comittee',
    'Interning',
    'Fund',
    'Business',
    'Principal',
    'Investment',
    'Sales',
    'Specialist',
    ]

    for item in to_clean:
        if item in string:
            string = string.replace(item, ' ')

    return string.strip()


### MAIN

def main(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):
    global add_keywords_to_remove
    keywords_to_remove = keywords_to_remove + add_keywords_to_remove

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    if v:
        print(f"\n---\nget.team #{get_linenumber()}: parsing {url}\n")

    set_people_found = set()

    text = soup.get_text()

    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)

    # if v:
    #     print(f"\nents:\n")
    count_person = 0
    if v:
        print(f"\nget.team #{get_linenumber()}: {len(doc.ents)} entities in doc.ents:\n")
    for ent in doc.ents:
        
        label = ent.label_

        if v:
            print(f"get.team #{get_linenumber()}: {label} ➤ {ent}")

        if label == 'PERSON':
            count_person += 1
            person = ent.text
            if v:
                print(f"get.team #{get_linenumber()}: {count_person} {repr(person)} ➤ {label}")
            if ' ' in person: # remove single-word names
                if not any(ele in person for ele in keywords_to_remove): # remove people with specific keywords listed in to_remove
                    set_people_found.add(clean_string(person))
                else:
                    print(f"get.team #{get_linenumber()}: ------REMOVING: {person}")

    sorted_list_people_found = sorted(set_people_found)

    if v:
        print(f"\nget.team #{get_linenumber()}: {len(sorted_list_people_found)} records in sorted_list_people_found:")
        for p in sorted_list_people_found:
            print(f"get.team #{get_linenumber()}: {repr(p)}")

    return list(sorted_list_people_found)


########################################################################################################

if __name__ == '__main__':

    print()