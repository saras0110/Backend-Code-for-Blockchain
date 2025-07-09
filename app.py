
from flask import Flask, render_template, request, redirect, session
import json, os
from blockchain import Blockchain
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

blockchain = Blockchain()

# Load data files
USERS_FILE = 'users.json'
PARTIES_FILE = 'parties.json'
VOTES_FILE = 'votes.json'

# Routes
@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
    users = json.load(open(USERS_FILE))
    uname = request.form['username']
    pwd = request.form['password']
    if uname in users and users[uname] == pwd:
        session['user'] = uname
        return redirect('/countdown')
    return 'Invalid credentials'

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def do_register():
    uname = request.form['username']
    pwd = request.form['password']
    with open(USERS_FILE) as f:
        users = json.load(f)
    users[uname] = pwd
    json.dump(users, open(USERS_FILE, 'w'))
    return redirect('/')

@app.route('/countdown')
def countdown():
    if 'user' not in session:
        return redirect('/')
    return render_template('countdown.html')

@app.route('/vote')
def vote():
    if 'user' not in session:
        return redirect('/')
    with open(PARTIES_FILE) as f:
        parties = json.load(f)
    return render_template('vote.html', parties=parties)

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    if 'user' not in session:
        return redirect('/')
    party = request.form['party']
    blockchain.add_block({'voter': session['user'], 'vote': party})
    blockchain.save_to_file(VOTES_FILE)
    return redirect('/results')

@app.route('/results')
def results():
    data = blockchain.count_votes()
    return render_template('results.html', votes=data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['admin_pass'] == 'admin123':
            session['admin'] = True
            return redirect('/add_party')
        return 'Incorrect password'
    return render_template('admin.html')

@app.route('/add_party', methods=['GET', 'POST'])
def add_party():
    if 'admin' not in session:
        return redirect('/admin')
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        with open(PARTIES_FILE) as f:
            parties = json.load(f)
        parties[name] = image
        json.dump(parties, open(PARTIES_FILE, 'w'))
        return redirect('/add_party')
    return render_template('add_party.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
