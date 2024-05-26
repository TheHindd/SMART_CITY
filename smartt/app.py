from flask import Flask, request, render_template, g, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'cmse322projterm'
DATABASE = 'users.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    user_name = session.get('user_name', 'Guest')
    return render_template('home.html', name1=user_name)


@app.route('/form_login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name1 = request.form['username']
        pwd = request.form['password']

        if not name1 or not pwd:
            return render_template('login.html', info="All fields are required.")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (name1,))
        user = cursor.fetchone()

        if user is None:
            return render_template('login.html', info="Username doesn't exist. Please try again.")
        elif user[0] != pwd:
            return render_template('login.html', info='Invalid Password')
        else:
            session['user_name'] = name1  # Store the user's name in the session
            if "admin2024" in name1 and "2024" in pwd:
                return render_template('admin_home.html', name=name1, info="Welcome Admin")
            else:
                return redirect(url_for('home'))  # Redirect to the home page

    return render_template('login.html')


@app.route('/form_register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name1 = request.form['username']
        email = request.form['email']
        pwd = request.form['password']

        if not name1 or not email or not pwd:
            return render_template('register.html', info="All fields are required.")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT username, email FROM users WHERE username = ? OR email = ?", (name1, email))
        user = cursor.fetchone()

        if user:
            if user[0] == name1:
                return render_template('register.html', info='Username already exists. Please choose another.')
            elif user[1] == email:
                return render_template('register.html', info='Email already exists. Please choose another.')
        else:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (name1, email, pwd))
            db.commit()
            return render_template('login.html', info='Registration successful. Please log in.')

    return render_template('register.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')


@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')


@app.route('/important_num')
def imp_num():
    return render_template('important_num.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/events')
def events():
    return render_template('events.html')


if __name__ == '__main__':
    init_db()  # Ensure the database and tables are initialized if not existing
    app.run() #TO RUN THE PROGRAM
