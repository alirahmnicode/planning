from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
from .utils.password_validation import vlidate


auth = Blueprint('auth', __name__)

@auth.get('/signup/')
def signup():
    return render_template('auth/signup.html')


@auth.post('/signup/')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('password2')

    password_validation = vlidate(password, confirm_password)
    if len(password_validation) > 0:
        flash(password_validation)
        return redirect(request.referrer)
    user = User.query.filter_by(username=username).first()
    
    if user:
        flash('The username already exists')
        return redirect(url_for('auth.signup'))
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, True)
    return redirect(url_for('views.home'))


@auth.get('/login/')
def login():
    return render_template('auth/login.html')


@auth.post('/login/')
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    print(username, password)
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, True)
    return redirect(url_for('views.home'))


@auth.get('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
