from flask import Flask, render_template
import random as r
import json

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='index')


def random_alphabet():
    n = list('abcdefghijklmnopqrstuvwxyz')
    o = n.copy()

    def D(l):
        o = l[:]
        while any(x == y for x, y in zip(o, l)): r.shuffle(l)

    D(n)

    ret = {}

    for i in zip(n, o):
        ret[i[0]] = i[1]

    return ret


@app.route('/getnew', methods=['GET'])
def test_words():
    words = [i.replace('\n', '') for i in open('app/static/dictall.txt').readlines()]

    ret = {}

    word = r.choice(words)

    alphabet = random_alphabet()

    ret['correct_word'] = word.upper()
    ret['encoded_word'] = ''.join([alphabet[i] for i in word]).upper()

    ret['guess'] = list(ret['correct_word'])

    # pick a random difficulty percentage from 0.25 to 0.75
    per = 0.33 + r.random()/3

    for i in range(len(word)):
        if r.random() > per:
            ret['guess'][i] = "_"
            per += 0.05

    ret['guess'] = ''.join(ret['guess'])

    if '_' not in ret['guess']:
        return test_words()

    return json.dumps(ret)
