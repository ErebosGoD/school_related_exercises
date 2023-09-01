from flask import Flask, request, render_template, redirect, url_for
from usermanager import UserManager
from gamemanager import GameManager


app = Flask(__name__, template_folder='.')

users = {}
attempts = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    print(username)
    user_manager.create_user(username)
    return redirect(url_for('game', name=username))


@app.route('/game/<name>')
def game(name):
    random_number = game_manager.get_random_number()
    return render_template('game.html', username=name, random_number=random_number)


@app.route('/check-guess')
def check_guess():
    guess = int(request.form.get('guess'))


if __name__ == '__main__':
    database_path = "guessthenumber\database.db"
    user_manager = UserManager(database_path)
    user_manager._create_tables()
    game_manager = GameManager()
    app.run()
