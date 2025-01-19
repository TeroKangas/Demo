
# hiermit wird die Applikation gestartet
from nicegui import ui
		 
		   
from datetime import datetime, timedelta
from app.utils import create_quest, getAllQuests, deleteQuest, completeQuest, editQuest

# Define a JavaScript function to detect tab closure
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

							 




# Inject the JavaScript function directly into the head
ui.add_head_html(f'''
    <script>{js_code}</script>
''')

#global variables
buttons_showed: bool = False
quest_id = 0
current_id = 0
btn_edit: ui.button = None
btn_delete: ui.button = None
btn_complete: ui.button = None

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
    if quest_id != 0:
        editQuest(id, name, desc, diff, start_date, due_date)
        ui.notify('Quest {id} edited')

    if id is not None and id > 0:
        editQuest(id, name, desc, diff, start_date, due_date)
        ui.notify('Quest {id} edited')
    
def delete_quest(id: int):
    if quest_id != 0:
        deleteQuest(id)
        ui.notify('Quest {id} deleted')

def complete_quest(id: int):
    if quest_id != 0:
        completeQuest(id)
        ui.notify('Quest {id} completed')

@ui.page('/other_page')
def other_page():
    ui.label('Welcome to the other side')

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

    # Calendar inputs for start_date and due_date
    ui.label('Select Start Date:')
    start_date_picker = ui.date(
        value=datetime.now().strftime('%Y-%m-%d')  # Default to today
    )
    
    ui.label('Select Due Date:')
    due_date_picker = ui.date(
        value=(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')  # Default to one week from now
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

    quests = getAllQuests()
    quest_options = []
    quest_options_menu = []
    quest_open = ""

    for quest in quests:
        quest_options.append(quest)
        quest_id = quest[0]
        quest_options_menu.append(quest_id)

    quest_id = ui.select(
        options=quest_options_menu,
        on_change=lambda e: on_select_change(quest_id.value, buttons_showed)
    ) 

    ui.label('Title:')
    name_input = ui.input() 
    
    ui.label('Description:')
    description_input = ui.input() 

    ui.label('Select Difficulty:')
    difficulty_select = ui.select(
        options=['Easy', 'Normal', 'Hard']
    )

    # Calendar inputs for start_date and due_date
    ui.label('Select Start Date:')
    start_date_picker = ui.date()
    
    ui.label('Select Due Date:')
    due_date_picker = ui.date()

    def on_select_change(selected_value, buttonbool: bool):
        selected_quest = next((quest for quest in quest_options if quest[0] == selected_value), None)
        quest_id = selected_quest[0]
        current_id = selected_quest[0]
        name_input.value = selected_quest[2]
        description_input.value = selected_quest[3]
        difficulty_select.value = selected_quest[4]
        start_date_picker.value = selected_quest[5]
        due_date_picker.value = selected_quest[6]
        quest_open = selected_quest[7]

        global btn_edit
        global btn_delete
        global btn_complete

        if ButtonManager.buttons_showed == False:
            btn_edit = ui.button("Save changes", on_click = lambda: edit_quest(selected_quest[0], name_input.value, description_input.value, difficulty_select.value, start_date_picker.value, due_date_picker.value))
            btn_delete = ui.button("Delete", on_click = lambda: delete_quest(selected_quest[0], name_input.value, description_input.value, difficulty_select.value, start_date_picker.value, due_date_picker.value))
            btn_complete = ui.button("Complete", on_click = lambda: complete_quest(selected_quest[0], name_input.value, description_input.value, difficulty_select.value, start_date_picker.value, due_date_picker.value))
            ButtonManager.buttons_showed = True

        if ButtonManager.buttons_showed == True and quest_open == 'completed':
            btn_edit.disable()
            btn_delete.disable()
            btn_complete.disable()
        if ButtonManager.buttons_showed == True and quest_open == 'open':
            btn_edit.enable()
            btn_delete.enable()
            btn_complete.enable()

@ui.page('/see_quests_page')
def see_quests_page():
    ui.label('Here are your quests:')
    quests = getAllQuests()

    for quest in quests:
        quest_description = quest[3]
        quest_difficulty = quest[4]
        quest_start_date = quest[5]
        quest_due_date = quest[6]
        quest_open = quest[7]

        newtext = (
            f"""Description: {quest_description},
        Difficulty: {quest_difficulty}, 
        Start date: {quest_start_date}, 
        Due date: {quest_due_date},
        Guest status: {quest_open}"""
        )
        ui.label(newtext)

@ui.page('/user_creation')
def user_creation():
    ui.label('Welcome to user creation')										   
																		
        
						  
					
										



# Buttons to open or focus on the other tabs
																								 
ui.button('Create quest', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_quest_page")'))
ui.button('Edit quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/edit_quest_page")'))
ui.button('User Creation', on_click=lambda: ui.run_javascript('openOrFocusTab("/user_creation")'))
																					  


							
									 

# Run the app
ui.run()


