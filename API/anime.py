from API import app 
from flask import jsonify 
import requests 

ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    description (asHtml: false)
    format
    status
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
    }
    coverImage {
      extraLarge
    }
    genres
    tags {
      name
    }
    averageScore
    relations {
      edges {
        node {
          title {
            romaji
            english
          }
          id
        }
        relationType
      }
    }
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    isAdult
    isFavourite
    mediaListEntry {
      status
      score
      id
    }
    siteUrl
  }
}
"""

ISADULT = """
query ($id: Int) {
  Media (id: $id) {
    isAdult
  }
}
"""
url = 'https://graphql.anilist.co'

def anime_info(query):
    variables = {'search': query, 'type': "ANIME"}
    if query.isdigit():
        variables = {'id': int(query), 'type': "ANIME"}
    json = requests.post(
        url, json={
            'query': ANIME_QUERY,
            'variables': variables
        }).json()    
    if 'errors' in json.keys():
        return {'success':False}
    else:
        return json
 
MANGA_QUERY = """
query ($search: String, $page: Int) {
  Page (perPage: 1, page: $page) {
    pageInfo {
      total
    }
    media (search: $search, type: MANGA) {
      id
      title {
        romaji
        english
        native
      }
      format
      countryOfOrigin
      source (version: 2)
      status
      description(asHtml: true)
      chapters
      isFavourite
      mediaListEntry {
        status
        score
        id
      }
      volumes
      averageScore
      siteUrl
      isAdult
    }
  }
}
"""   

def manga_info(query):
    variables = {'search': query, 'type': "MANGA"}
    if query.isdigit():
        variables = {'id': int(query), 'type': "MANGA"}
    json = requests.post(
        url, json={
            'query': MANGA_QUERY,
            'variables': variables
        }).json()    
    if 'errors' in json.keys():
        return {'success':False}
    else:
        return json.get('data').get('Page')
    
@app.route('/anime/<query>')
def anime_api(query):
    return jsonify(anime_info(query))

@app.route('/manga/<query>')
def manga_api(query):
    return jsonify(manga_info(query))