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

#Werkt nog niet
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

def writeToFile(content, file):
    if os.path.exists(file) and os.path.getsize(file) > 0:
        if content in open(file).read():
            print("Content / Url Already In File, Skipping")
            #Niet zeker bout dis close
            file.close()
        else:
            print("Content / URL NOT found, adding " +  content)
            logfile = open(file, 'a')
            logfile.write( content + "\n" )
            logfile.close()
    else:
        print("file not found or empty. Writing first line or Creating file: " + file)
        logfile = open(file, 'w')
        logfile.write( content + "\n" )
        logfile.close()

filepath = 'Input_Links/input_link.txt'
with open(filepath) as fp:
    content = fp.readlines()
All_website_urls = [x.strip() for x in content]

for website in All_website_urls:
    print("bezig met website " + website)
    
   # findAllHrefOnPage(website)


# Naar HTML file
def urlToHtml(url):
    try:
        raw_html = simple_get(url)
        soup = BeautifulSoup(raw_html, 'html.parser')
    except:
        print("IS KAPOT GEGAAN BIJ GET REQUEST OF BEAUTIFULSOUP IN URLTOHTML")
    try:
        file_name = "Html_Output/" + url + ".html"
        writeToFile( soup.prettify() , file_name)
    except:
        print("kapot")    

DierenFile = open ("outputs/utrecht.partijvoordedieren.nl.txt", "r")
while True:
    line = DierenFile.readline()
    if not line : 
        break
    urlToHtml(line.strip())