from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import os
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://'+os.environ['DATABASE_USER']+':'+os.environ['DATABASE_PASSWORD']+'@localhost/'+os.environ['DATABASE_NAME']
db = SQLAlchemy(application)

games = db.Table('games',
                 db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
                 db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
)

variants = db.Table('variants',
                    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
                    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)

player_sessions = db.Table('player_sessions',
                           db.Column('game_sessions_id', db.Integer, db.ForeignKey('game_sessions.id')),
                           db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    screen_name = db.Column(db.String(160), unique=True)
    desk_location = db.Column(db.String(160), unique=True)
    games = db.relationship('Game', secondary=games, backref=db.backref('players', lazy='dynamic'))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    variants = db.relationship('Game', secondary=variants, backref=db.backref('games', lazy='dynamic'))
    owners = db.relationship('Player', secondary=games, backref=db.backref('players', lazy='dynamic'))

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    play_date = db.Column(db.DateTime)
    players = db.relationship('Player', secondary=game_sessions, backref=db.backref('players', lazy='dynamic'))


@application.route("/health")
def health():
    return 'working'

@application.route("/", methods=['GET'])
def hello():
    if request.args.get('q', ""):
        return "Hello my main daimie! %s"%(request.args.get('q', ""),)
    else:
        return "Hello World!"

if __name__ == "__main__":
    application.run()
