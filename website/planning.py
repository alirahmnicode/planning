from flask import request, redirect, url_for, Blueprint, render_template, jsonify
from flask_login import current_user, login_required
from .models import Group, Plan
from . import db
from website.utils.owner_check import check
from .utils.add_habit_to_gruop import Habits

plan = Blueprint('plan', __name__)

@login_required
@plan.route('group/add/', methods=['GET', 'POST'])
def add_new_group():
    if request.method == 'POST':
        name = request.form.get('name')
        new_group = Group(name=name, user_id=current_user.id)
        new_group.save()
        # add habit to this group
        habits = Habits(new_group.id)
        habits.add_habit()
        return redirect(url_for('views.dashboard'))

    if request.method == 'GET':
        return render_template('planning/add_group.html')


@login_required
@plan.route('add/<int:group_id>/', methods=['GET', 'POST'])
def add_new_plan(group_id):
    if request.method == 'GET':
        return render_template('planning/add_plan.html')

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_plan = Plan(title=title, description=description,
                        is_done=False, user_id=current_user.id, 
                        group_id=group_id)
        new_plan.save()                    
        return redirect(url_for('views.home'))


@login_required
@plan.post('done/<int:plan_id>/')
def is_done(plan_id):
    item = Plan.query.get(plan_id)
    if item.is_done:
        item.is_done = False
    else:
        item.is_done = True
    item.save()
    return jsonify(item.is_done)


@login_required
@plan.route('edit/<int:plan_id>/', methods=['GET', 'POST'])
def edit_plan(plan_id):
    item = Plan.query.get(plan_id)
    if request.method == 'GET':
        return render_template('planning/edit.html', item=item)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        item.title = title
        item.description = description
        item.save()
        return redirect(url_for('views.dashboard'))


@login_required
@plan.route('delete/<int:plan_id>/', methods=['GET', 'POST'])
def delete_plan(plan_id):
    item = Plan.query.get(plan_id)
    if request.method == 'GET':
        return render_template('planning/delete_plan.html')
    if request.method == 'POST' and check(current_user.username, plan.user.username):
        plan.delete_obj()
        return redirect(url_for('views.dashboard'))



