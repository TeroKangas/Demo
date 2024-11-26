# hiermit wird die Applikation gestartet

from nicegui import ui
import app.code.quest 

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
    # Title label
    ui.label('Create quest:')
    
    # Input field for the quest title
    ui.label('Title:')
    quest_title = ui.input('Enter quest title here')  # Create text input field for title
    
    # Input field for quest description
    ui.label('Description:')
    quest_description = ui.input('Enter quest description here')  # Create text area for description
    
    # Button to submit quest details
    ui.button('Create Quest')  # Assuming a function `create_quest` to handle quest creation

    app.code.quest.QuestManager.createQuest()


# Buttons to open or focus on the other tabs
ui.button('Some other page', on_click=lambda: ui.run_javascript('openOrFocusTab("/other_page")'))
ui.button('Quest page', on_click=lambda: ui.run_javascript('openOrFocusTab("/quest_page")'))

# Keep the main page content
ui.label('Welcome to the Home Page!')

# Run the app
ui.run()
