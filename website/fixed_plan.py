from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import FixedPlan


fixes = Blueprint('fixes', __name__)

@login_required
@fixes.route('add/', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        time = f"{request.form.get('start')}-{request.form.get('end')}"
        new_plan = FixedPlan(name=name, description=description, time_to_do=time, 
                                user_id=current_user.id)
        new_plan.save()
        return redirect(url_for('views.dashboard'))

    if request.method == 'GET':
        return render_template('fixed/add.html')