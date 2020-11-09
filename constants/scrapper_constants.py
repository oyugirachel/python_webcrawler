"""
This is a list of sites that the scrapper is going to scrapp
"""
class scrapper_constants:
    def __init__(self):
        pass
    
    @property
    def sites_to_scrap(self):
        return [
            'https://amazon.com',
            'https://ebay.com'
        ]