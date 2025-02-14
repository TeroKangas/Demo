from datetime import datetime, timedelta  
from nicegui import ui

from app.code.createTables import create_tables_if_needed
create_tables_if_needed()

from app.utils import (
    create_quest, getAllCompletedQuests, deleteQuest, completeQuest,
    editQuest, create_user, get_all_user, change_user, getAllOpenQuests, 
    get_js_code, show_picture, show_player_name_and_level, change_picture
)

# Js engine:

js_code = get_js_code()

ui.add_head_html(f'''
    <script>{js_code}</script>
''')

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

    image_paths = [
        "app/static/Cat03.jpg",
        "app/static/cat_loafing.jpg",
        "app/static/cat_water.png"
    ]
    
    global picture_path
    picture_path = ""

    with ui.row():
        for path in image_paths:
            with ui.column():
                ui.image(path).style('width: 200px; height: 200px; border: 1px solid #ccc;')

    def on_change(e):
        global picture_path
        if e.value == "Left":
            picture_path = 'app/static/Cat03.jpg'
        elif e.value == "Center":
            picture_path = "app/static/cat_loafing.jpg"
        elif e.value == "Right":
            picture_path = "app/static/cat_water.png"
        
    ui.label("Choose your profile picture:")
    ui.radio(
    options=['Left', 'Center', 'Right'],
    on_change=on_change
    )

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
            picture_path
        )
    )
)

@ui.page('/users_cockpit')
def see_users_page():
    ui.label("Unlocked images:")

    image_paths = [
        "app/static/Cat03.jpg",
        "app/static/cat_loafing.jpg",
        "app/static/cat_water.png"
    ]

    pic_options = ["1", "2", "3"]

    users = get_all_user()
    global user_level

    for user in users:
        if user[8] == 1:
            global user_level
            user_level = user[6]

    if user_level > 2:
        image_paths.append("app/static/car.png")
        pic_options.append("4")

    if user_level > 5:
        image_paths.append("app/static/CARJPG.jpg")
        pic_options.append("5")

    global change_picture_path
    change_picture_path = ""

    with ui.row():
        for path in image_paths:
            with ui.column():
                ui.image(path).style('width: 200px; height: 200px; border: 1px solid #ccc;')

    def on_change(e):
        global change_picture_path
        if e.value == "1":
            change_picture_path = 'app/static/Cat03.jpg'
        elif e.value == "2":
            change_picture_path = "app/static/cat_loafing.jpg"
        elif e.value == "3":
            change_picture_path = "app/static/cat_water.png"
        elif e.value == "4":
            change_picture_path = "app/static/car.png"
        elif e.value == "5":
            change_picture_path = "app/static/CARJPG.jpg"

    ui.label("Change your profile picture:")
    ui.radio(
    options=pic_options,
    on_change=on_change
    )
    #on_click(lambda id=selected_quest[0]: ui.notify(pack_again(id)))
    ui.button('Change picture', on_click=lambda: ui.notify(handle_picture_change()))

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
        picture_container.clear()
        with label_container:
            ui.label(show_player_name_and_level()) 
        with picture_container:
            show_picture()

    def handle_picture_change():
        msg = change_picture(change_picture_path)
        picture_container.clear()
        with picture_container:
            show_picture()
        return msg

    for user in users:
        user_name = user[1]
        user_race = user[4]
        user_clas = user[5]
        user_level = user[6]
        user_xp = user[7]

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
with ui.row() as picture_container:
    picture_box = show_picture()

ui.button('Create quest', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_quest_page")'))
ui.button('Open quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/open_quests_page")'))
ui.button('Closed quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/see_closed_quests_page")'))
ui.button('Create user', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_user_page")'))
ui.button('Users cockpit', on_click=lambda: ui.run_javascript('openOrFocusTab("/users_cockpit")'))

# Run the app command:

ui.run()