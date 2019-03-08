from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

from mathematicians import simple_get
"""raw_html = simple_get('https://realpython.com/blog/')
print(len(raw_html))


raw_html = simple_get('http://www.fabpedigree.com/james/mathmen.htm')
html = BeautifulSoup(raw_html, 'html.parser')
for i, li in enumerate(html.select('li')):
    print(i, li)"""

#print(soup.prettify())
# for link in soup.find_all('a'):
#     links = link.get('href')
#     if links is not None:
#         if "nieuw" in links:
#             raw_deep = simple_get(links)
#             soup_deep = BeautifulSoup(raw_deep, 'html.parser')
#             for deep_link in soup.find_all('a'):
#                 deep_links = link.get('href')
#                 print(deep_links)
#             # deeplinks = link.get('href')
#             # print(deeplinks)

def recursiveLinks(url_link,query):
    raw_html = simple_get(url_link)
    soup = BeautifulSoup(raw_html, 'html.parser')

    for link in soup.find_all('a'):
        url = link.get('href')
        if url is not None:
            if query is not None:
                if query in url:
                    if url not in alreadyQueried:
                        alreadyQueried.append(url)
                        print(alreadyQueried)
                        recursiveLinks(url, query)

def findAllHrefOnPage(url):
    raw_html = simple_get(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    for link in soup.find_all('a'):
        urls_on_page = link.get('href')
        if(url_on_page is not None) and (urls_on_page in url) :
            
            file_obj = open("outputs/test_links.txt", "r")
            loglist = file_obj.readlines()
            file_obj.close()
            found = False
            for line in loglist:
                if url_on_page in line:
                    print (url_on_page + "Found in file, skipping.")
                    found = True

                if not found:
                    print(url_on_page + "not found, adding to file.")
                    logfile = open("outputs/test_links.txt", 'a')
                    logfile.write( url_on_page + "\n" )
                    logfile.close()
                    found = False
           
#findAllHrefOnPage(pvda_url)
        
#recursiveLinks(pvda_url, "nieuws")
#raw_html = simple_get(pvda_url)
#soup = BeautifulSoup(raw_html, 'html.parser')
#print(soup)
#file_obj = open("outputs/text", "w")
#file_obj.write(str(soup))

filepath = 'Input_Links/input_link.txt'
with open(filepath) as fp:
    content = fp.readlines()
All_website_urls = [x.strip() for x in content]

for website in All_website_urls:
    findAllHrefOnPage(website)