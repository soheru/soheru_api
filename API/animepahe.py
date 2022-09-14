from API import app
import requests
from flask import request 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}


def dict_executor(x):
    y = x.get('360')
    if y is not None:
        resolution = '360p'
    if y is None:
        y = x.get('480')
        resolution = "480p"
    if y is None:
        y=x.get('720')
        resolution = "720p"
    if y is None:
        y=x.get('1080')    
        resolution = "1080p"
    kwik = y.get('kwik')    
    kwiksearch = requests.get(kwik, headers={'Referer':'https://kwik.cx/'})
    urlsplit = kwiksearch.text.rsplit('Plyr', 1)[1].split('</script>')[0].split('.split')[0].split('|')
    kwik = f"https://na-{urlsplit[-3]}.files.nextcdn.org/hls/{urlsplit[-8]}/{urlsplit[3]}/owo.m3u8"
    return y, resolution, kwik, y.get('audio')

@app.route('/animepahe/download/<query>')
def animepahe_direct(query):
    pahe_ep_url = f"https://animepahe.com/api?m=links&id={query}&p=kwik"
    data = requests.get(pahe_ep_url, headers=headers).json().get('data') 
    list_to_process = []
    list_to_process.clear()
    check_eng_or_not = None
    #AUDIO CHECK 
    for x in data:
        y = dict_executor(x)
        audio = y[0].get('audio')
        if audio == "eng":
            check_eng_or_not = True       
    for x in data:
        y = dict_executor(x)
        resolution = y[1]
        link = y[2]
        audios = y[3]
        if check_eng_or_not is True:
            audio = "english"
            if audios == 'eng':
                list_to_process.append({'url':link, "quality":resolution, 'audio':'english'})         
        elif check_eng_or_not is None:
            audio = 'japanese'    
            if audios == 'jpn':
                list_to_process.append({'url':link, "quality":resolution, 'audio':'japanese'})   
    return {'sources':list_to_process}     
            
                
@app.route('/animepahe/search/<query>')
def animepahe_search(query):
    x = requests.get(f'https://animepahe.com/api?m=search&q={query}', headers=headers).json().get('data')
    results = []
    for x in x: 
        id = x.get('session')
        title = x.get('title')
        results.append({'id':id, 'title':title})
    return {'results':results}    
                                
             
        
        
    