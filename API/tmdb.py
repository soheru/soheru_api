import requests as r
from API import app
from flask import jsonify

base_url = "https://api.themoviedb.org/3"
pic_url = "https://image.tmdb.org/t/p/original"
TMDBAPI = "2df5093b15a5c8d2ea2a34725ed3de49"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}

def byname(val):
    if val == "":
        return "Not available"
    datalist = []
    for x in val:
        datalist.append(x["name"])
    return datalist

def get_raw_tmdb(c_id):
    payload = {"api_key": TMDBAPI, "language": "en-US", "append_to_response": "videos"}
    x = r.get(f"{base_url}/tv/{c_id}?", params=payload, headers=headers).json()
    return x

def get_beauitfy_details(c_id):
    payload = {"api_key": TMDBAPI, "language": "en-US", "append_to_response": "videos"}
    x = r.get(f"{base_url}/tv/{c_id}?", params=payload, headers=headers).json()
   
    return {
        'original_name':x.get('original_name'),
        'available_in':byname(x.get('networks')),
        'thumbnail':pic_url+x.get('backdrop_path'),
        'first_air_date':x.get('first_air_date'),
        'id':x.get('id'),
        'last_air_date':x.get('last_episode_to_air').get('air_date'),
        'last_episodes':x.get('last_episode_to_air').get('episode_number'),
        'episodes':x.get('number_of_episodes'),
        'next_episode_to_air':x.get('next_episode_to_air'),
        'total_seasons':x.get('number_of_seasons'),
        'episode_run_time':x.get('episode_run_time'),
        'languages':byname(x.get('spoken_languages')),
        'description':x.get('overview'),
        'genres':byname(x.get("genres")),
        'rating':x.get('rating'),
        'studios':byname(x.get('production_companies')),
        'imdbid':x.get('imdb_id'),
    }

def get_shows(query):
    x= r.get(f"{base_url}/search/tv?api_key={TMDBAPI}&language=en&query={query}&page=1&include_adult=true", headers=headers).json().get('results')
    return x[0].get('id'), x

def get_movie(query):
    x= r.get(f"{base_url}/search/movie?api_key={TMDBAPI}&language=en&query={query}&page=1&include_adult=true", headers=headers).json().get('results')
    return x[0].get('id'), x

def moviedata(query):
    payload = {"api_key": TMDBAPI, "language": "en-US", "append_to_response": "videos"}
    data = r.get(f"{base_url}/movie/{query}?", params=payload).json()
    return {
        'c_id' : data.get("id"),
        'title' :data.get("title"),
        'tagline' : data.get("tagline"),
        'status' : data.get("status"),
        'genres' : byname(data.get("genres")),
        'language' : byname(data.get("spoken_languages")),
        'runtime' : data.get("runtime"),
        'release'  : data.get("release_date"),
        'rating'  : data.get("vote_average"),
        'popularity' : data.get("popularity"),
        'overview' : data.get("overview"),
        'posterpath' : data.get("backdrop_path"),
        'homepage' : data.get("homepage"),
        'imdbid' : data.get("imdb_id"),
    }, data
    
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