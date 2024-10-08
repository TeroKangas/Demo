from nicegui import ui
import webbrowser
import sys

# Define the behavior for the exit button
def exit_app():
    # Show a message to inform the user to close the window manually
    ui.label('Thank you for using the app! Please close this window.')
    # Optionally, you can hide the exit button after clicking
    exit_button.visible = False

# Create the GUI
ui.label('Welcome')

# Button to exit the app
exit_button = ui.button('Exit', on_click=exit_app)

# Function to open the app in the default web browser
def open_in_browser():
    webbrowser.open('http://localhost:8080')  # Open in default browser (Edge)

# Run the NiceGUI application
ui.run()

# After starting the application, open the browser
open_in_browser()
