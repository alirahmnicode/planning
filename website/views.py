from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import desc
from .models import Group, Plan
from .utils.constant import WEEKLY_DATE_FORMAT, TODAY_FORMAT
import datetime
import math


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return redirect(url_for('views.dashboard'))


@views.get('/dashboard/')
@login_required
def dashboard():
    groups = Group.query.filter_by(user=current_user).order_by(desc(Group.date))
    if len(list(groups)) > 0:
        today_list = groups[0]
    else:
        today_list = None
    return render_template('auth/dashboard.html', groups=groups, today_list=today_list)


@views.get('/report/')
def report():
    return render_template('report.html')


@views.get('/chart/week/')
def weekly_chart():
    week_n = int(request.args.get("n"))
    g_plans = Group.query.filter_by(user=current_user)
    weekly_data = get_the_plans_done(list(g_plans), week_n)
    start_date = g_plans.first()
    end_date = g_plans.order_by(desc(Group.date)).first()
    data = {
        "weekly_data": weekly_data,
        "weeks_count":math.ceil(((end_date.date - start_date.date).days+1) / 7)
    }
    return jsonify(data)


def get_the_plans_done(query, week_n):
    plans = []
    day_count = 0
    period = 7
    end_of_period = (week_n * period) 
    start_fo_period = end_of_period - period
    for i in range(len(query)):
        day_count += 1
        if day_count > end_of_period:
            return plans[start_fo_period:end_of_period]
        # add plans 
        day_plans = query[i]
        next_day_date = day_plans.date + datetime.timedelta(days=1)
        # create daily plans obj and add to plans
        daily_plans = {
            'day':day_plans.date.strftime(WEEKLY_DATE_FORMAT),
            'percent': get_percent(query[i].id),
        }
        plans.append(daily_plans)
        # create empty daily plans obj
        if i < len(query)-1:
            while next_day_date.day != query[i+1].date.day:
                day_count += 1
                if day_count > end_of_period:
                    return plans[start_fo_period:end_of_period]
                daily_plans = {
                    'day':next_day_date.strftime(WEEKLY_DATE_FORMAT),
                    'percent': 0,
                }
                plans.append(daily_plans)
                next_day_date = next_day_date + datetime.timedelta(days=1)
    return plans[start_fo_period:end_of_period]
        

def get_percent(group_id):
    plans = Plan.query.filter_by(user=current_user).filter_by(group_id=group_id)
    plans_length = len(list(plans))
    plans_done_lenght = len(list(plans.filter_by(is_done=True)))
    return int((plans_done_lenght/plans_length)*100)
