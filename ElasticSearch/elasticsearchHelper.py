class elasticsearchHelper:
    def __init__(self):
        self.watdfk = 'sd'

    def getSearchFields(self):
        return ['titel', 'url', 'content','partij', 'onderwerp']

    def getIndex(self):
        return 'scraped_content'