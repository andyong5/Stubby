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


