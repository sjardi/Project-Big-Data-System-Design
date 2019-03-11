from datetime import datetime
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

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
    </body>
</html>
"""

firstLine = raw_data.index("\n")
secondLine = raw_data.index("\n", firstLine+1)

url = raw_data[:firstLine]
party = raw_data[firstLine+1:secondLine]
raw_html = raw_data[secondLine+1:]
soup = BeautifulSoup(raw_html, 'html.parser')
title = soup.head.title.string
content = "\n".join(soup.stripped_strings)

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