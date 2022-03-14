
from builtins import int, print, str
from flask import Flask, Response, abort, render_template, request, session
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null, true

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yddtfownnapucg:b0a986c0582ebfbbaa23abf8e95aae7560b4d6a13c710fa0841f616b17474438@ec2-44-194-116-221.compute-1.amazonaws.com:5432/dfncr07o1t2r9p'

db=SQLAlchemy(app)

class Game(db.Model):
    __tablename__='game'

    id=db.Column(db.Integer, primary_key=True)
    p1=db.Column(db.String(50))
    p2=db.Column(db.String(50))


db.init_app(app)


@app.route("/", methods=['get', 'post'])
def gameplay():
    if request.method == 'POST':
        player=request.json['player']
        value=request.json['value']

        if player == 1:
            get_latest_record().p1 = value
            print("Player 1 has played")
        elif player == 2:
            get_latest_record().p2 = value
            print("Player 2 has played")

        print("Made it to session adding phase")
        db.session.add(get_latest_record())
        db.session.commit()
        return "Game successfully updated", 200

    if request.method == 'GET':
        if (get_latest_record().p1 == None and get_latest_record().p2 == None):
            result = ("\nPlayer 1: {}\nPlayer 2: {}\n{}").format(get_last_record().p1, get_last_record().p2, game_logic(get_last_record().p1, get_last_record().p2))
            return result, 200

        elif (get_latest_record().p1 == None) != (get_latest_record().p2 == None):
            return "Game is still ongoing", 200

        else:
            result = ("\nPlayer 1: {}\nPlayer 2: {}\n{}").format(get_latest_record().p1, get_latest_record().p2, game_logic(get_latest_record().p1, get_latest_record().p2))
            game = Game()
            db.session.add(game)
            db.session.commit()
            return result, 200


def get_latest_record():
    if len(Game.query.all()) == 0:
        game = Game()
        db.session.add(game)
        db.session.commit()
    return Game.query.order_by(Game.id.desc()).first()

def get_last_record():
    return Game.query.order_by(Game.id.desc()).all()[1]

def game_logic(p1, p2):
    if p1 == p2:
        return "It's a tie!"
    elif p1 == "Sakset" and p2 == "Kivi":
        return "Player 2 won!"
    elif p1 == "Sakset" and p2 == "Paperi":
        return "Player 1 won!"
    elif p1 == "Paperi" and p2 == "Kivi":
        return "Player 1 won!"
    elif p1 == "Paperi" and p2 == "Sakset":
        return "Player 2 won!"
    elif p1 == "Kivi" and p2 == "Paperi":
        return "Player 2 won!"
    elif p1 == "Kivi" and p2 == "Sakset":
        return "Player 1 won!"
    else:
        return "Invalid inputs detected"

def init():
    print("Initializing the game")
    if len(Game.query.all()) == 0:
        game = Game()
        db.session.add(game)
        db.session.commit()
    else:
        print("There already is a game initialized")

def main():
    print("Activating Main:")
    init()

    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()