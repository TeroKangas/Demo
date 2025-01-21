
#some utils

import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import quest
import user

db_dir = 'db'
db_path = os.path.join(db_dir, 'game.db')
obj = quest.QuestManager(db_path, 1)
obj_user = user.UserManager(db_path, 1)


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

def getAllOpenQuests():
    quests = obj.getOpenQuests()
    return quests

def getAllQuests():
    quests = obj.getAllQuests()
    return quests

def getAllCompletedQuests():
    quests = obj.getCompletedQuests()
    return quests

def deleteQuest(id: int):
    obj.deleteQuest(id)

def completeQuest(id: int):
    obj.completeQuest(id)

def editQuest(id: int, name: str, desc: str, diff: str, start_date, due_date):
    obj.editQuest(id, name, desc, diff, start_date, due_date)

def completeQuest(id: int):
    obj.completeQuest(id)

def changePlayer(name: str):
    obj_user.changePlayer(name)

def editQuest(id: int, name: str, desc: str, diff: str, start_date, due_date):
    obj.editQuest(id, name, desc, diff, start_date, due_date)

def create_user(name: str, image_path: str, race: str, clas: str, level: int, xp: int):
    empty_fields = []

    for field_name, field_value in [("name", name), ("image_path", image_path), ("race", race), ("clas", clas)]:
        if not field_value:
            empty_fields.append(field_name)

    if empty_fields:
        return f"Error! Missing values for: {', '.join(empty_fields)}"
    
    users = get_all_user()

    if len(users) == 0:
        is_active = 1
    else:
        is_active = 0

    obj_user.createUser(
        name=name,
        image_path=image_path,
        race=race,
        clas=clas,
        level=level,
        xp=xp,
        is_active=is_active
    )

    return f'User "{name}" created successfully!'

def get_all_user():
    user = obj_user.getAllUser()
    return user

def delete_user(id: int):
    obj_user.deleteUser(id)
    return 0

def update_user(id: int, name: str = None, image_path: str = None, race: str = None, clas: str = None):
    obj_user.updateUser(id, name, image_path, race, clas)
    return 0

def activate_user(id: int):
    msg = obj_user.getAllUser()
    return msg
