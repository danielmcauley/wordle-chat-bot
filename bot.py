from flask import Flask, request
import requests
import random
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

user_states = {}

with open('CSW19.txt', 'r') as f:
    five_letter_words = [w for w in f.read().split('\n') if len(w) == 5]

with open('answers.txt', 'r') as f:
    answer_words = [w.upper() for w in f.read().split('\n')]

@app.route('/bot', methods=['POST'])
def bot():
    resp = MessagingResponse()
    msg = resp.message()

    incoming_msg = request.values.get('Body', '').upper()
    user = request.values.get('From', '')
    print(f"incoming_msg: {incoming_msg}")
    print(f"user: {user}")

    if user not in user_states.keys():
        print("user not in user_states.keys()")
        print(f"initializing user: {user}")
        initialize_user(user, user_states)

    if incoming_msg in five_letter_words:
        clue = get_clue(incoming_msg, user_states[user]['answer'])
        user_states[user]['tries'] += 1
        print(f"tries: {user_states[user]['tries']}")
        print(f"guess: {incoming_msg}")
        print(f"answer: {user_states[user]['answer']}")
        print(f"user_states: {user_states}")
        msg.body(clue)

        if incoming_msg == user_states[user]['answer'] :
            msg.body('\nYou won!')
            print(f"re-initializing user: {user}")
            initialize_user(user, user_states)
        elif user_states[user]['tries'] == 6:
            msg.body(f"\nYou lost :( ({user_states[user]['answer']})")
            print(f"re-initializing user: {user}")
            initialize_user(user, user_states)
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

def initialize_user(user, user_states):
    answer = random.choice(answer_words)
    print(answer)
    user_states[user] = {'answer': answer, 'tries': 0}
    print(f"user_states: {user_states}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)