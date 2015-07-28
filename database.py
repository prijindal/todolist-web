from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.todo

tasks = db.tasks

def create_project(projectname,projectdescription):
	if check_project(projectname)==False:
		projectInfo = {
		"project" : projectname,
		"description" : projectdescription,
		"dateofcreation" : datetime.utcnow(),
		"url" : projectname.replace(" ","_"),
		"tasks" : []
		}
		tasks.insert_one(projectInfo)

def get_projects():
	allProjects = []
	for project in tasks.find():
		completed=0
		remaining = 0
		for task in project["tasks"]:
			if task['completed']:
				completed+=1
			else:
				remaining+=1
		project["completed"] = completed
		project["remaining"] = remaining
		allProjects.append(project)
	return allProjects

def check_project(project):
	if tasks.find_one({"project":project}):
		return True
	else:
		return False

def project_details(project):
	projectDetails = tasks.find_one({"url":project})
	completed=0
	remaining = 0
	if projectDetails:
		for task in projectDetails["tasks"]:
			if task['completed']:
				completed+=1
			else:
				remaining+=1
		projectDetails["completed"] = completed
		projectDetails["remaining"] = remaining
	return projectDetails

def create_task(projectname,taskinfo):
	previousTasks = tasks.find_one({"project":projectname})["tasks"]
	title = taskinfo["title"]
	details = taskinfo["description"]
	lastdate = taskinfo["last-date"]
	taskinfo = {
	"title" : title,
	"details" : details,
	"setdate" : datetime.utcnow(),
	"lastdate" : lastdate,
	"completed" : False,
	"url" : title.replace(" ","_")
	}
	previousTasks.append(taskinfo)
	tasks.update({"project":projectname},{'$set': {"tasks":previousTasks}})

def project_details_all(project):
	projectDetails = project_details(project)
	return projectDetails

def project_details_recent(project):
	projectDetails = project_details(project)
	for i in range(0,len(projectDetails["tasks"])):
		if (projectDetails["tasks"][i]["setdate"] - datetime.utcnow()).days > 1:
			projectDetails["tasks"][i]=None

	return projectDetails

def editproject(project, description):
	projectDetails = project_details(project)
	projectDetails['description'] = description
	tasks.update({"url":project},projectDetails)

def project_details_completed(project):
	projectDetails = project_details(project)
	for i in range(0,len(projectDetails["tasks"])):
		if projectDetails["tasks"][i]["completed"]==False:
			projectDetails["tasks"][i]=None

	return projectDetails

def project_details_remaining(project):
	projectDetails = project_details(project)
	for i in range(0,len(projectDetails["tasks"])):
		if projectDetails["tasks"][i]["completed"]==True:
			projectDetails["tasks"][i]=None

	return projectDetails


def delete_project(project):
	db.tasks.remove({'url':project})

def delete_task(project,taskDel):
	projectDetails = project_details_all(project)
	newTask = []
	for task in projectDetails['tasks']:
		if task['url'] != taskDel:
			newTask.append(task)
	projectDetails['tasks']=newTask
	tasks.update({"url":project},projectDetails)

def markcomplete(project,taskThis):
	projectDetails = project_details_all(project)
	newTask = []
	for task in projectDetails['tasks']:
		if task['url'] == taskThis:
			task['completed'] = True
		newTask.append(task)
	projectDetails['tasks']=newTask
	tasks.update({"url":project},projectDetails)

def markremain(project,taskThis):
	projectDetails = project_details_all(project)
	newTask = []
	for task in projectDetails['tasks']:
		if task['url'] == taskThis:
			task['completed'] = False
		newTask.append(task)
	projectDetails['tasks']=newTask
	tasks.update({"url":project},projectDetails)

def editTask(project, taskThis, newContent, newDate):
	projectDetails = project_details_all(project)
	newTask = []
	for task in projectDetails['tasks']:
		if task['url'] == taskThis:
			task['details'] = newContent
			task['lastdate'] = newDate
		newTask.append(task)
	projectDetails['tasks']=newTask
	tasks.update({"url":project},projectDetails)
