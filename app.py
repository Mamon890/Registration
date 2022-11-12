import requests, psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

conn = psycopg2.connect(database="service_db", user="admin", password="admin", host="localhost", port="5432")
cursor = conn.cursor()


@app.route("/")
def index():
    return render_template("login.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == "Admin" and password == "UniPass":
                return render_template("admin.html")
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if not username or not password:
                return render_template('login.html', error="You must enter a Login and Password!")
            elif len(records) == 0:
                return render_template('login.html', error="Login or Password is incorrect!")
            else:
                return render_template('account.html', full_name=records[0][1], login=records[0][1],
                                       password=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration")
    return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if request.form.get('signup'):
            if not name or not login or not password:
                return render_template('registration.html', error="All fields are required")

        cursor.execute('SELECT id FROM service.users WHERE login = %s', (login,))
        user = cursor.fetchone()
        if request.form.get('signup'):
            if user:
                return render_template('registration.html', error="User with this login already exists")

            cursor.execute('INSERT INTO service.users(full_name, login, password) VALUES(%s, %s, %s);',
                           (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login')

    return render_template('registration.html')

if __name__ == "__main__":
    app.run()