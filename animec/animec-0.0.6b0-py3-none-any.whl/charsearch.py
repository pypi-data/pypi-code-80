from googlesearch import search
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

class charsearch:
    
    def __init__(self, query):

        if " " in query:
            query = query.replace(" ", "%20")

        html_page = urlopen(f"https://myanimelist.net/character.php?q={query}")
        soup = BeautifulSoup(html_page, 'html.parser')

        char_div = soup.find("td", {'class': 'borderClass bgColor2'})
        char_url = char_div.find("a", href = True)
        url = char_url['href']

        ch_pg = urlopen(url)
        char_page = BeautifulSoup(ch_pg, 'html.parser')

        images = char_page.findAll('img')

        string_list = [str(i) for i in images]

        for k in string_list:
            if 'characters' in k:
                char = k
                break

        image_url = re.search("https://.*jpg", char).group()

        title = char_page.find('h2')
        title = title.get_text()

        self.title = title
        self.url = url
        self.image_url = image_url

print(charsearch("okabe").image_url)