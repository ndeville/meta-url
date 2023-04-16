# script name
loc = ">get/metadata"

from collections import namedtuple

from inspect import currentframe
def ln():
    cf = currentframe()
    return cf.f_back.f_lineno



### MAIN

def main(soup_tuple,keywords_to_remove=[],keywords_to_keep=[],v=False,test=False):

    meta_fields = [
        'description',
        'title',
        'keywords',
        'h1',
        'site_name',
    ]
    
    metadata = namedtuple('Socials', meta_fields)

    soup = soup_tuple.soup

    if soup != None:

        url = soup_tuple.url
        if url.endswith('/'):
            url = url[:-1]

        metas = [x for x in soup.find_all('meta')]
        if v:
            print(f"\n{loc} #{ln()}: {len(metas)} meta tags found in total:\n")
            for m in metas:
                print(f"{loc} #{ln()}: {m}")
            print()

        tag_types = [
            'keywords',
            'description',
            'title',
            'og:title',
            'og:description',
            'og:site_name',
        ]

        keywords = ''
        description = ''
        og_description = ''

        if soup.title != None:
            page_title = soup.title.text
        else:
            page_title = ''

        title = ''
        og_title = ''
        try:
            h1 = soup.h1.text
            if '\n' in h1:
                h1 = h1.replace('\n',' ')
        except:
            h1 = ''
        if v:
            print(f"\n{loc} #{ln()}: {h1=}\n")
        site_name = ''

        for tag in metas:

            # Name tags

            if 'name' in tag.attrs.keys():

                if tag.attrs['name'].strip().lower() == 'keywords':
                    try:
                        keywords = tag.attrs['content']
                        if v:
                            print (f'{loc} #{ln()}: CONTENT NAME :',tag.attrs['content'])
                    except:
                        continue

                if tag.attrs['name'].strip().lower() == 'description':
                    try:
                        description = tag.attrs['content']
                        if v:
                            print (f'{loc} #{ln()}: CONTENT NAME :',tag.attrs['content'])
                    except:
                        continue

            # Property tags

            if 'property' in tag.attrs.keys():

                if tag.attrs['property'].strip().lower() == 'og:title':
                    og_title = tag.attrs['content']
                    if v:
                        print (f'{loc} #{ln()}: CONTENT PROPERTY :',tag.attrs['content'])

                if tag.attrs['property'].strip().lower() == 'og:site_name':
                    site_name = tag.attrs['content']
                    if v:
                        print (f'{loc} #{ln()}: CONTENT PROPERTY :',tag.attrs['content'])

                if tag.attrs['property'].strip().lower() == 'og:description':
                    og_description = tag.attrs['content']
                    if v:
                        print (f'{loc} #{ln()}: CONTENT PROPERTY :',tag.attrs['content'])

        if v:
            print(f"\nChoosing between og_title and page_title for title:")
            print(f"{loc} #{ln()}: {page_title=}")
            print(f"{loc} #{ln()}: {og_title=}")

        # Select between alternatives

        if page_title > og_title:
            title = page_title
        else:
            title = og_title

        if description > og_description:
            description = description
        else:
            description = og_description

        if v:
            print(f"➤ Selected \"{title}\"\n")

        # Cleaning

        if '\n' in description:
            description = description.replace('\n',' ')
        if '\n' in title:
            title = title.replace('\n',' ')
        if '\n' in h1:
            h1 = h1.replace('\n',' ')
        if '\t' in h1:
            h1 = h1.replace('\t',' ')

        if len(description) > 0:
            description = description.strip()
        if len(title) > 0:
            title = title.strip()
        if len(h1) > 0:
            h1 = h1.strip()
        if len(site_name) > 0:
            site_name = site_name.strip()

        # Creating namedtuple

        if description == '':
            description = None
        metadata.description = description

        if title == '':
            title = None
        metadata.title = title

        if keywords == '':
            keywords = None
        metadata.keywords = keywords

        if h1 == '':
            h1 = None
        metadata.h1 = h1

        if site_name == '':
            site_name = None
        metadata.site_name = site_name


        if v:
            print(f"{loc} #{ln()}: NOTE: returns namedtuple of metadata fields: {','.join(meta_fields)}.\n---\n")

        # return metadata
        return metadata
    
    else:
        return None