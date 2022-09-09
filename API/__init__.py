from flask import Flask
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


from API import home
from API import anime 
from API import devian
from API import tmdb 
