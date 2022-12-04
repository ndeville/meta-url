# process.emails

"""
emails: return a list of emails not assigned to team / add to separate table in Grist
"""

from collections import namedtuple
from inspect import currentframe

# Supporting functions

# script name
loc = f"process/emails"

# get line numbers
from inspect import currentframe
def ln():
    """
    print line numbers with f"{ln()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

def email_to_pattern(email,first_name,last_name,v=False):

    first_name = first_name.strip().lower()
    last_name = last_name.strip().lower()
    email_prefix = email.strip().lower().split("@")[0]
    if v:
        print(f"\n{loc} #{ln()}: first_name: {first_name}")
        print(f"{loc} #{ln()}: last_name: {last_name}")
        print(f"{loc} #{ln()}: email_prefix: {email_prefix}")

    email_pattern = ''

    if '.' in email_prefix:
        parts = email_prefix.split(".")
        if parts[0] == first_name and parts[1] == last_name:
            email_pattern = "first.last"
        if parts[0] == last_name and parts[1] == first_name:
            email_pattern = "last.first"
        if parts[0] == first_name[0] and parts[1] == last_name:
            email_pattern = "f.last"
        if parts[0] == first_name and parts[1] == last_name[0]:
            email_pattern = "first.l"
    else:
        if email_prefix == f"{first_name[0]}{last_name}":
            email_pattern = "flast"
        if email_prefix == first_name:
            email_pattern = "first"
        if email_prefix == last_name:
            email_pattern = "last"
        if email_prefix == f"{first_name}{last_name}":
            email_pattern = "firstlast"
        if email_prefix == f"{last_name}{first_name[0]}":
            email_pattern = "lastf"
        if email_prefix == f"{first_name}{last_name[0]}":
            email_pattern = "firstl"
        if email_prefix == f"{last_name}{first_name}":
            email_pattern = "lastfirst"

    if v:
        print(f"{loc} #{ln()}: email_pattern: {email_pattern}")

    return email_pattern

# MAIN

def main(emails, team, domain, v=False, test=False):
    if v:
        print(f"\n---\n{loc} #{ln()}: processing {len(emails)} emails:")
        print(f"{emails}")
        print(f"\n---\n{loc} #{ln()}: processing team {team}")

    dict_emails_to_return = {}

    """
    returns dict_emails_to_return
    with:
    - list of dicts with emails, associated with Team person where possible
    - list of email pattern(s)
    """

    emails_dict = {}

    for em,url in emails.items():
        if v:
            print(f"\n{loc} #{ln()}: processing {em}")
        
        email_prefix = em.split('@')[0].lower()

        for person,person_url in team.items():
            first_name = person.split(' ')[0].lower()
            last_name = person.split(' ')[1].lower()
            if last_name in email_prefix:
                if v:
                    print(f"{loc} #{ln()}: {last_name} matches {email_prefix}")
                emails_dict[em] = {
                    'type': 'person',
                    'person': person,
                    'src': url,
                    }
            elif first_name == email_prefix:
                if v:
                    print(f"{loc} #{ln()}: {first_name} matches {email_prefix}")
                emails_dict[em] = {
                    'type': 'person',
                    'person': person,
                    'src': url,
                    }

    # Add missing emails

    list_emails_remaining = [x for x in emails if x not in [email for email,v in emails_dict.items()]]

    list_generic_email_prefixes = []

    new_team = team
    if v:
        print(f"\n{loc} #{ln()}: new_team: {new_team}")

    for email_remaining in list_emails_remaining:
        email_pref = email_remaining.split('@')[0].lower()
        if email_pref.lower() in list_generic_email_prefixes:
            emails_dict[email_remaining] = {
                'type': 'generic',
                'person': 'n/a',
                'src': url,
                }

        elif '.' in email_pref:
            new_person = email_pref.replace('.',' ').title()
            new_team.append(new_person)
            emails_dict[email_remaining] = {
                'type': 'person',
                'person': new_person,
                'src': url,
                }

        else:
            emails_dict[email_remaining] = {
                        'type': 'unassigned',
                        'person': 'n/a',
                        'src': url,
                        }

    if v:
        print(f"\n{loc} #{ln()}: {len(emails_dict)} emails after processing")


    ### Email Patterns

    list_email_patterns = []
    for email,v in emails_dict.items():
        if v['type'] == 'person':
            # email_prefix = email.split('@')[0].lower()
            name = v['person'].lower()
            first_name = name.split(' ')[0]
            last_name = name.split(' ')[1]

            email_pattern = email_to_pattern(email,first_name,last_name,v=True)

            if email_pattern not in [None, '']:
                list_email_patterns.append(email_pattern)

    list_email_patterns = list(sorted(set(list_email_patterns)))
    list_email_patterns = [f"{x}@{domain}" for x in list_email_patterns]

    if v:
        print(f"\n{loc} #{ln()}: new_team {new_team}")

    dict_emails_to_return['emails'] = emails_dict
    dict_emails_to_return['email_patterns'] = list_email_patterns
    dict_emails_to_return['team'] = new_team
    

    return dict_emails_to_return
