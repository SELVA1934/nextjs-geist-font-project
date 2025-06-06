import PySimpleGUI as sg
import json
import asyncio
import threading
from discord_cloner import ServerCloner
import logging
from datetime import datetime

# Set the theme for a modern dark look
sg.theme('DarkGrey13')

class DiscordClonerGUI:
    def __init__(self):
        self.window = None
        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {
                "bot_token": "",
                "default_source_server_id": "",
                "default_target_server_id": ""
            }

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_layout(self):
        # Header
        header = [
            [sg.Text('Discord Server Cloner', font=('Helvetica', 20), justification='center', pad=(10, 20))],
            [sg.HSep()],
        ]

        # Main content
        content = [
            [sg.Text('Bot Token:', size=(15, 1)), 
             sg.Input(self.config.get('bot_token', ''), key='-TOKEN-', password_char='*', size=(40, 1))],
            
            [sg.Text('Source Server ID:', size=(15, 1)), 
             sg.Input(self.config.get('default_source_server_id', ''), key='-SOURCE-', size=(40, 1))],
            
            [sg.Text('Target Server ID:', size=(15, 1)), 
             sg.Input(self.config.get('default_target_server_id', ''), key='-TARGET-', size=(40, 1))],
            
            [sg.HSep()],
            
            [sg.Text('Cloning Options:', font=('Helvetica', 10, 'bold'))],
            [sg.Checkbox('Clone Roles', default=True, key='-ROLES-'),
             sg.Checkbox('Clone Channels', default=True, key='-CHANNELS-'),
             sg.Checkbox('Clone Categories', default=True, key='-CATEGORIES-'),
             sg.Checkbox('Clone Emojis', default=True, key='-EMOJIS-')],
            
            [sg.HSep()],
            
            [sg.Text('Progress Log:', font=('Helvetica', 10, 'bold'))],
            [sg.Multiline(size=(60, 10), key='-LOG-', autoscroll=True, reroute_stdout=True, 
                         reroute_stderr=True, disabled=True, background_color='black')],
        ]

        # Footer with buttons
        footer = [
            [sg.Button('Start Cloning', key='-START-', size=(15, 1)),
             sg.Button('View Logs', key='-VIEWLOGS-', size=(15, 1)),
             sg.Button('Exit', key='-EXIT-', size=(15, 1))]
        ]

        return header + content + footer

    def update_log(self, message):
        if self.window:
            self.window['-LOG-'].print(f"{datetime.now().strftime('%H:%M:%S')} - {message}")

    def run_cloner(self, values):
        try:
            # Save configuration
            self.config['bot_token'] = values['-TOKEN-']
            self.config['default_source_server_id'] = values['-SOURCE-']
            self.config['default_target_server_id'] = values['-TARGET-']
            self.save_config()

            # Create and run the cloner
            cloner = ServerCloner(values['-TOKEN-'])
            
            def cloning_thread():
                asyncio.run(cloner.start_cloning(
                    values['-SOURCE-'],
                    values['-TARGET-']
                ))
                self.update_log("Cloning process completed!")
                self.window['-START-'].update(disabled=False)

            # Start cloning in a separate thread
            threading.Thread(target=cloning_thread, daemon=True).start()
            
        except Exception as e:
            self.update_log(f"Error: {str(e)}")
            self.window['-START-'].update(disabled=False)

    def run(self):
        # Create the window
        self.window = sg.Window('Discord Server Cloner', 
                              self.create_layout(),
                              finalize=True,
                              resizable=True)

        # Event Loop
        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break

            elif event == '-START-':
                # Validate inputs
                if not values['-TOKEN-']:
                    sg.popup_error('Please enter a bot token!')
                    continue
                if not values['-SOURCE-']:
                    sg.popup_error('Please enter a source server ID!')
                    continue
                if not values['-TARGET-']:
                    sg.popup_error('Please enter a target server ID!')
                    continue

                # Disable start button during cloning
                self.window['-START-'].update(disabled=True)
                self.update_log("Starting cloning process...")
                
                # Run the cloner
                self.run_cloner(values)

            elif event == '-VIEWLOGS-':
                try:
                    with open('error.log', 'r') as f:
                        log_contents = f.read()
                    sg.popup_scrolled(log_contents, title='Error Logs', size=(60, 20))
                except:
                    sg.popup_error('No log file found!')

        self.window.close()

if __name__ == '__main__':
    gui = DiscordClonerGUI()
    gui.run()
