from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import Group
from . import db


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return redirect(url_for('views.dashboard'))


@views.get('/dashboard/')
@login_required
def dashboard():
    goups = Group.query.filter_by(user=current_user)
    return render_template('auth/dashboard.html', goups=goups)
