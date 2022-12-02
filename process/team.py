# process.team

"""
team: return a namedtuple with first / last / full / email
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

def main(emails, team, url, v=False, test=False):
    if v:
        print(f"\n---\nprocess.emails #{get_linenumber()}: processing {len(emails)} emails")

    team_field_names = [
        'email', 
        'team',
        ]

    team_member = namedtuple('Team', team_field_names)

    team_list_namedtuples = []

    for t in team:
        if v:
            print(f"\nprocess.emails #{get_linenumber()}: processing {email}")
        


        

    if v:
        print(f"\nprocess.emails #{get_linenumber()}: {len(team_list_namedtuples)} emails after processing")

    return team_list_namedtuples
