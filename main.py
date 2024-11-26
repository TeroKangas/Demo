from nicegui import ui

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

# Inject the JavaScript function directly into the head
ui.add_head_html(f'''
    <script>{js_code}</script>
    <link rel="stylesheet" type="text/css" href="styles.css">
''')

@ui.page('/other_page')
def other_page():
    ui.label('Welcome to the other side')

@ui.page('/dark_page', dark=True)
def dark_page():
    ui.label('Welcome to the dark side')

# Buttons to open or focus on the other tabs
ui.button('Visit other page', on_click=lambda: ui.run_javascript('openOrFocusTab("/other_page")'))
ui.button('Visit dark page', on_click=lambda: ui.run_javascript('openOrFocusTab("/dark_page")'))

# Keep the main page content
ui.label('Welcome to the Home Page!')

# Run the app
ui.run()
