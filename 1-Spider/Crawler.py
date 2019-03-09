from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pathlib import Path
import io
import os.path


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


# Beautifull soup 4

def findAllHrefOnPage(url, baseUrl=None):
    if (baseUrl == None):
        baseUrl = url
    try:
        full_url = "https://" + url
        raw_html = simple_get(full_url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        All_Urls_On_Website_File = "outputs/" + baseUrl + ".txt"
    except:
        print("ERROR in findAllHrefOnPage")
    try:
        for link in soup.find_all('a'):
            url_on_page = link.get('href')
            if (url_on_page is not None) and (baseUrl in url_on_page):
                findAllHrefOnPage(url_on_page, baseUrl)
                writeToFile(url_on_page, All_Urls_On_Website_File, False)
    except:
        print("kapot bij for in find all href on page")


def writeToFile(content, file, isHtml):
    try:
        # and os.path.getsize(file) > 0
        if os.path.isfile(file.strip()):
            print("FILE TO OPEN IS " + file)
            if (isHtml is not True) and (content in open(file).read()):
                print(" Url Already In File, Skipping")
            elif isHtml and (content in open(file).read()):
                print("Content already exists in file")
            else:
                try:
                    if isHtml is not True:
                        print("URL not found, Adding url: " + content)
                    else:
                        print("Content NOT found, adding CONTENT or URL")
                    logfile = open(file, 'a', encoding='utf-')
                    logfile.write(content + "\n")
                    logfile.close()
                except:
                    print("error in 2e else van WriteToFile")
        else:
            print("bestaat niet of leeg")
            try:
                if not os.path.exists(file):
                    print("file not found or empty. Writing first line or Creating file: " + file)
                    logfile = open(file, 'w', encoding='utf-8')
                    logfile.write(content + "\n")
                    logfile.close()
            except Exception as e:
                print(e)
                print("error in 1e else van WriteToFile")
    except Exception as e:
        print("Write To File Exception: " + e)


#Start of application, gets all websites to scrape and put their internal linking in file
def scrapeAllUrlFromWebsite(file_location):
    with open(file_location) as fp:
        content = fp.readlines()
    All_website_urls = [x.strip() for x in content]

    for website in All_website_urls:
        print("bezig met website " + website)
        try:
            findAllHrefOnPage(website)
        except:
            print("aanroepen van find all href on page error")

scrapeAllUrlFromWebsite('Input_Links/input_link.txt')

# Naar HTML file
def urlToHtml(url):
    try:
        raw_html = simple_get(url)
        soup = BeautifulSoup(raw_html, 'html.parser')
    except:
        print("IS KAPOT GEGAAN BIJ GET REQUEST OF BEAUTIFULSOUP IN URLTOHTML")
    try:
        fixedUrl = url.replace('https://', '').replace('/', '_')
        file_name = "Html_Output/" + fixedUrl + ".html.txt"
        pretty_soup = soup.prettify()
        try:
            writeToFile(pretty_soup, file_name, True)
        except:
            print("writeTofile Failed")
    except:
        print("Error bij urlToHtml aan het einde")

    # AllFilesWithUrlPerWebsite

def AllLinkInFileToHtmlFile(links_source):
    for filename in os.listdir(links_source):
        filename = links_source + filename
        if os.path.exists(filename.strip()):
            print("exists")
            with open(filename, "r") as f:
                for line in f.readlines():
                    if not line:
                        break
                    urlToHtml(line.strip())
        else:
            print("file not exist.")
#AllLinkInFileToHtmlFile("outputs/")


