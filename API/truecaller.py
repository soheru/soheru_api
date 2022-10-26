import requests
from API import app

@app.route('/truecaller/<query>')
def alphacoders(query):
    url=(f"https://search5-noneu.truecaller.com/v2/search?q=+91{query}&countryCode=IN&type=20&locAddr=&placement=SEARCHRESULTS%2CHISTORY%2CDETAILS&adId=11b72395-38bc-465f-aa5d-689f2cce1a29&encoding=json")
    data = ""
    Bearer="a1i0b--Z8TCObFs-wY81jynjroY1f-HDM8qMPA_doFu8SuC_1979axtLg6LjQHId"
    headers = {"User-Agent":"Truecaller/11.25.6 (Android;9)","Host": "search5-noneu.truecaller.com",
    "Authorization": "Bearer "+ Bearer ,"accept-encoding": "gzip","Connection": "Keep-Alive"}
    x = requests.get(url,data=data,headers=headers)
    return x.json()