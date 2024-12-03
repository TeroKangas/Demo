#some utils

import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import quest

db_dir = 'db'
db_path = os.path.join(db_dir, 'game.db')
obj = quest.QuestManager(db_path, 1)

def create_quest(name: str, description: str, difficulty: str, startDate: str, endDate: str):
    empty_fields = []

    for field_name, field_value in [("name", name), ("description", description), ("difficulty", difficulty)]:
        if not field_value:
            empty_fields.append(field_name)

    if empty_fields:
        return f"Error! Missing values for: {', '.join(empty_fields)}"
    
    obj.createQuest(
        name=name,
        description=description,
        difficulty=difficulty,
        start_date=startDate,
        due_date=endDate
    )
    
    return f'Quest "{name}" created successfully!'

