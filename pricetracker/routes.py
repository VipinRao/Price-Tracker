import os
import time
import secrets
from PIL import Image
from datetime import datetime
from celery import shared_task
import requests
import json
from flask import render_template, url_for, redirect, request, flash #for message
from pricetracker.forms import RegistrationForm,UpdateAccountForm, LoginForm, SearchForm
from pricetracker.models import User
from pricetracker import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from bs4 import BeautifulSoup
import smtplib  #simple mail transfer protocol smtp
# from pricetracker.rabbit import start

interval_user = {}     # interval -> user_id
url_dict = {}
from redis import Redis
import rq
queue = rq.Queue('q1',connection = Redis.from_url('redis://'))


@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
@login_required
def home():
    form = SearchForm()
    if form.validate_on_submit():
        #interval -> [time of request1 to enter system], [request1], [request2], [request3]
        #all request of one interval will be checked at once w.r.t time of first request
        # if not form.interval in interval_user:
            # interval_user[form.interval] = [time.time()]
        if form.url not in url_dict:
            url_dict[form.url.data] = True
            print('DATA: \n\n\n\n')
            print(form.url.data)
            print(form.target_price.data)
            print(current_user.email)
            queue.enqueue('pricetracker.rabbit.start',[form.url.data,form.target_price.data,str(current_user.email),time.time()])
            # queue.enqueue('pricetracker.rabbit.start',20)
        # interval_user[form.interval].append([form.url, form.target_price, current_user.email, time.time()])
        # print(interval_user)
        flash('{}, your request is successfully registered, you will be recieve email when price has fallen down to target price'.format(current_user.username),'success')
        return redirect(url_for('home'))

    return render_template('home.html',form=form)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # flash(f'Account Created Successfully for {form.username.data}','success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created Successfully!','success')
        return redirect(url_for('home')) #name of function for that route
    return render_template('register.html', title='Register',form  =form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next') #[] dont use it will show error if page not exit in dictionary
            return redirect(next_page if next_page else url_for('home')) #name of function for that route
        else:
            flash(f'Unsuccessfull Login','danger')
    return render_template('login.html', title='Login',form  =form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #randomise image name as it can collide
    _, f_ext = os.path.splitext(form_picture.filename)  #file_name will be unused
    picture_fn  = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)

    i = Image.open(form_picture)
    i.thumbnail((125,125))  #125px 125 px scaling of image to make website fast
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated Successfully','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)
