# hiermit wird die Applikation gestartet
import app.code.quest 

from nicegui import ui
import os
import time
from datetime import datetime, timedelta

# JavaScript function to open or focus a tab
js_code = '''
function openOrFocusTab(url) {
    var tabs = window.tabs || (window.tabs = {});
    if (tabs[url]) {
        tabs[url].focus();
    } else {
        tabs[url] = window.open(url, '_blank');
        tabs[url].onbeforeunload = function() {
            delete tabs[url];
        };
    }
}
'''
#
# Inject the JavaScript function directly into the head
ui.add_head_html(f'''
    <script>{js_code}</script>
''')

@ui.page('/other_page')
def other_page():
    ui.label('Welcome to the other side')

@ui.page('/quest_page')
def quest_page():
    db_dir = 'db'
    db_path = os.path.join(db_dir, 'game.db')

    # Assuming `QuestManager` is defined in `app.code.quest`
    instance = app.code.quest.QuestManager(db_path, 1)

    ui.label('Create quest:')
    
    ui.label('Title:')
    name_input = ui.input('Enter quest title here') 
    
    ui.label('Description:')
    description_input = ui.input('Enter quest description here')

    ui.label('Select Difficulty:')
    difficulty_select = ui.select(
        options=['Easy', 'Normal', 'Hard'],
        value='Normal'
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

    def create_quest():
        # Retrieve values from input fields
        name = name_input.value
        description = description_input.value
        difficulty = difficulty_select.value

        # Convert selected dates to UNIX timestamps
        start_date = int(datetime.strptime(start_date_picker.value, '%Y-%m-%d').timestamp())
        due_date = int(datetime.strptime(due_date_picker.value, '%Y-%m-%d').timestamp())

        # Call the instance method
        instance.createQuest(
            name=name,
            description=description,
            difficulty=difficulty,
            start_date=start_date,
            due_date=due_date
        )
        ui.notify(f'Quest "{name}" created successfully!')

    ui.button('Create Quest', on_click=create_quest)



# Buttons to open or focus on the other tabs
ui.button('Some other page', on_click=lambda: ui.run_javascript('openOrFocusTab("/other_page")'))
ui.button('Quest page', on_click=lambda: ui.run_javascript('openOrFocusTab("/quest_page")'))

# Keep the main page content
ui.label('Welcome to the Home Page!')

# Run the app
ui.run()
