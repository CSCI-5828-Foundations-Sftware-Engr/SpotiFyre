from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

host = os.getenv('PQ_HOST', "postgres-db-postgresql")
port = os.getenv('PQ_PORT', "5432")
user = os.getenv('PQ_USER', "root")
passWd = os.getenv('PQ_PASS', "algo123")
pqdb = os.getenv('PQ_DB', "spotifyre_db")


url = f'postgresql://{user}:{passWd}@{host}:{port}/{pqdb}'
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        user = Users(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()
        if not user:
            return render_template('login.html', error='Invalid email or password')

        if not check_password_hash(user.password, password):
            return render_template('login.html', error='Invalid email or password')

        session['user_id'] = user.id
        return redirect('/profile')

    return render_template('login.html')

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return redirect('/login')

    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

#@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hi  ddddd {}!".format(name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
