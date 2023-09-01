from flask import Flask, request, render_template, redirect
from usermanager import UserManager


app = Flask(__name__, template_folder='.')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    args = request.args.to_dict()
    username = args['username']
    user_manager.create_user(username)
    return redirect('/game')


@app.route('/game')
def game():
    return render_template('game.html')


if __name__ == '__main__':
    database_path = "guessthenumber\database.db"
    user_manager = UserManager(database_path)
    user_manager._create_tables()
    app.run()
