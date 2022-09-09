import requests, re
from bs4 import BeautifulSoup as bs
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}

def devian(query):
    x = requests.get(f"https://www.deviantart.com/search?q={query}", headers=headers).content
    y = bs(x, "html.parser")
    ks = []
    for item in y.find_all('img', src=re.compile('https://images-wixmp')):
        ks.append(item['src'])  
    return ks    
          
