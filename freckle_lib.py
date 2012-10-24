import requests
import json
from ConfigParser import SafeConfigParser

def print_welcome_message():
    print "\nFreckle CLI v0.1: The Luddite's Preferred Time Tracking Interface.\n"
    print "Select a project to work on. Choose wisely.\n"
    print "Loading projects..."

def get_all_projects():
    parser = SafeConfigParser()
    
    try: 
        parser.read('.freckle')
    except IOError:
        print 'Could not detect .freckle configuration file.'

    base_url = parser.get('freckle_credentials', 'base_url')
    freckle_key = parser.get('freckle_credentials', 'api_key')
    url = base_url + '/projects.json'
    
    headers = {'X-FreckleToken': freckle_key} 

    r = requests.get(url, headers=headers)
    projects = r.json

    count = 0
    
    # Include our own index in each project dictionary
    for project in projects:
        project[u'project'][u'cli_id'] = count
        count += 1

    return projects

def get_project_id():
    project_id = str(input("\nEnter Project#: "))
    
    #TODO input error checking
        
    return project_id

def print_project_menu(projects_object):
    for project in projects_object:
        print "[" + str(project[u'project'][u'cli_id']) + "] : " + str(project[u'project'][u'name'])

def get_freckle_project_id(projects_object, cli_id):
    for project in projects_object:
        if project[u'project'][u'cli_id'] == int(cli_id):
            return project[u'project'][u'id']
