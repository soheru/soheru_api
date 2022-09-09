import requests, random
from API import app, db
from flask import redirect, jsonify
from datetime import datetime
from API.routes import generate_short_id
from API.models import ShortUrls

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}

@app.route('/')
def mainpage():
    return redirect('https://teamyokai.tech')

@app.route('/alpha/<query>')
def alphacoders(query):
    x = requests.get(f"https://wall.alphacoders.com/api2.0/get.php?auth=6950f559377140a4e1594c564cdca6a3&method=search&term={query}", headers=headers).json().get('wallpapers')
    y = random.choice(x)
    
    short_id = generate_short_id(8)
    thumb = ShortUrls(original_url=y.get('url_thumb'), short_id=short_id, created_at=datetime.now())
    urlimage = ShortUrls(original_url=y.get('url_image'), short_id=short_id, created_at=datetime.now())
    db.session.add(thumb)
    db.session.add(urlimage)
    db.session.commit()
    return jsonify({'url_image':urlimage, 'thumb_url':thumb})