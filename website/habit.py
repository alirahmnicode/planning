from flask import Blueprint, request, redirect, url_for, render_template, jsonify
from flask_login import login_required, current_user
from .models import Habit
import datetime
from .utils.owner_check import check
from .utils.calculate_expiration import calculate_term


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


@login_required
@habit.route('edit/<int:habit_id>/', methods=['GET', 'POST'])
def edit_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if request.method == 'POST' and check(current_user.username, habit.user.username):
        name = request.form.get('name')
        description = request.form.get('description')
        term = request.form.get('term')
        expiration = calculate_term(term)
        # set valus
        habit.name = name
        habit.description = description
        habit.expiration = expiration
        habit.save()
        return redirect(url_for('views.dashboard'))

    if request.method == 'GET':
        return render_template('habit/edit.html', habit=habit)

    else:
        return redirect(url_for('views.dashboard'))


@login_required
@habit.post('active/<int:habit_id>/')
def activate(habit_id):
    habit = Habit.query.get(habit_id)
    if request.method == 'POST' and check(current_user.username , habit.user.username):
        print(habit.active)
        if habit.active:
            habit.active = False
        else:
            habit.active = True
        habit.save()
        return jsonify("ok")
    
    else:
        return redirect(url_for('views.dashboard'))