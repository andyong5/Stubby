from flask import Flask, redirect, url_for, session, render_template, request, flash, abort
from authlib.integrations.flask_client import OAuth
import os
import secrets
from PIL import Image
from datetime import timedelta
from stubby.forms import RegistrationForm, UpdateAccountForm, PostForm, AddClass
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
    posts = Post.query.all()
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('home.html', title="Home", posts=posts)


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
    return redirect(next_page) if next_page else redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('/'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.file_name)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, '/static/profile_pic', picture_fn)
    output_size(125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


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
        flash("Your account has been updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('account.html', form=form)


@app.route('/post/new', methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title="New Post", form=form, legend="New Post")


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title="Update Post", form=form, legend="Update Post")


@app.route('/post/<int:post_id>/delete', methods=["POST"])
@login_required
def delete_post(post_id):
    print(post_id)
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/post/new', methods=["GET", "POST"])
@login_required
def classes():
    form = AddClass()
    return render_template('classes.html', title="Classes", form=form)


@app.route('/add_class', methods=["GET", "POST"])
@login_required
def add_class():
    form = AddClass()
    return render_template('add_class.html', title="Add Classes", form=form)


@app.route('/user/<int:id>')
def user_posts(id):
    user = User.query.filter_by()
    post = Post.query.filter_by(user_id=user).order_by(Post.date_posted.desc())
    return render_template('user_posts.html', title="Add Classes", form=form, posts=posts, user=user)
