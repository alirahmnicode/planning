from flask import Blueprint, request, redirect
from flask_login import login_required, current_user


habit = Blueprint('habit', __name__)

@login_required
@habit.route('add/', methods=['GET', 'POST'])
def add_habit():
    print('ali')
    