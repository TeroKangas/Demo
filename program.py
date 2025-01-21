from nicegui import ui
from datetime import datetime, timedelta
from app.utils import create_quest, getAllOpenQuests, deleteQuest, completeQuest, editQuest, getAllCompletedQuests


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
buttons_showed: bool = False

class ButtonManager:
    def __init__(self):
        self._buttons_showed = False

    @property
    def buttons_showed(self):
        return self._buttons_showed

    @buttons_showed.setter
    def buttons_showed(self, value):
        if isinstance(value, bool):
            self._buttons_showed = value
        else:
            raise ValueError("buttons_showed must be a boolean value")

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

# Buttons to open or focus on the other tabs
ui.button('Create quest', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_quest_page")'))
ui.button('Open quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/edit_quest_page")'))
ui.button('Closed quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/see_closed_quests_page")'))

# Run the app
ui.run()