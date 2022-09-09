import requests, re
from bs4 import BeautifulSoup as bs

def devian(query):
    x = requests.get(f"https://www.deviantart.com/search?q={query}").content
    y = bs(x, "html.parser")
    final = y.find_all('img', src=re.compile('https://images-wixmp'))
    return final
