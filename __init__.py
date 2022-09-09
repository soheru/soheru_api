import random 
import os
import requests 
from flask import Flask, render_template, jsonify, redirect
from .tmdb import get_shows, get_beauitfy_details, get_raw_tmdb, get_movie, moviedata
from .anilist import anime_info, manga_info
app = Flask(__name__)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
@app.route('/')
def mainpage():
    return redirect('https://teamyokai.tech')

@app.route('/alpha/<query>')
def alphacoders(query):
    x = requests.get(f"https://wall.alphacoders.com/api2.0/get.php?auth=6950f559377140a4e1594c564cdca6a3&method=search&term={query}", headers=headers).json().get('wallpapers')
    y = random.choice(x)
    return jsonify({'url_image':y.get('url_image'), 'thumb_url':y.get('url_thumb')})
#------------TMDB---------------------
@app.route('/tmdb/tv/v1/<query>')
def tmdb_v1(query):
    x = get_shows(query)[0]
    return jsonify(get_beauitfy_details(x))

@app.route('/tmdb/tv/<query>')
def tmdb_whole_raw(query):
    x = get_shows(query)
    return jsonify(x[1])

@app.route('/tmdb/tv/raw/<query>')
def tmdb_raw(query):
    x = get_shows(query)
    return jsonify(get_raw_tmdb(x[0]))    

@app.route('/tmdb/movie/v1/<query>')
def tmdbmovie_v1(query):
    x = get_movie(query)[0]
    return jsonify(moviedata(x)[0])

@app.route('/tmdb/movie/<query>')
def tmdbmovie_whole_raw(query):
    x = get_movie(query)
    return jsonify(x[1])

@app.route('/tmdb/movie/raw/<query>')
def tmdbmovie_raw(query):
    x = get_movie(query)
    return jsonify(moviedata(x[0])[1])    
#----------------------------------------
@app.route('/anime/<query>')
def anime_api(query):
    return jsonify(anime_info(query))

@app.route('/manga/<query>')
def manga_api(query):
    return jsonify(manga_info(query))

if __name__ == '__main__':
    app.run()
