import freckle_lib
from ConfigParser import SafeConfigParser
import os
import sys
import argparse

class Text_Command(object):
    def __init__(self, arg1, arg2):
        self.name = arg1 
        self.description = arg2

all_valid_commands = []

all_valid_commands.append( Text_Command('howmuch', "'howmuch' to see time logged so far today") )
all_valid_commands.append( Text_Command('timer', "'timer' to access timer function") )
all_valid_commands.append( Text_Command('quit', "'quit' to quit and exit") )

def freckle_init(all_projects_object, api_object, user):
    parser = argparse.ArgumentParser(description='Get tracked time')
    parser.add_argument("--total", help="return total time tracked today (in hrs)", action="store_true")
    args = parser.parse_args()

    if args.total:
        hrs = api_object.get_time_spent_today(user)
        hrs = hrs.split(" ")
        print hrs[0]                     
        sys.exit()
        
def main_menu(all_projects_object, api_object, user):

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
            freckle_lib.time_tracker(all_projects_object, user, api_object)
            main_menu_input = str(raw_input(main_menu_prompt)) 
    
    sys.exit()

# open config file
parser = SafeConfigParser()
parser.read('/home/joe/.freckle')

# Connection details
base_url = parser.get('freckle_credentials', 'base_url') 

# User details
api_key  = parser.get('freckle_credentials', 'api_key')
user     = parser.get('freckle_credentials', 'user')

api_object = freckle_lib.FreckleApi(base_url, api_key)

# load all projects
all_projects = api_object.get_all_projects()

# check if freckle was called with optional params
freckle_init(all_projects, api_object, user)

# print welcome message
freckle_lib.print_welcome_message()

# main menu
main_menu(all_projects, api_object, user)
