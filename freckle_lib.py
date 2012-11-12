import requests
import json
import time
import datetime
import sys

def print_welcome_message():
    print "\nFreckle CLI v0.1: The Luddite's Preferred Time Tracking Interface."

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
        
        if r.headers['status'] == '201 Created':
            return True
        
        return False

   def get_all_users(self):
        url = self.base_url + '/users.json' 
        headers = {'X-FreckleToken': self.api_key}
       
        r = requests.get(url, headers=headers)
        all_users = r.json

        return all_users

   def extract_current_user(self, email):
        all_users_object = self.get_all_users()
        
        for users in all_users_object:
            if users[u'user'][u'email'] == email:
                return users[u'user'][u'id']
           
   def get_current_date(self):
       now = datetime.datetime.now()
       return now.strftime("%Y-%m-%d")  
   
   def get_time_spent_today(self, user):
        url = self.base_url + '/entries.json' 
        headers = {'X-FreckleToken': self.api_key}
        current_date = self.get_current_date()
        user_id = self.extract_current_user(user)

        search_params = {'search[people]' : str(user_id), 'search[from]' : current_date} 
        
        r = requests.get(url, headers=headers, params=search_params)
        all_time_entries = r.json
       
        time_spent = 0
        
        for entry in all_time_entries:
            time_spent += float(entry[u'entry'][u'minutes'])
        
        # convert minutes to hours
        time_spent = time_spent / 60
        
        return str(time_spent) + " hours logged so far today."

def get_project_id(all_projects):
    get_project_id_prompt = "\nEnter Project #: "
    project_id = raw_input(get_project_id_prompt)
    
    # get max proj num from all_projects 
    max_proj_num = all_projects[-1][u'project'][u'cli_id']
    
    valid_ids = range(0, max_proj_num + 1)
    
    # convert valid_ids to str to test against input
    valid_ids = [str(x) for x in valid_ids]

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
    
    # if user logs less than 60 seconds, round it up to one minute
    if minutes == 0:
        minutes = 1

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

def time_tracker(all_projects_object):
    print "Select a project to work on. Choose wisely.\n"
    print "Loading projects..."
    print_project_menu(all_projects_object)
    
    tracker_vals = ['start', 'stop']
    tracker_prompt = "\nEnter: \n - 'start' to start the timer \n - 'stop' to stop the timer \n: "

    # flag to maintain timer state
    start_has_fired = False

    while 1:

        tracker = str(raw_input(tracker_prompt)) 
        
        while not tracker in tracker_vals:
            print "\nPlease enter a valid command."
            tracker = str(raw_input(tracker_prompt)) 
    
        if tracker == 'start':
            if start_has_fired == False:
                print '\n*** Tracking Time ***'
                start_time = time.time()
                start_has_fired = True
            else:
                print "\nPlease only enter 'start' once."     
    
        if tracker == 'stop':
            if start_has_fired == True:
                elapsed_time = time.time() - start_time
                elapsed_time = elapsed_time/60

                print str(elapsed_time) + " minutes spent on task."
                return elapsed_time
            else:
                print "\nYou need to start tracking time first." 
