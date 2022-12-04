import sys
sys.path.append(f"/Users/nic/Python/indeXee")

import grist_BB
import tldextract

count_added_to_grist = 0

dict_grist_domains = {x.id: x.domain for x in grist_BB.VCs.fetch_table('Master')}

# Supporting functions

# get script name
import sys
def get_loc():
    return f"{sys.argv[0][18:-3]}"
loc = get_loc()

def find_key(input_dict, value):
    for k, v in input_dict.items():
        if v == value:
            return k

def domain_from_url(url):
    o = tldextract.extract(url)
    domain = f"{o.domain}.{o.suffix}".lower()
    if 'www.' in domain:
        domain = domain.replace('www.','')
    return domain

def domain_name_from_url(url):
    o = tldextract.extract(url)
    domain_name = o.domain.lower()
    if 'www.' in domain_name:
        domain_name = domain_name.replace('www.','')
    return domain_name


# Main


def vcs_team(url, list_people,v=False,test=False):
    global count_added_to_grist

    domain_name = domain_from_url(url)
    if v:
        print(f"\n{domain_name=}")
    domain_name_key = find_key(dict_grist_domains, domain_name)
    if v:
        print(f"{domain_name_key=}\n")

    if len(list_people) > 0:
        print(f"\nAdding to Grist...")
        existing_people = [f"{x.first.lower()} {x.last.lower()}" for x in grist_BB.VCs.fetch_table('Team') if dict_grist_domains[int(x.domain)] == domain_name]
        if v and len(existing_people) > 0:
            print(f"\n{existing_people=}\n")
        if v and len(existing_people) == 0:
            print(f"\nNO existing people found for {domain_name}\n")

        for person in list_people:

            if person.lower() not in existing_people: # remove duplicates

                first = person.split(' ')[0]
                if v: 
                    print(f"\n{first=}")
                last = person.split(' ')[1:]
                last = ' '.join(last)
                if v: 
                    print(f"{last=}")
                
                grist_BB.VCs.add_records('Team', [
                                                {   'first': first.strip(),
                                                    'last': last.strip(),
                                                    'domain': domain_name_key,
                                                    'src_page_url': url,
                                                    }
                                            ])

                count_added_to_grist += 1
            else:
                print(f"{person} already in Grist")

        return print(f"\nADDED {count_added_to_grist} records to Grist.\n")


    else:
        grist_BB.VCs.add_records('Team', [
                                            {   'domain': domain_name_key,
                                                'src_page_url': url,
                                                }
                                            ])
        return print(f"No people found on website")