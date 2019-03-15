from datetime import datetime

class elasticsearchHelper:
    def __init__(self):
        self.watdfk = 'sd'

    def getFields(self):
        return ['title','party','url','content','timestamp']

    def getIndex(self):
        return 'scraped_content2'

    def getDummyDoc(self):
        doc = {
            'title': 'Minder vlees eten is goed voor het millieu',
            'url': 'http://www.klimaatbeleid.nl',
            'content': 'filler content met geen inhoud',
            'party': 'PVDA',
            'timestamp': datetime.now()
        }
        return doc