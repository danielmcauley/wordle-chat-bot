import random

from sqlalchemy import create_engine
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from twilio.twiml.messaging_response import MessagingResponse

from user import User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gznmmihldcpwar:25576f7f9965581417abf57b1e48cddd23ed157ffe8910c9e6a5ba9ef564dae1@ec2-67-202-63-147.compute-1.amazonaws.com:5432/d6m8dcei8eee3d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()


with open('CSW19.txt', 'r') as f:
    five_letter_words = [w for w in f.read().split('\n') if len(w) == 5]

with open('answers.txt', 'r') as f:
    answer_words = [w.upper() for w in f.read().split('\n')]


@app.route('/bot', methods=['POST'])
def bot():
    resp = MessagingResponse()
    msg = resp.message()

    incoming_msg = request.values.get('Body', '').upper()
    from_str = request.values.get('From', '')
    print(f"incoming_msg: {incoming_msg}")
    print(f"user: {from_str}")

    if User.query.filter_by(from_str=from_str).scalar():
        print("user is in db")
        print(f"retrieving user from db: {from_str}")
        user = db.session.query(User).filter(User.from_str == from_str).first()
        print(user)
        print(type(user))
    else:
        print("user not in db")
        print(f"initializing user: {from_str}")
        user = User(from_str=from_str, answer=random.choice(answer_words))
        db.session.add(user)
        db.session.commit()

    if incoming_msg in five_letter_words:
        clue = get_clue(incoming_msg, user.answer)
        user.tries += 1
        db.session.commit()
        print(f"tries: { user.tries }")
        print(f"guess: { incoming_msg }")
        print(f"answer: { user.answer }")
        print(f"user_states: { user }")
        msg.body(clue)

        if incoming_msg == user.answer:
            msg.body('\nYou won!')
            print(f"deleting user: { user }")
            db.session.delete(user)
            db.session.commit()
            # print(User.query.all())
        elif user.tries == 6:
            msg.body(f"\nYou lost :( ({ user.answer })")
            print(f"deleting user: { user }")
            db.session.delete(user)
            db.session.commit()
    else:
        msg.body('Only English 5-letter words, please!')

    return str(resp)


def get_clue(guess, answer):
    clue = ''
    for (x, y) in zip(guess, answer):
        if x == y:
            clue += '🟩'
        elif x in answer:
            clue += '🟨'
        else:
            clue += '⬛️'
    return clue


if __name__ == '__main__':
    app.run(debug=True)
