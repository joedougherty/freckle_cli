import requests
import json

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

   def create_time_entry(self, entry_xml):
        url = self.base_url + '/entries.xml'
        headers = {"X-FreckleToken" : "lltpffanobj4a8yzpihmm7xan0al89s", "Content-type" : "text/xml"}
        
        files = {'file': entry_xml}

        r = requests.post(url, headers=headers, files=files) 
        return

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
