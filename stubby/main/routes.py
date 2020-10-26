from flask import Blueprint, render_template, request
from stubby.models import Post
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
def front():
    return render_template('index.html', title="Stubby - Log In or Sign Up")


@main.route('/home')
def home():
    posts = Post.query.all()
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('home.html', title="Home", posts=posts)


@main.route('/error')
def error():
    return render_template('erroremail.html', title="Stubby - Log In or Sign Up")


@main.route('/post/new', methods=["GET", "POST"])
@login_required
def classes():
    form = AddClass()
    return render_template('classes.html', title="Classes", form=form)


@main.route('/add_class', methods=["GET", "POST"])
@login_required
def add_class():
    form = AddClass()
    return render_template('add_class.html', title="Add Classes", form=form)
