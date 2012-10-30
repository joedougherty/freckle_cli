import freckle_lib
from ConfigParser import SafeConfigParser

#open config file
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

freckle_lib.print_welcome_message()
freckle_lib.print_project_menu(all_projects)

# get user input for which project to work on
current_project_id = freckle_lib.get_project_id()

# store freckle project id 
freckle_project_id = freckle_lib.get_freckle_project_id(all_projects, current_project_id)

print freckle_project_id
