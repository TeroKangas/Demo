# hiermit wird die Applikation gestartet
from nicegui import ui
import os
import time
from datetime import datetime, timedelta
from app.utils import create_quest, getAllOpenQuests, deleteQuest

# JavaScript function to open or focus a tab
js_code = '''
function openOrFocusTab(url) {
    var tabs = window.tabs || (window.tabs = {});
    
    // Check if the tab reference exists and is not closed
    if (tabs[url] && !tabs[url].closed) {
        tabs[url].focus();
    } else {
        // Open a new tab and store the reference
        tabs[url] = window.open(url, '_blank');
        tabs[url].onbeforeunload = function() {
            delete tabs[url];
        };
    }
}

'''

from datetime import datetime
import os



# Inject the JavaScript function directly into the head
ui.add_head_html(f'''
    <script>{js_code}</script>
''')

def delete_quest(label, id, button):
    label.style("color: gray;") 
    button.disable() 
    button.style("color: gray;")
    deleteQuest(id)

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
    
@ui.page('/see_quests_page')
def see_quests_page():
    ui.label('Here are your quests:')
    quests = getAllOpenQuests()

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
        abc = ui.label(newtext)

        delete_button = ui.button("Delete",
            on_click=lambda: delete_quest(abc, quest[0], delete_button))
        

# Buttons to open or focus on the other tabs
ui.button('Some other page', on_click=lambda: ui.run_javascript('openOrFocusTab("/other_page")'))
ui.button('Create quest', on_click=lambda: ui.run_javascript('openOrFocusTab("/create_quest_page")'))
ui.button('See quests', on_click=lambda: ui.run_javascript('openOrFocusTab("/see_quests_page")'))

# Keep the main page content
ui.label('Welcome to the Home Page!')

# Run the app
ui.run()


