from nicegui import ui

# Include the CSS file in your template
ui.header().add_resource('<link rel="stylesheet" type="text/css" href="styles.css">')

# Define your functions for different content sections
def home_page():
    ui.label('Welcome to the Home Page!')

    for row in range(4):
        with ui.row().classes('flex-row'):
            for col in range(3):
                if row == 0 and col == 0:
                    ui.label('Row 1, Column 1').classes('size-30 bg-red')
                elif row == 0 and col == 1:
                    ui.label('Row 1, Column 2').classes('size-20 bg-green')
                elif row == 0 and col == 2:
                    ui.label('Row 1, Column 3').classes('size-50 bg-blue')
                elif row == 1 and col == 0:
                    ui.label('Row 2, Column 1').classes('size-25 bg-yellow')
                elif row == 1 and col == 1:
                    ui.button('Button in Row 2, Column 2', on_click=lambda: print('Button clicked')).classes('size-50 bg-green')
                elif row == 1 and col == 2:
                    ui.label('Row 2, Column 3').classes('size-25 bg-red')
                elif row == 2 and col == 0:
                    ui.input('Input in Row 3, Column 1').classes('size-33 bg-blue')
                elif row == 2 and col == 1:
                    ui.label('Row 3, Column 2').classes('size-34 bg-yellow')
                elif row == 2 and col == 2:
                    ui.label('Row 3, Column 3').classes('size-33 bg-green')
                elif row == 3 and col == 0:
                    ui.label('Row 4, Column 1').classes('size-20 bg-red')
                elif row == 3 and col == 1:
                    ui.label('Row 4, Column 2').classes('size-40 bg-blue')
                elif row == 3 and col == 2:
                    ui.label('Row 4, Column 3').classes('size-40 bg-yellow')

    ui.button('Go to Page 1', on_click=lambda: show_page('page_1')).classes('flex-grow bg-blue')
    ui.button('Go to Page 2', on_click=lambda: show_page('page_2')).classes('flex-grow bg-green')

def page_1():
    ui.label('You are on Page 1!')
    ui.button('Go back to Home', on_click=lambda: show_page('home')).classes('flex-grow bg-yellow')
    ui.button('Go to Page 2', on_click=lambda: show_page('page_2')).classes('flex-grow bg-blue')

def page_2():
    ui.label('You are on Page 2!')
    ui.button('Go back to Home', on_click=lambda: show_page('home')).classes('flex-grow bg-red')
    ui.button('Go to Page 1', on_click=lambda: show_page('page_1')).classes('flex-grow bg-green')

# Function to show sections
def show_page(page_name):
    # Clear the content (remove all components inside the root)
    content.clear()  # This should clear the entire UI
    
    # Show the appropriate section
    if page_name == 'home':
        home_page()
    elif page_name == 'page_1':
        page_1()
    elif page_name == 'page_2':
        page_2()

# Initialize with the home page
show_page('home')

# Run the app
ui.run()
