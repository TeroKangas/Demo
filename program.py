from datetime import datetime, timedelta  
from nicegui import ui                   

from app.utils import (
    create_quest, getAllCompletedQuests, deleteQuest, completeQuest,
    editQuest, create_user, update_user, get_all_user, delete_user,
    changePlayer, getAllOpenQuests, get_js_code, getAllQuests, handle_upload
)
from app.db.createTables import create_tables_if_needed

js_code = get_js_code()

ui.add_head_html(f'''
    <script>{js_code}</script>
''')

#global variables
player_label = None

create_tables_if_needed()

# Auxilary methods: 

def delete_quest(id: int):
    if id != 0:
        delete_msg = deleteQuest(id)
        btn_edit.enabled = False
        btn_delete.enabled = False
        btn_complete.enabled = False
        return delete_msg

def complete_quest(id: int):
    if id != 0:
        complete_msg = completeQuest(id)
        btn_edit.enabled = False
        btn_delete.enabled = False
        btn_complete.enabled = False
        return complete_msg

def change_user(name: str):
    if name != '':
        changePlayer(name)
        ui.notify('Player changed')

def show_player_name_and_level():
    users = get_all_user()
    if len(users) == 0:
        return "Player: not selected"
    else:  
        for user in users:
            abc = user
            if abc[7] == 1: #if user is active
                name = abc[1]
                level = abc[5]
                return f"Player name: {name} | Level: {level}"

    return "No user is activated"

def set_profile_image_size():
    width = 75
    height = 75
    return width, height

#Pages:

@ui.page('/create_quest_page')
def create_quest_page():
    ui.label('Create quest')

    ui.label('Title:')
    name_input = ui.input() 
    
    ui.label('Description:')
    description_input = ui.input()

    ui.label('Select difficulty:')
    difficulty_select = ui.select(
        options=['Easy', 'Normal', 'Hard']
)
    
    ui.label('Select start date:')
    start_date_picker = ui.date(
    value=datetime.now().strftime('%Y-%m-%d')
    )
    ui.label('Select due date:')
    due_date_picker = ui.date(
    value=(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    )

    ui.button(
        'Create Quest',
        on_click=lambda: ui.notify(
            create_quest(
                name_input.value,
                description_input.value,
                difficulty_select.value,
                start_date_picker.value,
                due_date_picker.value
            )
        )
    )

@ui.page('/open_quests_page')
def open_quests_page():
    ui.label('Your quests:')

    quests = getAllOpenQuests()
    quest_options = []
    quest_options_menu = []

    for quest in quests:
        quest_options.append(quest)
        quest_id = quest[0]
        quest_options_menu.append(quest_id)

    quest_id = ui.select(
        options=quest_options_menu,
        on_change=lambda e: on_select_change(e.value)
    ) 

    ui.label('Title:')
    name_input = ui.input() 
    
    ui.label('Description:')
    description_input = ui.input() 

    ui.label('Select Difficulty:')
    difficulty_select = ui.select(
        options=['Easy', 'Normal', 'Hard']
    )

    ui.label('Select Start Date:')
    start_date_picker = ui.date()   
    
    ui.label('Select Due Date:')
    due_date_picker = ui.date()

    global btn_edit
    global btn_delete
    global btn_complete

    btn_edit = ui.button("edit quest")
    btn_delete = ui.button("delete quest")
    btn_complete = ui.button("complete quest")

    def on_select_change(selected_value):
        for quest in getAllOpenQuests():
            if quest[0] == selected_value:
                selected_quest = quest

        name_input.value = selected_quest[2]
        description_input.value = selected_quest[3]
        difficulty_select.value = selected_quest[4]
        start_date_picker.value = selected_quest[5]
        due_date_picker.value = selected_quest[6]

        btn_edit.on_click(lambda id=selected_quest[0]: ui.notify(pack_again(id)))
        btn_delete.on_click(lambda id=selected_quest[0]: ui.notify(handle_delete_action(id)))
        btn_complete.on_click(lambda id=selected_quest[0]: ui.notify(handle_complete_action(id)))

        if selected_quest[7] != "open":
            btn_edit.enabled = False
            btn_delete.enabled = False
            btn_complete.enabled = False
        else:
            btn_edit.enabled = True
            btn_delete.enabled = True
            btn_complete.enabled = True

    def pack_again(id: int):
        package = [None] * 7
        package[0] = id
        package[1] = "player"
        package[2] = name_input.value
        package[3] = description_input.value 
        package[4] = difficulty_select.value
        package[5] = start_date_picker.value
        package[6] = due_date_picker.value
        return editQuest(package)

    def handle_complete_action(id: int):
        complete_msg = complete_quest(id)
        return complete_msg

    def handle_delete_action(id: int):
        quest_options_menu.remove(id)
        delete_msg = delete_quest(id)
        return delete_msg

@ui.page('/see_closed_quests_page')
def see_quests_page():
    ui.label('Here are your completed quests:')
    quests = getAllCompletedQuests()

    for quest in quests:
        quest_name = quest[2]
        quest_description = quest[3]
        quest_difficulty = quest[4]
        quest_start_date = quest[5]
        quest_due_date = quest[6]

        item = (
        f"""
        Name: {quest_name},
        Description: {quest_description},
        Difficulty: {quest_difficulty}, 
        Start date: {quest_start_date}, 
        Due date: {quest_due_date}
        """)
        ui.label(item)

@ui.page('/create_user_page')
def create_user_page():
    ui.label('Create user:')

    ui.label('Name:')
    name_input = ui.input('Enter username here')

    ui.label('select image here: (under construction)')
    image_data = {}
    ui.upload(on_upload=lambda e: image_data.update({"image": handle_upload(e)}), max_files=1)

    ui.label('Select Race:')
    race_input = ui.select(
        options=['Human', 'Elf', 'Gnome']
    )

    ui.label('Select Class:')
    clas_input = ui.select(
        options=['Knight', 'Healer', 'Fighter']
    )

    level_input = 1
    xp_input = 0

    ui.button(
    'Create User',
    on_click=lambda: ui.notify(
        create_user(
            name_input.value,
            race_input.value,
            clas_input.value,
            level_input,
            xp_input,
            image_data.get("image")
        )
    )
)

@ui.page('/users_cockpit')
def see_users_page():
    ui.label('Change user:')

    users = get_all_user()
    user_options = []
    user_options_menu = []

    for user in users:
        user_options.append(user)
        user_name = user[1]
        user_options_menu.append(user_name)

    def handle_user_change(name: str):
        change_user(name)
        label_container.clear()
        with label_container:
            ui.label(show_player_name_and_level()) 

    for user in users:
        user_name = user[1]
        user_race = user[3]
        user_clas = user[4]
        user_level = user[5]
        user_xp = user[6]

        ui.label(
            f"""
            NAME: {user_name},
            RACE: {user_race}, 
            CLASS: {user_clas},
            LEVEL: {user_level},
            XP: {user_xp}
            """
        )
        ui.button(f"Make {user[1]} active", on_click=lambda user_name=user[1]: handle_user_change(user_name))

#Main page interface:

with ui.row() as label_container:
    player_label = ui.label(show_player_name_and_level())
with ui.row():
    width, height = set_profile_image_size()
    ui.image(source="app/static/Cat03.jpg").style(f"width: {width}px; height: {height}px; object-fit: cover;")

ui.button('Create quest', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_quest_page")'))
ui.button('Open quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/open_quests_page")'))
ui.button('Closed quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/see_closed_quests_page")'))
ui.button('Create user', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_user_page")'))
ui.button('Users cockpit', on_click=lambda: ui.run_javascript('openOrFocusTab("/users_cockpit")'))

# Run the app command:
ui.run()