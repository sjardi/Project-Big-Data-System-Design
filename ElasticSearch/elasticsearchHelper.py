class elasticsearchHelper:
    def __init__(self):
        self.watdfk = 'sd'

    def getFields(self):
        return ['titel', 'url', 'content','partij', 'onderwerp']

    def getIndex(self):
        return 'scraped_content2'

    def getDummyDoc(self):
        doc = {
            'titel': 'Minder vlees eten is goed voor het millieu',
            'url': 'http://www.klimaatbeleid.nl',
            'content': 'filler content met geen inhoud',
            'partij': 'PVDA',
            'onderwerp': 'klimaatbeleid'
        }
        return doc