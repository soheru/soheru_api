import requests, random
from API import app 
from flask import redirect, jsonify
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}

@app.route('/')
def mainpage():
    return redirect('https://teamyokai.tech')

@app.route('/alpha/<query>')
def alphacoders(query):
    x = requests.get(f"https://wall.alphacoders.com/api2.0/get.php?auth=6950f559377140a4e1594c564cdca6a3&method=search&term={query}", headers=headers).json().get('wallpapers')
    y = random.choice(x)
    return jsonify({'url_image':y.get('url_image'), 'thumb_url':y.get('url_thumb')})