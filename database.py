import datetime

from config import db


class Task(db.EmbeddedDocument):
	title = db.StringField(verbose_name = "Title", max_length = 255, unique = True, required = True)
	details = db.StringField(verbose_name = "Details")
	setdate = db.DateTimeField(default = datetime.datetime.now)
	lastdate = db.DateTimeField(verbose_name = "Last Date")
	completed = db.BooleanField(default = False)
	url = db.StringField(max_length = 255, unique = True)


class Project(db.Document):
	project = db.StringField(verbose_name = "Project",max_length = 255, unique = True, required = True)
	description = db.StringField(verbose_name = "Description")
	dateofcreation = db.DateTimeField(default = datetime.datetime.now)
	url = db.StringField(max_length = 255, unique = True, required = True)
	tasks = db.ListField(db.EmbeddedDocumentField('Task'))

	@property
	def completed(self):
		projectDetails =  Project.objects().get(url = self.url)
		count = 0
		for i in projectDetails.tasks:
			if i.completed == True:
				count+=1
		return count

	@property
	def remaining(self):
		projectDetails =  Project.objects().get(url = self.url)
		count = 0
		for i in projectDetails.tasks:
			if i.completed == False:
				count+=1
		return count





def create_project(projectname,projectdescription):
	if check_project(projectname)==False:
		project = Project(
		project = projectname,
		description = projectdescription,
		dateofcreation = datetime.datetime.utcnow(),
		url = projectname.replace(" ","_"),
		tasks = []
		)
		project.save()

def get_projects():
	return Project.objects.all()

def check_project(project):
	try:
		Project.objects.get(url = project)
		return True
	except db.DoesNotExist:
		return False

def project_details(project):
	projectDetails = Project.objects().get(url = project)
	return projectDetails

def project_details_recent(project):
	projectDetails = project_details(project)
	for i in range(0,len(projectDetails["tasks"])):
		if (projectDetails["tasks"][i]["setdate"] - datetime.datetime.utcnow()).days > 1:
			projectDetails["tasks"][i]=None

	return projectDetails



def project_details_completed(project):
	projectDetails = project_details(project)
	i = 0
	while i < len(projectDetails.tasks):
		if projectDetails.tasks[i].completed == False:
			del projectDetails.tasks[i]
		i+=1
	return projectDetails

def project_details_remaining(project):
	projectDetails = project_details(project)
	i = 0
	while i < len(projectDetails.tasks):
		if projectDetails.tasks[i].completed == True:
			del projectDetails.tasks[i]
		i+=1
	return projectDetails



def create_task(projectname,taskinfo):
	project = project_details(projectname)
	title = taskinfo["title"]
	details = taskinfo["description"]
	lastdate = taskinfo["last-date"]
	task = Task(
	title = title,
	details = details,
	setdate = datetime.datetime.utcnow(),
	lastdate = lastdate,
	completed = False,
	url = title.replace(" ","_")
	)
	project.tasks.append(task)
	project.save()



def editproject(project, description):
	Project.objects(url=project).update(**{'description':description})


def delete_project(project):
	Project.objects(url=project).delete()

def delete_task(project,taskDel):
	projectDesc = Project.objects(url=project).get()
	for i in range(len(projectDesc.tasks)):
		if projectDesc.tasks[i].url == taskDel:
			del projectDesc.tasks[i]
			break
	projectDesc.save()

def markcomplete(project,taskThis):
	projectDesc = Project.objects(url=project).get()
	for i in range(len(projectDesc.tasks)):
		if projectDesc.tasks[i].url == taskThis:
			projectDesc.tasks[i].completed = True
			break
	projectDesc.save()

def markremain(project,taskThis):
	projectDesc = Project.objects(url=project).get()
	for i in range(len(projectDesc.tasks)):
		if projectDesc.tasks[i].url == taskThis:
			projectDesc.tasks[i].completed = False
			break
	projectDesc.save()

def editTask(project, taskThis, newContent, newDate):
	projectDesc = Project.objects(url=project).get()
	for i in range(len(projectDesc.tasks)):
		if projectDesc.tasks[i].url == taskThis:
			projectDesc.tasks[i].details = newContent
			projectDesc.tasks[i].lastdate = newDate
			break
	projectDesc.save()
