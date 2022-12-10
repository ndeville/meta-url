# process/team

import pprint
pp = pprint.PrettyPrinter(indent=4)

"""
team: return a dict with first / last / full / email / title / src
"""

# from collections import namedtuple
from inspect import currentframe

# Supporting functions

loc = f"process/team"

def ln(): # print line numbers with f"{ln()}"
    cf = currentframe()
    return cf.f_back.f_lineno

def generate_email(email_pattern,first,last,v=False):
    if v:
        print(f"{loc} #{ln()} generate_email: email_pattern: {email_pattern}")
        print(f"{loc} #{ln()} generate_email: first: {first}")
        print(f"{loc} #{ln()} generate_email: last: {last}")

    first = first.lower()
    last = last.lower()
    email = ''

    if 'first.last@' in email_pattern:
        email = email_pattern.replace('first.last@', f"{first}.{last}@")
    elif 'last.first@' in email_pattern:
        email = email_pattern.replace('last.first@', f"{last}.{first}@")
    elif 'f.last@' in email_pattern:
        email = email_pattern.replace('f.last@', f"{first[0]}.{last}@")
    elif 'first.l@' in email_pattern:
        email = email_pattern.replace('first.l@', f"{first}.{last[0]}@")
    elif 'flast@' in email_pattern:
        email = email_pattern.replace('flast@', f"{first[0]}{last}@")
    elif 'first@' in email_pattern:
        email = email_pattern.replace('first@', f"{first}@")
    elif 'last@' in email_pattern:
        email = email_pattern.replace('last@', f"{last}@")
    elif 'firstlast@' in email_pattern:
        email = email_pattern.replace('firstlast@', f"{first}{last}@")
    elif 'lastf@' in email_pattern:
        email = email_pattern.replace('lastf@', f"{last}{first[0]}@")
    elif 'firstl@' in email_pattern:
        email = email_pattern.replace('firstl@', f"{first}{last[0]}@")
    elif 'lastfirst@' in email_pattern:
        email = email_pattern.replace('lastfirst@', f"{last}{first}@")

    if v:
        print(f"{loc} #{ln()}: email: {email}")

    return email


# MAIN

def main(emails, team, email_patterns, v=False, test=False):
    if v:
        print(f"\n---\np{loc} #{ln()}: processing {len(emails)} emails:")
        pp.pprint(emails)
        print(f"{loc} #{ln()}: processing team:")
        pp.pprint(team)
        print(f"{loc} #{ln()}: with email patterns: {email_patterns}")

    team_dict = {}

    for email,v in emails.items():
        person_name = v['person'].title()
        src_email = v['src']

        if person_name not in [None, '', 'n/a']:
            if person_name in team:
                team_dict[person_name] = {
                    'email': email,
                    'first': person_name.split(' ')[0],
                    'last': person_name.split(' ')[1],
                    'src': src_email,
                }

    # Add missing team members

    # list_team_remaining = [x for x in team if x not in [name for name,v in team_dict.items()]]

    # for team_remaining in list_team_remaining:
    for team_person,person_src in team.items():
        if team_person not in [name for name,v in team_dict.items()]:
            if v:
                print(f"\n{loc} #{ln()} {team_person=}")
                print(f"{loc} #{ln()} {person_src=}")
            first = team_person.split(' ')[0].title()
            last = team_person.split(' ')[1].title()
            if len(email_patterns) > 0:
                email_pattern = email_patterns[0]
                email = generate_email(email_pattern, first, last, v=v)
                team_dict[team_person.title()] = {
                    'email': email,
                    'first': first,
                    'last': last,
                    'src': f'Email generated. Person from {person_src}',
                    }
            else:
                team_dict[team_person.title()] = {
                    'email': '',
                    'first': first,
                    'last': last,
                    'src': person_src,
                    }

    return team_dict
