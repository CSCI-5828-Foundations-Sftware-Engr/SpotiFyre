from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users
from . import db
from flask_login import login_user

auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    return render_template('home.html')

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Users.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        # flash('Please check your login details and try again.')
        response = {'success': False, 'message': 'Please check your login details and try again.'}
        return jsonify(response)
        # if the user doesn't exist or password is wrong, reload the page
        # return redirect(url_for('auth.login'))

    # login code goes here
    login_user(user, remember=False)
    session['user_id'] = user.id

    response = {'success': True, 'message': 'Login Successful'}
    return jsonify(response)
    # return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password, method='sha256')

    user = Users.query.filter_by(email=email).first()

    if user:
        # flash('email exists', 'danger')
        # return redirect(url_for('auth.login'))

        response = {'success': False, 'message': 'Please check your login details and try again.'}
        return jsonify(response)

    new_user = Users(email=email, name=name,
                     password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        print("failed")

    response = {'success': True, 'message': ' Sign up successful'}
    return jsonify(response)
    # return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    response = {'success': True, 'message': 'Logged out successfully'}
    return jsonify(response)
    # return redirect('/')