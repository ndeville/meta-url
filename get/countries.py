


# script name
loc = ">get/countries"


# list_countries_ref = list(my_utils.dict_country)
# if v:
#     for c in sorted(list_countries_ref):
#         print(repr(c))


Country = [
('US', 'United States'),
('AF', 'Afghanistan'),
('AL', 'Albania'),
('DZ', 'Algeria'),
('AS', 'American Samoa'),
('AD', 'Andorra'),
('AO', 'Angola'),
('AI', 'Anguilla'),
('AQ', 'Antarctica'),
('AG', 'Antigua And Barbuda'),
('AR', 'Argentina'),
('AM', 'Armenia'),
('AW', 'Aruba'),
('AU', 'Australia'),
('AT', 'Austria'),
('AZ', 'Azerbaijan'),
('BS', 'Bahamas'),
('BH', 'Bahrain'),
('BD', 'Bangladesh'),
('BB', 'Barbados'),
('BY', 'Belarus'),
('BE', 'Belgium'),
('BZ', 'Belize'),
('BJ', 'Benin'),
('BM', 'Bermuda'),
('BT', 'Bhutan'),
('BO', 'Bolivia'),
('BA', 'Bosnia And Herzegowina'),
('BW', 'Botswana'),
('BV', 'Bouvet Island'),
('BR', 'Brazil'),
('BN', 'Brunei Darussalam'),
('BG', 'Bulgaria'),
('BF', 'Burkina Faso'),
('BI', 'Burundi'),
('KH', 'Cambodia'),
('CM', 'Cameroon'),
('CA', 'Canada'),
('CV', 'Cape Verde'),
('KY', 'Cayman Islands'),
('CF', 'Central African Rep'),
('TD', 'Chad'),
('CL', 'Chile'),
('CN', 'China'),
('CX', 'Christmas Island'),
('CC', 'Cocos Islands'),
('CO', 'Colombia'),
('KM', 'Comoros'),
('CG', 'Congo'),
('CK', 'Cook Islands'),
('CR', 'Costa Rica'),
('CI', 'Cote D`ivoire'),
('HR', 'Croatia'),
('CU', 'Cuba'),
('CY', 'Cyprus'),
('CZ', 'Czech Republic'),
('DK', 'Denmark'),
('DJ', 'Djibouti'),
('DM', 'Dominica'),
('DO', 'Dominican Republic'),
('TP', 'East Timor'),
('EC', 'Ecuador'),
('EG', 'Egypt'),
('SV', 'El Salvador'),
('GQ', 'Equatorial Guinea'),
('ER', 'Eritrea'),
('EE', 'Estonia'),
('ET', 'Ethiopia'),
('FK', 'Falkland Islands (Malvinas)'),
('FO', 'Faroe Islands'),
('FJ', 'Fiji'),
('FI', 'Finland'),
('FR', 'France'),
('GF', 'French Guiana'),
('PF', 'French Polynesia'),
('TF', 'French S. Territories'),
('GA', 'Gabon'),
('GM', 'Gambia'),
('GE', 'Georgia'),
('DE', 'Germany'),
('GH', 'Ghana'),
('GI', 'Gibraltar'),
('GR', 'Greece'),
('GL', 'Greenland'),
('GD', 'Grenada'),
('GP', 'Guadeloupe'),
('GU', 'Guam'),
('GT', 'Guatemala'),
('GN', 'Guinea'),
('GW', 'Guinea-bissau'),
('GY', 'Guyana'),
('HT', 'Haiti'),
('HN', 'Honduras'),
('HK', 'Hong Kong'),
('HU', 'Hungary'),
('IS', 'Iceland'),
('IN', 'India'),
('ID', 'Indonesia'),
('IR', 'Iran'),
('IQ', 'Iraq'),
('IE', 'Ireland'),
('IL', 'Israel'),
('IT', 'Italy'),
('JM', 'Jamaica'),
('JP', 'Japan'),
('JO', 'Jordan'),
('KZ', 'Kazakhstan'),
('KE', 'Kenya'),
('KI', 'Kiribati'),
('KP', 'Korea (North)'),
('KR', 'Korea (South)'),
('KW', 'Kuwait'),
('KG', 'Kyrgyzstan'),
('LA', 'Laos'),
('LV', 'Latvia'),
('LB', 'Lebanon'),
('LS', 'Lesotho'),
('LR', 'Liberia'),
('LY', 'Libya'),
('LI', 'Liechtenstein'),
('LT', 'Lithuania'),
('LU', 'Luxembourg'),
('MO', 'Macau'),
('MK', 'Macedonia'),
('MG', 'Madagascar'),
('MW', 'Malawi'),
('MY', 'Malaysia'),
('MV', 'Maldives'),
('ML', 'Mali'),
('MT', 'Malta'),
('MH', 'Marshall Islands'),
('MQ', 'Martinique'),
('MR', 'Mauritania'),
('MU', 'Mauritius'),
('YT', 'Mayotte'),
('MX', 'Mexico'),
('FM', 'Micronesia'),
('MD', 'Moldova'),
('MC', 'Monaco'),
('MN', 'Mongolia'),
('MS', 'Montserrat'),
('MA', 'Morocco'),
('MZ', 'Mozambique'),
('MM', 'Myanmar'),
('NA', 'Namibia'),
('NR', 'Nauru'),
('NP', 'Nepal'),
('NL', 'Netherlands'),
('AN', 'Netherlands Antilles'),
('NC', 'New Caledonia'),
('NZ', 'New Zealand'),
('NI', 'Nicaragua'),
('NE', 'Niger'),
('NG', 'Nigeria'),
('NU', 'Niue'),
('NF', 'Norfolk Island'),
('MP', 'Northern Mariana Islands'),
('NO', 'Norway'),
('OM', 'Oman'),
('PK', 'Pakistan'),
('PW', 'Palau'),
('PA', 'Panama'),
('PG', 'Papua New Guinea'),
('PY', 'Paraguay'),
('PE', 'Peru'),
('PH', 'Philippines'),
('PN', 'Pitcairn'),
('PL', 'Poland'),
('PT', 'Portugal'),
('PR', 'Puerto Rico'),
('QA', 'Qatar'),
('RE', 'Reunion'),
('RO', 'Romania'),
('RU', 'Russian Federation'),
('RW', 'Rwanda'),
('KN', 'Saint Kitts And Nevis'),
('LC', 'Saint Lucia'),
('VC', 'St Vincent/Grenadines'),
('WS', 'Samoa'),
('SM', 'San Marino'),
('ST', 'Sao Tome'),
('SA', 'Saudi Arabia'),
('SN', 'Senegal'),
('SC', 'Seychelles'),
('SL', 'Sierra Leone'),
('SG', 'Singapore'),
('SK', 'Slovakia'),
('SI', 'Slovenia'),
('SB', 'Solomon Islands'),
('SO', 'Somalia'),
('ZA', 'South Africa'),
('ES', 'Spain'),
('LK', 'Sri Lanka'),
('SH', 'St. Helena'),
('PM', 'St.Pierre'),
('SD', 'Sudan'),
('SR', 'Suriname'),
('SZ', 'Swaziland'),
('SE', 'Sweden'),
('CH', 'Switzerland'),
('SY', 'Syrian Arab Republic'),
('TW', 'Taiwan'),
('TJ', 'Tajikistan'),
('TZ', 'Tanzania'),
('TH', 'Thailand'),
('TG', 'Togo'),
('TK', 'Tokelau'),
('TO', 'Tonga'),
('TT', 'Trinidad And Tobago'),
('TN', 'Tunisia'),
('TR', 'Turkey'),
('TM', 'Turkmenistan'),
('TV', 'Tuvalu'),
('UG', 'Uganda'),
('UA', 'Ukraine'),
('AE', 'United Arab Emirates'),
('UK', 'United Kingdom'),
('UY', 'Uruguay'),
('UZ', 'Uzbekistan'),
('VU', 'Vanuatu'),
('VA', 'Vatican City State'),
('VE', 'Venezuela'),
('VN', 'Viet Nam'),
('VG', 'Virgin Islands (British)'),
('VI', 'Virgin Islands (U.S.)'),
('EH', 'Western Sahara'),
('YE', 'Yemen'),
('YU', 'Yugoslavia'),
('ZR', 'Zaire'),
('ZM', 'Zambia'),
('ZW', 'Zimbabwe')
]


def main(soup_tuple,v=False,test=False):

    soup = soup_tuple.soup
    url = soup_tuple.url
    if url.endswith('/'):
        url = url[:-1]

    text = soup.get_text()

    for pair in Country:
        if (pair[1] in text):
            
            print(pair[1])


    return None



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