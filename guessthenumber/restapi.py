import os
import random
from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from usermanager import UserManager

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24).hex()  # Zufälliger Sitzungsschlüssel


# Dictionaries, um Benutzer, ihre Versuche und ihren Score zu verfolgen
users = {}
attempts = {}
scores = {}


def is_user_authenticated():
    return 'username' in session


def has_permission(username):
    return session.get('username') == username


def login_required(view_function):
    @wraps(view_function)
    def decorated_view(*args, **kwargs):
        if not is_user_authenticated() or not has_permission(session.get('username')):
            flash('You need to log in first', 'User not logged in')
            return redirect(url_for('index'))
        return view_function(*args, **kwargs)
    return decorated_view


def generate_random_key(length=24):
    """
    Generates a random key with the specified length.
    """
    key = os.urandom(length)
    return key.hex()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user_manager.create_user(username, password)
            return redirect(url_for('index'))
        except ValueError as e:
            return render_template('register.html', error=str(e))

    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    session.clear()
    username = request.form.get('username')
    password = request.form.get('password')

    if username not in attempts:
        attempts[username] = 0

    user = user_manager.get_user(username)

    if user and check_password_hash(user['password'], password):
        session['username'] = username
        return redirect(url_for('game', name=username))
    else:
        print("check funktioniert nicht")
        return render_template('index.html', error='Ungültige Anmeldedaten')


@app.route('/game/<name>', methods=['GET', 'POST'])
@login_required
def game(name):
    username = session.get('username')
    random_number = session.get('random_number')
    if random_number is None:
        random_number = random.randint(1, 100)
        session['random_number'] = random_number
    if username:
        random_number = session.get('random_number')
        result = ""

        if request.method == 'POST':
            guess = int(request.form.get('guess'))
            result = check_guess_result(int(random_number), guess)

            attempts[username] += 1

            scores[username] = calculate_highscore(attempts[username])

            if result == "Correct":
                user_manager.update_score(scores[username], username)
                return redirect(url_for('guess_result', name=username, random_number=random_number, score=scores[username]))

        return render_template('game.html', username=username, attempts=attempts.get(name, 0), result=result, score=scores.get(name, 0))

    else:
        return redirect(url_for('index'))


@app.route('/guess_result/<name>')
@login_required
def guess_result(name):
    random_number = session.get('random_number')
    score = scores.get(name, 0)

    return render_template('guess_result.html', username=name, random_number=random_number, score=score)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def check_guess_result(random_number, guess):
    if guess < random_number:
        return "Too low"
    elif guess > random_number:
        return "Too high"
    else:
        return "Correct"


def calculate_highscore(guess_count):
    highscore = max(1000 - 2 ** (guess_count - 1), 0)
    return highscore


if __name__ == '__main__':
    database_path = "guessthenumber\database.db"
    user_manager = UserManager(database_path)
    user_manager._create_tables()
    app.run()
