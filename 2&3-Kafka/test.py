from datetime import datetime
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from bs4.element import Comment

raw_data = """https://google.com
De Test Partij
<!doctype html>
<html>
    <head>
        <title>Test article</title>
    </head>
    <body>
        <h1>This is a test article</h1>
        This is a test article. It's great. Lorem ipsum is way worse.
        This is the best article ever! More text.
        <div>
            <script>
                let thisIsAScript = true;
            </script>
        </div>
        <style>
            body {
                background: red;
            }
        </style>
        <!-- comment -->
    </body>
</html>
"""

#from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

firstLine = raw_data.index("\n")
secondLine = raw_data.index("\n", firstLine+1)

url = raw_data[:firstLine]
party = raw_data[firstLine+1:secondLine]
raw_html = raw_data[secondLine+1:]
soup = BeautifulSoup(raw_html, 'html.parser')
title = soup.head.title.string
content = text_from_html(soup)
#content = "\n".join(soup.stripped_strings)

print(url)
print(party)
print(title)
print("\n\nContent:\n")
print(content)

doc = {
    'title': title,
    'party': party,
    'url': url,
    'content': content,
    'timestamp': datetime.now(),
    'keyword': "test",
}

es = Elasticsearch()
res = es.index(index="scraped-content", doc_type='page', body=doc)
es.indices.refresh(index="scraped-content")