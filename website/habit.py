from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from .models import Habit
import datetime
from .utils.owner_check import check


habit = Blueprint('habit', __name__)

@login_required
@habit.route('add/', methods=['GET', 'POST'])
def add_habit():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        term = request.form.get('term')
        expiration = calculate_term(term)
        new_habit = Habit(name=name, description=description, 
                            expiration=expiration, user_id=current_user.id)
        new_habit.save()
        return redirect(url_for('views.dashboard'))
    
    if request.method == 'GET':
        return render_template('habit/add.html')

@login_required
@habit.route('delete/<int:habit_id>/', methods=['GET', 'POST'])
def delete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if request.method == 'POST' and check(current_user.username, habit.user.username):
        habit.delete_obj()
        return redirect(url_for('views.dashboard'))

    elif request.method == 'GET':
        return render_template('delete_obj.html')

    else:
        return redirect(url_for('views.dashboard'))
        

def calculate_term(term):
    now = datetime.datetime.now()
    if term == 'year':
        expiration = now + datetime.timedelta(days=365)
    elif term == 'month':
        expiration = now + datetime.timedelta(days=30)
    else:
        expiration = now + datetime.timedelta(days=7)
    return expiration

