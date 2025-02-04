
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
    return f'Quest with {id} was deleted successfully!'

def editQuest(quest):
    if quest[0] is not None and quest[0] > 0:
        if quest[2] != '' and quest[3] != '':
            obj.editQuest(quest[0], quest[2], quest[3], quest[4], quest[5], quest[6])
            ui.notify(f"Quest {quest[3]} edited")
        else:
            ui.notify("Title and description must be given.")

def completeQuest(id: int):
    howXp = obj.getHowMuchXp(id)
    if howXp:
        obj_level.add_xp(howXp)
        obj.completeQuest(id)
        return f'Quest with id {id} was completed succesfully!'
    else:
        obj_level.add_xp(2)
        obj.completeQuest(id)
        return f'Quest {id} has no defined xp, 2 xp will be awarded'

def changePlayer(name: str):
    obj_user.changePlayer(name)

def create_user(name: str, race: str, clas: str, level: int, xp: int, picture_path: str):
    empty_fields = []

    for field_name, field_value in [("name", name), ("race", race), ("clas", clas)]:
        if not field_value:
            empty_fields.append(field_name)

    if empty_fields:
        return f"Error! Missing values for: {', '.join(empty_fields)}."
    
    if picture_path == "":
        return f"Error! No profile picture selected."
    
    users = get_all_user()

    if len(users) == 0:
        is_active = 1
    else:
        is_active = 0

    obj_user.createUser(
        name=name,
        image_path=picture_path,
        race=race,
        clas=clas,
        level=level,
        xp=xp,
        is_active=is_active,
    )

    return f'User "{name}" created successfully!'

def get_all_user():
    user = obj_user.getAllUser()
    return user

def delete_user(id: int):
    obj_user.deleteUser(id)

def update_user(id: int, name: str = None, image_path: str = None, race: str = None, clas: str = None):
    obj_user.updateUser(id, name, image_path, race, clas)

def get_active_user_id():
    active_user_id = obj_user.getActiveUser()
    return active_user_id

def change_user(name: str):
    if name != '':
        changePlayer(name)
        ui.notify('Player changed')

def change_picture(path: str):
    msg = obj_user.change_picture_path(path)
    return msg

def get_image_path(player_id: int):
    image_path = obj_user.getImagePath(player_id)
    return image_path

def set_profile_image_size():
    #evtl. dynamisch machen
    width = 100
    height = 100
    return width, height

def show_player_name_and_level():
    users = get_all_user()
    if len(users) == 0:
        return "Player: not selected"
    else:  
        for user in users:
            abc = user
            if abc[8] == 1: #if user is active
                name = abc[1]
                levelDisplayed = abc[6]
                return f"Player name: {name} | Level: {levelDisplayed}"

    return "No user is activated"

def show_picture():
    width, height = set_profile_image_size()
    active_user_id = get_active_user_id()
    if active_user_id != "no_user":
        path = get_image_path(active_user_id)
        path = path[0] if isinstance(path, tuple) else path
        filename = path.rsplit("/", 1)[-1]
        ui.image(source=f"app/static/{filename}").style(f"width: {width}px; height: {height}px; object-fit: cover;")
    
