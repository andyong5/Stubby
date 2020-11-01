from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
from stubby.models import User, Post
from stubby.users.forms import RegistrationForm, UpdateAccountForm
from stubby.users.utils import save_picture
from authlib.integrations.flask_client import OAuth
from flask import current_app
from stubby import db
from stubby.api_keys import client_id, client_secret

users = Blueprint('users', __name__)

# oAuth Setup
oauth = OAuth(current_app)
google = oauth.register(
    name='google',
    client_id=client_id,
    client_secret=client_secret,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)


@users.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('users.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@users.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()

    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()

    session['profile'] = user_info

    session.permanent = True

    if 'hd' in session["profile"]:
        first_name = session["profile"]['given_name']
        last_name = session["profile"]['family_name']
        email = session["profile"]['email']
        at_sign_index = email.find("@")
        username = email[:at_sign_index]
        profile_pic = session["profile"]["picture"]
    else:
        return redirect('/error')

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, first_name=first_name,
                    last_name=last_name, username=username)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    next_page = request.args.get('next')
    profile_pic = session["profile"]["picture"]
    print(profile_pic)
    return redirect(next_page) if next_page else redirect(url_for('main.home'))


@users.route('/logout')
def logout():
    logout_user()
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('main.front'))


@users.route('/account', methods=["GET", "POST"])
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
        flash("Your account has been updated!", 'success')
        return redirect(url_for('posts.account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('account.html', title="Account", form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    post = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())
    return render_template('user_posts.html', title="Post by " + user.first_name + " " + user.last_name, posts=post, user=user)
