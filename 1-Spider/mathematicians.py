from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pathlib import Path
import os

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



#Beautifull soup 4 
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
    full_url = "https://" + url
    raw_html = simple_get(full_url)
    soup = BeautifulSoup(raw_html, 'html.parser')
    All_Urls_On_Website_File = "outputs/" + url + ".txt"
    for link in soup.find_all('a'):
        url_on_page = link.get('href')
        if(url_on_page is not None) and (url in url_on_page ):
            writeToFile(url_on_page, All_Urls_On_Website_File)

def writeToFile(url, file):
    if os.path.exists(file) and os.path.getsize(file) > 0:
        print("file exists and not empty")
        """openFile = open(file, 'r')
        allUrlsInFile = openFile.readlines()"""
        if url in open(file).read():
            print("Url Already In File, Skipping")
        else:
            print("URL NOT found, adding " +  url)
            logfile = open(file, 'a')
            logfile.write( url + "\n" )
            logfile.close()
    else:
        print("file not found or empty. Writing first line or Creating file: " + file)
        logfile = open(file, 'w')
        logfile.write( url + "\n" )
        logfile.close()

filepath = 'Input_Links/input_link.txt'
with open(filepath) as fp:
    content = fp.readlines()
All_website_urls = [x.strip() for x in content]

for website in All_website_urls:
    print("bezig met website " + website)
    
    findAllHrefOnPage(website)

            
"""try:
    file_obj = open(All_Urls_On_Website_File, "r")
    loglist = file_obj.readlines()
    file_obj.close()
    found = False
    for line in loglist:
        if url_on_page in line:
            print (url_on_page + "Found in file, skipping.")
            found = True

        if not found:
            print(url_on_page + "not found, adding to file.")
            logfile = open(All_Urls_On_Website_File, 'a')
            logfile.write( url_on_page + "\n" )
            logfile.close()
            found = False
except:
    print("error")
    file_obj = open(All_Urls_On_Website_File, "w")
    loglist = file_obj
    print(url_on_page + "not found, adding to file.")
    logfile.write( url_on_page + "\n" )
    logfile.close()
    found = False"""
            
           
#findAllHrefOnPage(pvda_url)
        
#recursiveLinks(pvda_url, "nieuws")
#raw_html = simple_get(pvda_url)
#soup = BeautifulSoup(raw_html, 'html.parser')
#print(soup)
#file_obj = open("outputs/text", "w")
#file_obj.write(str(soup))

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