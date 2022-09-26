from API import app 
from flask import jsonify 
import requests 

ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    endDate {
        day
        month
        year
    }    
    startDate {
        day
        month
        year
    }    
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
    bannerImage
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
 
def animestatus(query):
    search = query
    variables = {'search': search, 'type': "ANIME"}
    json = requests.post(
        url, json={
            'query': ANIME_QUERY,
            'variables': variables
        }).json()
    if 'errors' in json.keys():
        return None
    if json:
        from datetime import date
        print(date.today())
        status = json['data']['Media']['status']    
        if status == 'FINISHED':
            endDate = json['data']['Media']['endDate'] 
            day = endDate.get('day')
            if len(str(day)) == 1:
                day = f"0{day}"
            month = endDate.get('month')
            if len(str(month)) == 1:
                month = f"0{month}"
            year = endDate.get('year')   
            if str(date.today()) == f"{year}-{month}-{day}":
              return "RELEASING"  
    return status
      
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