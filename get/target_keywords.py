# script name
loc = ">get/target_keywords"

import re
import regex

### MAIN

def main(soup_tuple,target_keywords=[],v=False,test=False):

    soup = soup_tuple.soup
    soup_pretty = soup.prettify()

    url = soup_tuple.url

    if v:
        print(f"\n{loc} Looking for {target_keywords} in {soup_tuple.url}\n")

    # url = soup_tuple.url
    # if url.endswith('/'):
    #     url = url[:-1]

    output = set()

    # # print(f"TEST 1: tk in soup")
    # for tk in target_keywords:
    #     if tk in soup:
    #         # print(f"✅ {loc} {tk} found in soup {url}")
    #         output.add(tk)

    # # print(f"TEST 2: tk in soup_pretty")
    # for tk in target_keywords:
    #     if tk in soup_pretty:
    #         # print(f"✅ {loc} {tk} found in soup_pretty {url}")
    #         output.add(tk)

    # print(f"TEST 3: regex in soup")
    # for tk in target_keywords:
    #     pattern = fr'(?<=https?://)(?:[a-zA-Z0-9-]*\.)?({re.escape(tk)})(?=[/"\s]?|$)'
    #     match = regex.findall(pattern, soup)
    #     if match:
    #         print(f"✅ {loc} {tk} regex found in soup {url}")
    #         output.add(tk)

    # print(f"TEST 4: regex in soup_pretty")
    for tk in target_keywords:
        pattern = fr'(?<=https?://)(?:[a-zA-Z0-9-]*\.)?({re.escape(tk)})(?=[/"\s]?|$)'
        match = regex.findall(pattern, soup_pretty)
        if match:
            print(f"✅ {loc} {tk} regex found in soup_pretty {url}")
            output.add(tk)


    # print(f"TEST 4: regex tk in soup.prety")
    # pattern = fr'https?://[a-zA-Z0-9-]+\.(?:{re.escape(tk)})'

    # # match = re.search(pattern, soup)

    # # if match:
    # #     print(f"✅ {loc} {tk} found in {url}")
    # #     output.append(tk)
    # pattern = fr'https?://[a-zA-Z0-9-]+\.(?:{re.escape(tk)})'
    # # print(f"pattern = {pattern}")
    # match = re.match(pattern, soup)

    # # if tk in soup:
    # if match:
    #     print(f"✅ {loc} {tk} found in {url}")
    #     output.append(tk)
    
    return output



# from typing import List, Tuple
# from bs4 import BeautifulSoup

# def main(soup_tuple: Tuple[BeautifulSoup, str], target_keywords: List[str] = [], v: bool = False, test: bool = False) -> List[str]:
#     soup = soup_tuple[0].prettify()
#     # soup = soup_tuple.soup.prettify()
#     url = soup_tuple[1]

#     if v:
#         print(f"\n{loc} Looking for {target_keywords} in {url}\n")

#     if url.endswith('/'):
#         url = url[:-1]

#     output = []

#     for tk in target_keywords:
#         pattern = fr'https?://[a-zA-Z0-9-]+\.(?:{re.escape(tk)})'
#         match = re.search(pattern, soup)

#         if match:
#             print(f"✅ {loc} {tk} found in {url}")
#             output.append(tk)
#         # else:
#         #     print(f"❌ {loc} {tk} not found in {url}")

#     return output
