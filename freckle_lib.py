import requests
import json
import time
import datetime

def print_welcome_message():
    print "\nFreckle CLI v0.1: The Luddite's Preferred Time Tracking Interface.\n"
    print "Select a project to work on. Choose wisely.\n"
    print "Loading projects..."

class FreckleApi(object):
   def __init__(self, arg1, arg2):
        self.base_url = arg1 
        self.api_key  = arg2

   def get_all_projects(self):
        url = self.base_url + '/projects.json'
        headers = {'X-FreckleToken': self.api_key} 

        r = requests.get(url, headers=headers)
        projects = r.json

        count = 0
    
        # Include our own index in each project dictionary
        for project in projects:
            project[u'project'][u'cli_id'] = count
            count += 1

        return projects

   def create_time_entry(self, xml_entry):
        url = self.base_url + '/entries.xml'
        headers = {"X-FreckleToken" : self.api_key, "Content-type" : "text/xml"}
        
        files = {'file': xml_entry}

        r = requests.post(url, headers=headers, files=files) 
        return

def get_project_id(all_projects):
    get_project_id_prompt = "\nEnter Project #: "
    project_id = raw_input(get_project_id_prompt)
    
    # get max proj num from all_projects 
    max_proj_num = all_projects[-1][u'project'][u'cli_id']
    
    valid_ids = range(0, max_proj_num + 1)

    while project_id not in valid_ids:
        print "Your input should be a number between 0 and " + str(max_proj_num)
        project_id = raw_input(get_project_id_prompt)

    return project_id

def print_project_menu(projects_object):
    for project in projects_object:
        print "[" + str(project[u'project'][u'cli_id']) + "] : " + str(project[u'project'][u'name'])

def get_freckle_project_id(projects_object, cli_id):
    for project in projects_object:
        if project[u'project'][u'cli_id'] == int(cli_id):
            return project[u'project'][u'id']

def generate_xml_post(minutes, user, project_num, tags='development'):    
    minutes = int(minutes)
    # convert back to str and append 'm'
    minutes = str(minutes) + 'm' 
    project_num = str(project_num)

    xml_post = '''
                <?xml version="1.0" encoding="UTF-8"?>
                    <entry>
                        <minutes>''' + minutes + '''</minutes>
                        <user>''' + user + '''</user>
                        <project-id type="integer">''' + project_num  + '''</project-id>
                        <description>''' + tags + '''</description>
                    </entry>
                '''
    return xml_post
    
def time_tracker():

    tracker_vals = ['start', 'stop']
    tracker_prompt = "Enter 'start' to start the timer and 'stop' to stop the timer:"

    while 1:
        tracker = str(raw_input(tracker_prompt)) 

        while not tracker in tracker_vals:
            print "Please enter either 'start' or 'stop'."
            tracker = str(raw_input(tracker_prompt)) 
    
        if tracker == 'start':
            print 'Tracking time...'
            start_time = time.time()
    
        if tracker == 'stop':
            elapsed_time = time.time() - start_time
            elapsed_time = elapsed_time/60

            print str(elapsed_time) + " minutes spent on task."
            return elapsed_time              
