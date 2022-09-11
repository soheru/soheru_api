from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['FLASK_APP']='API'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xmfzqksv:DwEFghfDu6PSqI0umNTQImL_PcIsNsdv@jelani.db.elephantsql.com/xmfzqksv'
app.config['SECRET_KEY']='verysss@@454521202++51fg44escretkeysojhiasbjswy8'
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()
    
migrate = Migrate(app, db)

from API import home
from API import anime 
from API import devian
from API import tmdb 
from API import routes
from API import models
from API import hastebin