from flask import Flask, redirect, url_for, session, render_template, request
from authlib.integrations.flask_client import OAuth
import os
import secrets
from PIL import Image
from datetime import timedelta
from stubby.forms import RegistrationForm, UpdateAccountForm, PostForm
from stubby import app, db
from flask_login import login_user, current_user, logout_user, login_required

from stubby.models import User, Post

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="238435131938-fejoag3giucdk0a1f8e0i5g1jti8t5rl.apps.googleusercontent.com",
    client_secret="fscGQxjoaNtx7jX04zTRuFnI",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/')
def front():
    return render_template('index.html', title="Stubby - Log In or Sign Up")


@app.route('/home')
def home():
    return render_template('home.html', title="Home")


@app.route('/error')
def error():
    return render_template('erroremail.html', title="Stubby - Log In or Sign Up")


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()

    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()

    session['profile'] = user_info

    session.permanent = True
    print(session['profile'])
    if 'hd' in session["profile"]:
        first_name = session["profile"]['given_name']
        last_name = session["profile"]['family_name']
        email = session["profile"]['email']
        profile_pic = session["profile"]["picture"]
    else:
        return redirect('/error')

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    next_page = request.args.get('next')
    profile_pic = session["profile"]["picture"]
    print(profile_pic)
    return redirect(next_page) if next_page else redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('front'))


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.file_name)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(
#         app.root_path, '/static/profile_pic', picture_fn)
#     output_size(125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#     return picture_fn


@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.iamge_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('account.html', form=form)


@app.route('/post/new', methods=["GET", "POST"])
@login_required
def new_post():
    form = postForm()
    if form.validate_on_submit():
        flash("Your post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title="New Post", form=form)
