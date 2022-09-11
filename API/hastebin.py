from API import app
import requests
from flask import request 
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}

@app.route('/paste', methods=['POST', 'GET'])
def hastebin():
    if request.method == 'POST':
        content = request.form['content']
    else:
        content = request.args['content']
    x = requests.post('https://hastebin.com/documents', data={'content':content}, headers=headers).json().get('key')     
    return {'url':f'https://hastebin.com/{x}', 'raw_url':f'https://hastebin.com/raw/{x}'}
    
    




    
   