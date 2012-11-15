import freckle_lib
from ConfigParser import SafeConfigParser
import os
import sys

class Text_Command(object):
    def __init__(self, arg1, arg2):
        self.name = arg1 
        self.description = arg2

all_valid_commands = []

all_valid_commands.append( Text_Command('howmuch', "'howmuch' to see time logged so far today") )
all_valid_commands.append( Text_Command('timer', "'timer' to access timer function") )
all_valid_commands.append( Text_Command('quit', "'quit' to quit and exit") )

def main_menu_input(all_projects_object, api_object, user):

    valid_inputs = []
    main_menu_prompt = "\nEnter: "

    for commands in all_valid_commands:
        # populate the valid inputs list
        valid_inputs.append( commands.name )

        # build the commands menu
        main_menu_prompt += "\n - " + commands.description

    main_menu_prompt += "\n : "

    main_menu_input = str(raw_input(main_menu_prompt)) 
    
    while not main_menu_input == 'quit':
        
        while not main_menu_input in valid_inputs:
            print "\nPlease enter a valid command."
            main_menu_input = str(raw_input(main_menu_prompt)) 
    
        if main_menu_input == 'howmuch':
            print api_object.get_time_spent_today(user)                     
            main_menu_input = str(raw_input(main_menu_prompt)) 
        
        if main_menu_input == 'timer':
            freckle_lib.time_tracker(all_projects_object)
            main_menu_input = str(raw_input(main_menu_prompt)) 
    
    sys.exit()

# open config file
parser = SafeConfigParser()
parser.read('.freckle')

# Connection details
base_url = parser.get('freckle_credentials', 'base_url') 

# User details
api_key  = parser.get('freckle_credentials', 'api_key')
user     = parser.get('freckle_credentials', 'user')

api_object = freckle_lib.FreckleApi(base_url, api_key)

# load all projects
all_projects = api_object.get_all_projects()

# welcome message
freckle_lib.print_welcome_message()

# main menu
main_menu_input(all_projects, api_object, user)

# store freckle project id 
freckle_project_id = freckle_lib.get_freckle_project_id(all_projects, current_project_id)

# create the time entry we'll pass to api_object
time_entry = freckle_lib.generate_xml_post(time_spent, user, freckle_project_id) 

# make post request
if api_object.create_time_entry(time_entry):
    print "New time entry has been created."
else:
    print "Service could not be reached."

