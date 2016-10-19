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

# player_sessions = db.Table('player_sessions',
#                            db.Column('game_sessions_id', db.Integer, db.ForeignKey('game_sessions.id')),
#                            db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
# )

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    screen_name = db.Column(db.String(160), unique=True)
    desk_location = db.Column(db.String(160), unique=True)
    games = db.relationship('Game', secondary=games, backref=db.backref('players'))

    def __init__(self, username, screen_name):
        self.username = username
        self.screen_name = screen_name

    def __repr__(self):
        return "<Player: %s (%s)>" % (self.screen_name, self.username)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    variants = db.relationship('Game', secondary=variants, backref=db.backref('games'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Game: %s>" % self.name

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    play_date = db.Column(db.DateTime)
    players = db.relationship('Player', backref='player')
    winner = db.Column(db.Integer, db.ForeignKey('player.id'))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))

    def __init__(self, play_date):
        self.play_date = play_date

    def __repr__(self):
        return "<GameSession date: %s, Game: %s>" % (self.play_date, self.game.name)

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
