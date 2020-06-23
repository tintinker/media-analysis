from bs4 import BeautifulSoup
import requests

class NewsParser(object):
    def GoogleNewsRequest(search_term):
        return 'https://news.google.com/search?q='+search_term
    
    def GoogleNewsParse(soup):
        headlines = soup.findAll('a', {'class': 'DY5T1d'})
        return [link.encode_contents().decode("utf-8") for link in headlines]
        

    def __init__(self, url_gen=GoogleNewsRequest, parser=GoogleNewsParse):
        self.url_gen = url_gen
        self.parser = parser
    
    def get_headlines(self, search_term):
        url = self.url_gen(search_term)

        page = requests.get(url)

        if(page.status_code != 200):
            raise "Bad Status Code: "+page.status_code
        
        soup = BeautifulSoup(page.text, 'html.parser')

        return self.parser(soup)