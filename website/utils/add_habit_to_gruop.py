from website.models import Habit, Plan
from flask_login import current_user
import datetime


class Habits:
    def __init__(self, group_id:int) -> None:
        self.group_id = group_id
        
    def add_habit(self):
        objects = self.get_objects()
        for obj in objects:
            if self.check_date(obj):
                self.add_as_plan(obj)

    def add_as_plan(self, obj):
        new_plan = Plan(title=obj.name, description=obj.description,
                            is_done=False, user_id=current_user.id, 
                            group_id=self.group_id)
        new_plan.save() 

    def get_objects(self):
        objects = Habit.query.filter_by(user_id=current_user.id)
        return objects

    def check_date(self, obj):
        return (obj.expiration-datetime.datetime.now()).days >= 0

    
