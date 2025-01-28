
#some utils

import os
import sys
import datetime
from nicegui import ui

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import quest
import user
import level

db_dir = 'db'
db_path = os.path.join(db_dir, 'game.db')

obj = quest.QuestManager(db_path, 1)
obj_user = user.UserManager(db_path, 1)
obj_level = level.LevelSystem(db_path, 1)

user_id = obj_user.get_active_user_id()

obj = quest.QuestManager(db_path, user_id)
obj_user = user.UserManager(db_path, user_id)
obj_level = level.LevelSystem(db_path, user_id)

def get_js_code():
    return '''
    function openOrFocusTab(url) {
        var tabs = window.tabs || (window.tabs = {});
        
        // Check if the tab reference exists and is not closed
        if (tabs[url] && !tabs[url].closed) {
            tabs[url].focus();
        } else {
            // Open a new tab and store the reference
            tabs[url] = window.open(url, '_blank');
            
            // Handle tab closure
            tabs[url].onbeforeunload = function() {
                delete tabs[url];
                
                // Send an event to the server when the tab is closed
                fetch('/on_tab_closed', {method: 'POST'});
            };
        }
    }
    '''

def handle_upload(event):
    uploaded_file = event.files[0]
    file_path = uploaded_file.path
    # Read the image as binary
    with open(file_path, 'rb') as f:
        return f.read()

def create_quest(name: str, description: str, difficulty: str, startDate: str, endDate: str):
    empty_fields = []

    for field_name, field_value in [("name", name), ("description", description), ("difficulty", difficulty)]:
        if not field_value:
            empty_fields.append(field_name)

    if empty_fields:
        return f"Error! Missing values for: {', '.join(empty_fields)}"
    
    start_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(endDate, "%Y-%m-%d")

    if end_date <= start_date:
        return "Error! The end date must be greater than the start date."

    quests = getAllQuests()

    for quest in quests:
        if quest[2] == name:
            return "Error! A quest with this name is already existing."

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
    return f'Quest was deleted successfully!'

def completeQuest(id: int):
    obj.completeQuest(id)
    return f'Quest was completed successfully!'

def editQuest(id: int, name: str, desc: str, diff: str, start_date, due_date):
    if id is not None and id > 0:
        if name != '' and desc != '':
            obj.editQuest(id, name, desc, diff, start_date, due_date)
            ui.notify("Quest {name} edited")
        else:
            ui.notify("Title and description must be given.")

def completeQuest(id: int):
    howXp = obj.getHowMuchXp(id)
    if howXp:
        obj_level.add_xp(howXp)
    else:
        obj_level.add_xp(2)
        print("Quest hat keine definierte XP, Standardwert wird verwendet.")
    obj.completeQuest(id)

def changePlayer(name: str):
    obj_user.changePlayer(name)

def create_user(name: str, race: str, clas: str, level: int, xp: int, image_data):
    empty_fields = []

    for field_name, field_value in [("name", name), ("race", race), ("clas", clas)]:
        if not field_value:
            empty_fields.append(field_name)

    if empty_fields:
        return f"Error! Missing values for: {', '.join(empty_fields)}"
    
    users = get_all_user()

    if len(users) == 0:
        is_active = 1
    else:
        is_active = 0

    image_path = "obsolet"

    obj_user.createUser(
        name=name,
        image_path=image_path,
        race=race,
        clas=clas,
        level=level,
        xp=xp,
        is_active=is_active,
        image_data=image_data
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
