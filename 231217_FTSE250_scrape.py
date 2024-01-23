

from get.soup import fetch_soup as get_soup


links_to_scrape = ['https://en.wikipedia.org/wiki/3i_Infrastructure', 'https://en.wikipedia.org/wiki/4imprint', 'https://en.wikipedia.org/wiki/Aberforth_Smaller_Companies_Trust', 'https://en.wikipedia.org/wiki/Abrdn', 'https://en.wikipedia.org/wiki/Abrdn_Private_Equity_Opportunities_Trust', 'https://en.wikipedia.org/wiki/Alliance_Trust', 'https://en.wikipedia.org/wiki/Allianz_Technology_Trust', 'https://en.wikipedia.org/wiki/AO_World', 'https://en.wikipedia.org/wiki/Apax_Global_Alpha', 'https://en.wikipedia.org/wiki/Ascential', 'https://en.wikipedia.org/wiki/Ashmore_Group', 'https://en.wikipedia.org/wiki/Asia_Dragon_Trust', 'https://en.wikipedia.org/wiki/Assura_plc', 'https://en.wikipedia.org/wiki/Aston_Martin', 'https://en.wikipedia.org/wiki/Auction_Technology_Group', 'https://en.wikipedia.org/wiki/AVI_Global_Trust', 'https://en.wikipedia.org/wiki/Babcock_International', 'https://en.wikipedia.org/wiki/Baillie_Gifford_Japan_Trust', 'https://en.wikipedia.org/wiki/Bakkav%C3%B6r', 'https://en.wikipedia.org/wiki/Balanced_Commercial_Property_Trust', 'https://en.wikipedia.org/wiki/Balfour_Beatty', 'https://en.wikipedia.org/wiki/Baltic_Classifieds', 'https://en.wikipedia.org/wiki/Bankers_Investment_Trust', 'https://en.wikipedia.org/wiki/Bank_of_Georgia', 'https://en.wikipedia.org/wiki/A.G._Barr', 'https://en.wikipedia.org/wiki/BBGI', 'https://en.wikipedia.org/wiki/AJ_Bell', 'https://en.wikipedia.org/wiki/Bellevue_Healthcare_Trust', 'https://en.wikipedia.org/wiki/Bellway', 'https://en.wikipedia.org/wiki/BH_Macro', 'https://en.wikipedia.org/wiki/Big_Yellow_Group', 'https://en.wikipedia.org/wiki/BlackRock_Greater_Europe_Investment_Trust', 'https://en.wikipedia.org/wiki/BlackRock_Smaller_Companies_Trust', 'https://en.wikipedia.org/wiki/BlackRock_Throgmorton_Trust', 'https://en.wikipedia.org/wiki/BlackRock_World_Mining_Trust', 'https://en.wikipedia.org/wiki/Bluefield_Solar_Income_Fund', 'https://en.wikipedia.org/wiki/Bodycote', 'https://en.wikipedia.org/wiki/Breedon_Group', 'https://en.wikipedia.org/wiki/Bridgepoint_Group', 'https://en.wikipedia.org/wiki/British_Land', 'https://en.wikipedia.org/wiki/Britvic', 'https://en.wikipedia.org/wiki/Bytes_Technology_Group', 'https://en.wikipedia.org/wiki/C%26C_Group', 'https://en.wikipedia.org/wiki/Caledonia_Investments', 'https://en.wikipedia.org/wiki/Capital_Gearing_Trust', 'https://en.wikipedia.org/wiki/Carnival_Corporation_%26_plc', 'https://en.wikipedia.org/wiki/Centamin', 'https://en.wikipedia.org/wiki/Chemring_Group', 'https://en.wikipedia.org/wiki/City_of_London_Investment_Trust', 'https://en.wikipedia.org/wiki/Clarkson_plc', 'https://en.wikipedia.org/wiki/Close_Brothers_Group', 'https://en.wikipedia.org/wiki/Coats_Group', 'https://en.wikipedia.org/wiki/Computacenter', 'https://en.wikipedia.org/wiki/Cranswick_plc', 'https://en.wikipedia.org/wiki/Crest_Nicholson', 'https://en.wikipedia.org/wiki/Currys_plc', 'https://en.wikipedia.org/wiki/Darktrace', 'https://en.wikipedia.org/wiki/Derwent_London', 'https://en.wikipedia.org/wiki/Direct_Line_Group', 'https://en.wikipedia.org/wiki/DiscoverIE_Group', 'https://en.wikipedia.org/wiki/Diversified_Energy', 'https://en.wikipedia.org/wiki/Domino%27s_Pizza_Group', 'https://en.wikipedia.org/wiki/Dowlais_Group', 'https://en.wikipedia.org/wiki/Drax_Group', 'https://en.wikipedia.org/wiki/Dr._Martens', 'https://en.wikipedia.org/wiki/Dunelm_Group', 'https://en.wikipedia.org/wiki/EasyJet', 'https://en.wikipedia.org/wiki/Edinburgh_Investment_Trust', 'https://en.wikipedia.org/wiki/Edinburgh_Worldwide_Investment_Trust', 'https://en.wikipedia.org/wiki/Elementis', 'https://en.wikipedia.org/wiki/Empiric_Student_Property', 'https://en.wikipedia.org/wiki/Energean', 'https://en.wikipedia.org/wiki/Essentra', 'https://en.wikipedia.org/wiki/European_Opportunities_Trust', 'https://en.wikipedia.org/wiki/European_Smaller_Companies_Trust', 'https://en.wikipedia.org/wiki/FDM_Group', 'https://en.wikipedia.org/wiki/Ferrexpo', 'https://en.wikipedia.org/wiki/Fidelity_China_Special_Situations', 'https://en.wikipedia.org/wiki/Fidelity_Emerging_Markets', 'https://en.wikipedia.org/wiki/Fidelity_European_Trust', 'https://en.wikipedia.org/wiki/Fidelity_Special_Values', 'https://en.wikipedia.org/wiki/Finsbury_Growth_%26_Income_Trust', 'https://en.wikipedia.org/wiki/FirstGroup', 'https://en.wikipedia.org/wiki/Foresight_Group', 'https://en.wikipedia.org/wiki/Foresight_Solar_Fund', 'https://en.wikipedia.org/wiki/Future_plc', 'https://en.wikipedia.org/wiki/Games_Workshop', 'https://en.wikipedia.org/wiki/GCP_Infrastructure_Investments', 'https://en.wikipedia.org/wiki/Genuit', 'https://en.wikipedia.org/wiki/Genus_plc', 'https://en.wikipedia.org/wiki/Global_Smaller_Companies_Trust', 'https://en.wikipedia.org/wiki/Grafton_Group', 'https://en.wikipedia.org/wiki/Grainger_plc', 'https://en.wikipedia.org/wiki/Great_Portland_Estates', 'https://en.wikipedia.org/wiki/Greencoat_UK_Wind', 'https://en.wikipedia.org/wiki/Greggs', 'https://en.wikipedia.org/wiki/Hammerson', 'https://en.wikipedia.org/wiki/Harbour_Energy', 'https://en.wikipedia.org/wiki/HarbourVest_Global_Private_Equity', 'https://en.wikipedia.org/wiki/Hargreaves_Lansdown', 'https://en.wikipedia.org/wiki/Hays_plc', 'https://en.wikipedia.org/wiki/Helios_Towers', 'https://en.wikipedia.org/wiki/Henderson_Smaller_Companies_Investment_Trust', 'https://en.wikipedia.org/wiki/Herald_Investment_Trust', 'https://en.wikipedia.org/wiki/Hg_Capital_Trust', 'https://en.wikipedia.org/wiki/HICL_Infrastructure_Company', 'https://en.wikipedia.org/wiki/Hill_%26_Smith', 'https://en.wikipedia.org/wiki/Hilton_Food_Group', 'https://en.wikipedia.org/wiki/Hipgnosis_Songs_Fund', 'https://en.wikipedia.org/wiki/Hiscox', 'https://en.wikipedia.org/wiki/Hochschild_Mining', 'https://en.wikipedia.org/wiki/Hunting_plc', 'https://en.wikipedia.org/wiki/Ibstock_plc', 'https://en.wikipedia.org/wiki/ICG_Enterprise_Trust', 'https://en.wikipedia.org/wiki/IG_Group', 'https://en.wikipedia.org/wiki/Impax_Environmental_Markets', 'https://en.wikipedia.org/wiki/Inchcape_plc', 'https://en.wikipedia.org/wiki/Indivior', 'https://en.wikipedia.org/wiki/IntegraFin', 'https://en.wikipedia.org/wiki/International_Distributions_Services', 'https://en.wikipedia.org/wiki/International_Public_Partnerships', 'https://en.wikipedia.org/wiki/Investec', 'https://en.wikipedia.org/wiki/IP_Group', 'https://en.wikipedia.org/wiki/Ithaca_Energy', 'https://en.wikipedia.org/wiki/ITV_plc', 'https://en.wikipedia.org/wiki/IWG_plc', 'https://en.wikipedia.org/wiki/JLEN_Environmental_Assets_Group', 'https://en.wikipedia.org/wiki/Johnson_Matthey', 'https://en.wikipedia.org/wiki/JPMorgan_American_Investment_Trust', 'https://en.wikipedia.org/wiki/JPMorgan_Emerging_Markets_Investment_Trust', 'https://en.wikipedia.org/wiki/JPMorgan_European_Discovery', 'https://en.wikipedia.org/wiki/JPMorgan_Global_Growth_%26_Income', 'https://en.wikipedia.org/wiki/JPMorgan_Indian_Investment_Trust', 'https://en.wikipedia.org/wiki/JPMorgan_Japanese_Investment_Trust', 'https://en.wikipedia.org/wiki/JTC_plc', 'https://en.wikipedia.org/wiki/Jupiter_Fund_Management', 'https://en.wikipedia.org/wiki/Just_Group_plc', 'https://en.wikipedia.org/wiki/Kainos', 'https://en.wikipedia.org/wiki/Keller_Group', 'https://en.wikipedia.org/wiki/Lancashire_Holdings', 'https://en.wikipedia.org/wiki/Law_Debenture', 'https://en.wikipedia.org/wiki/LondonMetric_Property', 'https://en.wikipedia.org/wiki/LXi_REIT', 'https://en.wikipedia.org/wiki/Man_Group', 'https://en.wikipedia.org/wiki/Marshalls_plc', 'https://en.wikipedia.org/wiki/ME_Group', 'https://en.wikipedia.org/wiki/Mercantile_Investment_Trust', 'https://en.wikipedia.org/wiki/Merchants_Trust', 'https://en.wikipedia.org/wiki/Mitchells_%26_Butlers', 'https://en.wikipedia.org/wiki/Mitie', 'https://en.wikipedia.org/wiki/Mobico_Group', 'https://en.wikipedia.org/wiki/Moneysupermarket.com', 'https://en.wikipedia.org/wiki/Monks_Investment_Trust', 'https://en.wikipedia.org/wiki/Moonpig', 'https://en.wikipedia.org/wiki/Morgan_Advanced_Materials', 'https://en.wikipedia.org/wiki/Morgan_Sindall', 'https://en.wikipedia.org/wiki/Murray_Income_Trust', 'https://en.wikipedia.org/wiki/Murray_International_Trust', 'https://en.wikipedia.org/wiki/NB_Private_Equity_Partners', 'https://en.wikipedia.org/wiki/Network_International', 'https://en.wikipedia.org/wiki/NextEnergy_Solar_Fund', 'https://en.wikipedia.org/wiki/Ninety_One_Limited', 'https://en.wikipedia.org/wiki/North_Atlantic_Smaller_Companies_Investment_Trust', 'https://en.wikipedia.org/wiki/Octopus_Renewables_Infrastructure_Trust', 'https://en.wikipedia.org/wiki/Kent_Reliance', 'https://en.wikipedia.org/wiki/Oxford_Instruments', 'https://en.wikipedia.org/wiki/Pacific_Horizon_Investment_Trust', 'https://en.wikipedia.org/wiki/PageGroup', 'https://en.wikipedia.org/wiki/Pantheon_International', 'https://en.wikipedia.org/wiki/Paragon_Banking_Group', 'https://en.wikipedia.org/wiki/Pennon_Group', 'https://en.wikipedia.org/wiki/Persimmon_plc', 'https://en.wikipedia.org/wiki/Personal_Assets_Trust', 'https://en.wikipedia.org/wiki/Petershill_Partners', 'https://en.wikipedia.org/wiki/Pets_at_Home', 'https://en.wikipedia.org/wiki/Playtech', 'https://en.wikipedia.org/wiki/Plus500', 'https://en.wikipedia.org/wiki/Polar_Capital_Technology_Trust', 'https://en.wikipedia.org/wiki/PPHE_Hotel_Group', 'https://en.wikipedia.org/wiki/Premier_Foods', 'https://en.wikipedia.org/wiki/Primary_Health_Properties', 'https://en.wikipedia.org/wiki/PureTech_Health', 'https://en.wikipedia.org/wiki/PZ_Cussons', 'https://en.wikipedia.org/wiki/Qinetiq', 'https://en.wikipedia.org/wiki/Quilter_plc', 'https://en.wikipedia.org/wiki/Rathbones', 'https://en.wikipedia.org/wiki/Redde_Northgate', 'https://en.wikipedia.org/wiki/Redrow_plc', 'https://en.wikipedia.org/wiki/Renishaw_plc', 'https://en.wikipedia.org/wiki/RHI_Magnesita', 'https://en.wikipedia.org/wiki/RIT_Capital_Partners', 'https://en.wikipedia.org/wiki/Rotork', 'https://en.wikipedia.org/wiki/Ruffer_Investment_Company', 'https://en.wikipedia.org/wiki/Safestore', 'https://en.wikipedia.org/wiki/Savills', 'https://en.wikipedia.org/wiki/Schroder_AsiaPacific_Fund', 'https://en.wikipedia.org/wiki/Schroder_Oriental_Income_Fund', 'https://en.wikipedia.org/wiki/Scottish_American_Investment_Company', 'https://en.wikipedia.org/wiki/SDCL_Energy_Efficiency_Income_Trust', 'https://en.wikipedia.org/wiki/Senior_plc', 'https://en.wikipedia.org/wiki/Sequoia_Economic_Infrastructure_Income_Fund', 'https://en.wikipedia.org/wiki/Serco', 'https://en.wikipedia.org/wiki/Shaftesbury_Capital', 'https://en.wikipedia.org/wiki/Sirius_Real_Estate', 'https://en.wikipedia.org/wiki/Smithson_Investment_Trust', 'https://en.wikipedia.org/wiki/Softcat', 'https://en.wikipedia.org/wiki/Spectris', 'https://en.wikipedia.org/wiki/Spire_Healthcare', 'https://en.wikipedia.org/wiki/Spirent', 'https://en.wikipedia.org/wiki/SSP_Group', 'https://en.wikipedia.org/wiki/SThree', 'https://en.wikipedia.org/wiki/Supermarket_Income_REIT', 'https://en.wikipedia.org/wiki/Syncona', 'https://en.wikipedia.org/wiki/Target_Healthcare_REIT', 'https://en.wikipedia.org/wiki/Tate_%26_Lyle', 'https://en.wikipedia.org/wiki/TBC_Bank', 'https://en.wikipedia.org/wiki/Telecom_Plus', 'https://en.wikipedia.org/wiki/Temple_Bar_Investment_Trust', 'https://en.wikipedia.org/wiki/Templeton_Emerging_Markets_Investment_Trust', 'https://en.wikipedia.org/wiki/The_Renewables_Infrastructure_Group', 'https://en.wikipedia.org/wiki/TI_Fluid_Systems', 'https://en.wikipedia.org/wiki/TP_ICAP', 'https://en.wikipedia.org/wiki/Trainline', 'https://en.wikipedia.org/wiki/Travis_Perkins', 'https://en.wikipedia.org/wiki/Tritax_Big_Box_REIT', 'https://en.wikipedia.org/wiki/Tritax_EuroBox', 'https://en.wikipedia.org/wiki/TR_Property_Investment_Trust', 'https://en.wikipedia.org/wiki/Trustpilot', 'https://en.wikipedia.org/wiki/TUI_Group', 'https://en.wikipedia.org/wiki/Tullow_Oil', 'https://en.wikipedia.org/wiki/Twentyfour_Income_Fund', 'https://en.wikipedia.org/wiki/Tyman', 'https://en.wikipedia.org/wiki/UK_Commercial_Property_REIT', 'https://en.wikipedia.org/wiki/Urban_Logistics_REIT', 'https://en.wikipedia.org/wiki/Vesuvius_plc', 'https://en.wikipedia.org/wiki/Victrex', 'https://en.wikipedia.org/wiki/Vietnam_Enterprise_Investments', 'https://en.wikipedia.org/wiki/VinaCapital_Vietnam_Opportunity_Fund', 'https://en.wikipedia.org/wiki/Virgin_Money_UK_plc', 'https://en.wikipedia.org/wiki/Vistry_Group', 'https://en.wikipedia.org/wiki/Volution_Group', 'https://en.wikipedia.org/wiki/W._A._G._Payment_Solutions', 'https://en.wikipedia.org/wiki/Watches_of_Switzerland', 'https://en.wikipedia.org/wiki/Wetherspoons', 'https://en.wikipedia.org/wiki/WHSmith', 'https://en.wikipedia.org/wiki/Witan_Investment_Trust', 'https://en.wikipedia.org/wiki/Wizz_Air', 'https://en.wikipedia.org/wiki/John_Wood_Group', 'https://en.wikipedia.org/wiki/Workspace_Group', 'https://en.wikipedia.org/wiki/Worldwide_Healthcare_Trust']


import webbrowser
import time

count = 0

for link in links_to_scrape:

    # open link with Chrome

    count += 1
    
    print(f"#{count} opening: {link}\n\n")

    webbrowser.get('chrome').open_new_tab(link)

    time.sleep(2)




# link = 'https://en.wikipedia.org/wiki/3i_Infrastructure'

# soup = get_soup(link).soup

# print(f"\n\nSOUP: {soup.text}\n\n")



# # from bs4 import BeautifulSoup

# # def extract_url(soup):

# #     # Find all anchor tags
# #     anchors = soup.find_all('a', href=True)
    
# #     # Extract URLs
# #     urls = [a['href'] for a in anchors if a['href'].startswith('http')]
    
# #     # Return the first URL found or None if no URL is found
# #     return urls[0] if urls else None



# from bs4 import BeautifulSoup

# def extract_url_from_infobox(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     # Find the first element with class 'infobox vcard'
#     infobox = soup.find('table', {'class': 'infobox vcard'})
    
#     # Extract URLs from the infobox
#     if infobox:
#         urls = [a['href'] for a in infobox.find_all('a', href=True) if a['href'].startswith('http')]
#         return urls[0] if urls else None
#     else:
#         return None







# url = extract_url_from_infobox(soup)

# print(f"\n\nURL: {url}\n\n")








