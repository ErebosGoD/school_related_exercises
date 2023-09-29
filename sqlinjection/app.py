from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    print(
        'SELECT * FROM users WHERE username ="' + username + '" AND password ="' + password + '"')
    cursor.execute(
        'SELECT * FROM users WHERE username ="' + username + '" AND password ="' + password + '"')
    record = cursor.fetchall()
    return record


if __name__ == "__main__":
    connection = sqlite3.connect("test.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT
                )''')

    cursor.execute(
        '''INSERT INTO users (username, password) VALUES ("Pedda","Dulli")''')
    cursor.execute(
        '''INSERT INTO users (username, password) VALUES ("Jeanblox", "Ropütz")''')
    connection.commit()
    app.run()
