import sys
sys.path.insert(0, "/home/apprenant/Documents/flask-tuto/")
from .utils import row2dict
from werkzeug.utils import redirect
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import row2dict
from flask_login import login_user, login_required, current_user, logout_user
from channel_app import db, app
from .model import Channel, User

@app.route('/')
def home():
    channel_list = []
    for channel in Channel.query.with_entities(Channel.title, Channel.description,Channel.image_url).all():
        channel_list.append(row2dict(channel,column_list=["title","description",'image_url']))
    return render_template("index.html", channel_list = channel_list)

@app.route('/<channel>')
def channel(channel):
    return render_template("channel.html", channel = row2dict(Channel.query.filter_by(title = channel).first()))

@app.route('/new_channel', methods=['POST', 'GET'])
def new_channel():
    if request.method == 'POST':
        channel = Channel(**request.form)
        db.session.add(channel)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("new_channel.html")

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again        
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('home'))

@app.route('/private')
@login_required
def private():
    return f"Bonjour {current_user.name}"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))