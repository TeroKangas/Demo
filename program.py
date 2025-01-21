from nicegui import ui
from datetime import datetime, timedelta
from app.utils import create_quest, getAllCompletedQuests, deleteQuest, completeQuest, editQuest, create_user, update_user, get_all_user, delete_user, changePlayer, getAllOpenQuests
from app.db.createTables import create_tables_if_needed

js_code = '''
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

ui.add_head_html(f'''
    <script>{js_code}</script>
''')

#global variables
#buttons_showed_open_quests: bool = False
player_label = None

create_tables_if_needed()

class ButtonManager:
    def __init__(self):
        self._buttons_showed_open_quests = False
        self._buttons_showed_player_cockpit = False
        self.player_label: str

    @property
    def buttons_showed(self):
        return self._buttons_showed_open_quests

    @buttons_showed.setter
    def buttons_showed(self, value):
        if isinstance(value, bool):
            self._buttons_showed_open_quests = value
        else:
            raise ValueError("buttons_showed must be a boolean value")
        
    @property
    def buttons_showed_player_cockpit(self):
        return self._buttons_showed_player_cockpit

    @buttons_showed.setter
    def buttons_showed_player_cockpit(self, value):
        if isinstance(value, bool):
            self._buttons_showed_player_cockpit = value
        else:
            raise ValueError("_buttons_showed_player_cockpit must be a boolean value")

def edit_quest(id: int, name: str, desc: str, diff: str, start_date, due_date):
    if id is not None and id > 0:
        if name != '' and desc != '':
            editQuest(id, name, desc, diff, start_date, due_date)
            ui.notify('Quest edited')
        else:
            ui.notify('Title and description must be given.')
    
def delete_quest(id: int):
    if id != 0:
        deleteQuest(id)
        ui.notify('Quest deleted')
        btn_edit.enabled = False
        btn_delete.enabled = False
        btn_complete.enabled = False

def complete_quest(id: int):
    if id != 0:
        completeQuest(id)
        ui.notify('Quest completed')
        btn_edit.enabled = False
        btn_delete.enabled = False
        btn_complete.enabled = False

def change_user(name: str):
    if name != '':
        changePlayer(name)
        ui.notify('Player changed')

@ui.page('/create_quest_page')
def quest_page():
    ui.label('Create quest:')
    
    ui.label('Title:')
    name_input = ui.input('Enter quest title here') 
    
    ui.label('Description:')
    description_input = ui.input('Enter quest description here')

    ui.label('Select Difficulty:')
    difficulty_select = ui.select(
        options=['Easy', 'Normal', 'Hard']
    )

    ui.label('Select Start Date:')
    start_date_picker = ui.date(
        value=datetime.now().strftime('%Y-%m-%d')
    )
    
    ui.label('Select Due Date:')
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

@ui.page('/edit_quest_page')
def edit_page():
    ui.label('Your quests:')
    ButtonManager.buttons_showed = False

    quests = getAllOpenQuests()
    quest_options = []
    quest_options_menu = []

    for quest in quests:
        quest_options.append(quest)
        quest_id = quest[0]
        quest_options_menu.append(quest_id)

    quest_id = ui.select(
        options=quest_options_menu,
        on_change=lambda e: on_select_change(quest_id.value)
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

    def on_select_change(selected_value):
        selected_quest = next((quest for quest in quest_options if quest[0] == selected_value), None)
        name_input.value = selected_quest[2]
        description_input.value = selected_quest[3]
        difficulty_select.value = selected_quest[4]
        start_date_picker.value = selected_quest[5]
        due_date_picker.value = selected_quest[6]

        global btn_edit
        global btn_delete
        global btn_complete

        if ButtonManager.buttons_showed == False:
            btn_edit = ui.button("Save changes", on_click = lambda: edit_quest(selected_quest[0], name_input.value, description_input.value, difficulty_select.value, start_date_picker.value, due_date_picker.value))
            btn_delete = ui.button("Delete", on_click = lambda: handle_delete_action(selected_quest[0]))
            btn_complete = ui.button("Complete", on_click = lambda: handle_complete_action(selected_quest[0]))
            ButtonManager.buttons_showed = True

        if ButtonManager.buttons_showed == True:
            btn_edit.enabled = True
            btn_delete.enabled = True
            btn_complete.enabled = True

    def handle_complete_action(id: int):
        complete_quest(id)
        quest_options_menu.remove(id)

    def handle_delete_action(id: int):
        delete_quest(id)
        quest_options_menu.remove(id)

@ui.page('/see_closed_quests_page')
def see_quests_page():
    ui.label('Here are your completed quests:')
    quests = getAllCompletedQuests()

    for quest in quests:
        quest_description = quest[3]
        quest_difficulty = quest[4]
        quest_start_date = quest[5]
        quest_due_date = quest[6]

        item = (
        f"""Description: {quest_description},
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

    ui.label('select image here:')
    image_path_input = ui.input('Enter image here !!!DAS WIRD SPÄTER NOCH GEÄNDERT!!!')

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
            image_path_input.value,
            race_input.value,
            clas_input.value,
            level_input,
            xp_input
        )
    )
)

@ui.page('/edit_user')
def edit_page():
    ui.label('Your users:')
    ButtonManager.buttons_showed = False

    users = get_all_user()
    user_options = []
    user_options_menu = []

    for user in users:
        user_options.append(user)
        user_id = user[0]
        user_options_menu.append(user_id)

    user_id = ui.select(
        options=user_options_menu,
        on_change=lambda e: on_select_change(user_id.value, ButtonManager.buttons_showed)
    )

    ui.label('Name:')
    name_input = ui.input()

    ui.label('Image Path:')
    image_path_input = ui.input()

    ui.label('Race:')
    race_input = ui.select(
        options=['Human', 'Elf', 'Gnome']
    )

    ui.label('Class:')
    clas_input = ui.select(
        options=['Knight', 'Healer', 'Fighter']
    )

    def on_select_change(selected_value, buttonbool: bool):
        selected_user = next((user for user in user_options if user[0] == selected_value), None)
        user_id = selected_user[0]
        current_id = selected_user[0]
        name_input.value = selected_user[1]
        image_path_input.value = selected_user[2] if selected_user[2] else ""
        race_input.value = selected_user[3] if selected_user[3] else "noRace"
        clas_input.value = selected_user[4] if selected_user[4] else "noClass"

        global btn_edit
        global btn_delete

        if not ButtonManager.buttons_showed:
            btn_edit = ui.button("Save changes", on_click=lambda: ui.notify(update_user(
                selected_user[0], name_input.value, image_path_input.value, race_input.value,
                clas_input.value
            )))
            btn_delete = ui.button("Delete", on_click=lambda: ui.notify(delete_user(
                selected_user[0]
            )))
            ButtonManager.buttons_showed = True

@ui.page('/users_cockpit')
def see_users_page():
    ui.label('Change user:')

    ButtonManager.buttons_showed_player_cockpit = False

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
            ui.label(show_player())        

    def on_select_change(event):
        global user_name
        user_name = event.value

        selected_player = next((user for user in user_options if user[1] == user_name), None)

        global btn_change_player
        if not ButtonManager.buttons_showed_player_cockpit:
            btn_change_player = ui.button("Save change", on_click=lambda: handle_user_change(selected_player[1]))
            ButtonManager.buttons_showed_player_cockpit = True

        if ButtonManager.buttons_showed_player_cockpit:
            btn_change_player.enabled = True

        label_container.clear()
        with label_container:
            ui.label(show_player())
    
    ui.select(
        options=user_options_menu,
        on_change=on_select_change
    )

    ui.label('Here are your users:')
    users = get_all_user()

    for user in users:
        user_id = user[0]
        user_name = user[1]
        user_image_path = user[2]
        user_race = user[3]
        user_clas = user[4]
        user_level = user[5]
        user_xp = user[6]
        user_active = user[7]

        newtext = (
            f"""
        id: {user_id},
        name: {user_name},
        image_path: {user_image_path}, 
        race: {user_race}, 
        clas: {user_clas},
        level: {user_level}
        xp: {user_xp},
        active: {user_active},
        """
        )
        ui.label(newtext)

def show_player():
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

with ui.row() as label_container:
    player_label = ui.label(show_player())
# Buttons to open or focus on the other tabs
ui.button('Create quest', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_quest_page")'))
ui.button('Open quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/edit_quest_page")'))
ui.button('Closed quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/see_closed_quests_page")'))
ui.button('Create user', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_user_page")'))
#ui.button('Edit User', on_click=lambda: ui.run_javascript('openOrFocusTab("/edit_user")'))
ui.button('Users cockpit', on_click=lambda: ui.run_javascript('openOrFocusTab("/users_cockpit")'))

# Run the app
ui.run()