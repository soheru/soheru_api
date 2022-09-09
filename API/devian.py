import requests, re
from API import app 
from flask import request 
from datetime import datetime
from bs4 import BeautifulSoup as bs
from API.routes import generate_short_id
from API.models import ShortUrls
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}

def devian(query):
    x = requests.get(f"https://www.deviantart.com/search?q={query}", headers=headers).content
    y = bs(x, "html.parser")
    ks = []
    for item in y.find_all('img', src=re.compile('https://images-wixmp')):
         
        url = item['src']
        short_id = generate_short_id(8)
        new_link = ShortUrls(
            original_url=url, short_id=short_id, created_at=datetime.now()
        )
        ks.append(request.host_url + "short/" + short_id) 
    return ks  


@app.route('/devian/<query>')
def devian_nolimit(query):
    return {'images':devian(query)}