# process.emails

"""
emails: return a list of emails not assigned to team / add to separate table in Grist
"""

from collections import namedtuple
from inspect import currentframe

# Supporting functions

def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

# MAIN

def main(emails, team, v=False, test=False):
    if v:
        print(f"\n---\nprocess.emails #{get_linenumber()}: processing {len(emails)} emails")

    dict_emails_to_return = {}

    """
    returns dict_emails_to_return
    with:
    - list of dicts with emails, associated with Team person where possible
    - list of email pattern(s)
    """

    # email_field_names = [
    #     'address',
    #     'type', # person, generic or unassigned
    #     'person', 
    #     'src', 
    #     ]

    # emails_list_namedtuples = []
    # emails_list_dicts = []
    emails_dict = {}

    for em,url in emails.items():
        if v:
            print(f"\nprocess.emails #{get_linenumber()}: processing {em}")
        
        # email = namedtuple('Email', email_field_names)

        email_prefix = em.split('@')[0].lower()

        for person in team:
            last_name = person.split(' ')[1].lower()
            if last_name in email_prefix:
                if v:
                    print(f"\nprocess.emails #{get_linenumber()}: {last_name} matches {email_prefix}")
                # email = {}
                # email['email'] = em
                # email['type'] = 'person'
                # email['person'] = person
                # email['src'] = url
                # emails_list_namedtuples.append(email)
                # emails_list_dicts.append(email)
                emails_dict[em] = {
                    'type': 'person',
                    'person': person,
                    'src': url,
                    }

    # Add missing emails
    # TODO add emails not assigned to person

    # for x in emails_dict:
        

    if v:
        print(f"\nprocess.emails #{get_linenumber()}: {len(emails_dict)} emails after processing")


    ### Email Patterns

    list_email_patterns = []
    # TODO

    list_email_patterns = sorted(set(list_email_patterns))

    dict_emails_to_return['emails'] = emails_dict
    dict_emails_to_return['email_patterns'] = list_email_patterns

    return dict_emails_to_return
