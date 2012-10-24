import freckle_lib

# load all projects
all_projects = freckle_lib.get_all_projects()

freckle_lib.print_welcome_message()
freckle_lib.print_project_menu(all_projects)

# get user input for which project to work on
current_project_id = freckle_lib.get_project_id()

# store freckle project id 
freckle_project_id = freckle_lib.get_freckle_project_id(all_projects, current_project_id)
