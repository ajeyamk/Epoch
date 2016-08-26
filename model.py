import peewee as pw
from flask import Flask
import datetime
from peewee import *
from playhouse.migrate import *

myDB = pw.MySQLDatabase("myDB", host="localhost", port=3306, user="root", passwd="tempyml")
migrator = MySQLMigrator(myDB)
class MySQLModel(pw.Model):
	class Meta:
		database = myDB

class TeamType(MySQLModel):
	team_type = pw.CharField()
	def __init__(self,**kwargs):
		super(TeamType, self).__init__()
		self.team_type = kwargs.get('team_type')

class User(MySQLModel):
	team_type =  pw.ForeignKeyField(TeamType)
	username = pw.CharField(max_length=40)
	email = pw.CharField(max_length=60,default =0)
	password = pw.CharField(max_length=50,default =0)
	designation = pw.TextField()
	created_at = pw.DateTimeField(default = datetime.datetime.now)
	modified_date = pw.DateTimeField(default = datetime.datetime.now)
	admin_status = pw.BooleanField(default =False )
	def __init__(self,**kwargs):
		super(User, self).__init__()
		self.username = kwargs.get('username')
		self.designation = kwargs.get('designation')
		self.team_type = kwargs.get('team_type')

class ProjectTable(MySQLModel):
	name = pw.CharField(max_length=60, unique=True)
	description = pw.TextField()
# Extra columns for datetime in charfield
	ext_date_start = pw.CharField()
	ext_date_end = pw.CharField()
# Original date time fields	
	date_start = pw.DateField()
	date_end = pw.DateField()
# ---------------------------------
	created_at = pw.DateTimeField(default = datetime.datetime.now)
	modified_date = pw.DateTimeField(default = datetime.datetime.now)
	project_manager = pw.ForeignKeyField(User)
	def __init__(self,**kwargs):
		super(ProjectTable, self).__init__()
		self.name = kwargs.get('name')
		self.description = kwargs.get('description')
# Extra columns for datetime in charfield
		self.ext_date_start = kwargs.get('date_start')
		self.ext_date_end = kwargs.get('date_end')
# Original date time fields		
		# self.ext_date_start = kwargs.get('date_start')
		# self.ext_date_end = kwargs.get('date_end')
		self.project_manager = kwargs.get('project_manager')

class ProjectUser(MySQLModel):
	project = pw.ForeignKeyField(ProjectTable)
	team_type =  pw.ForeignKeyField(TeamType)
	team_member = pw.ForeignKeyField(User)
	created_at = pw.DateTimeField(default = datetime.datetime.now)
	modified_date = pw.DateTimeField(default = datetime.datetime.now)
	def __init__(self,**kwargs):
		super(ProjectUser, self).__init__()
		self.project = kwargs.get('project')
		self.team_member = kwargs.get('team_member') 
		self.team_lead = kwargs.get('team_lead')
		self.team_type = kwargs.get('team_type')

class JobType(MySQLModel):
	jobtype = pw.TextField()
	def __init__(self,**kwargs):
		super(JobType, self).__init__()
		self.jobtype = kwargs.get('jobtype')

class ProjectLead(MySQLModel):
	project = pw.ForeignKeyField(ProjectTable)
	team_type =  pw.ForeignKeyField(TeamType)
	team_lead = pw.ForeignKeyField(User)
	created_at = pw.DateTimeField(default = datetime.datetime.now)
	modified_date = pw.DateTimeField(default = datetime.datetime.now)
	def __init__(self,**kwargs):
		super(ProjectLead, self).__init__()
		self.project = kwargs.get('project')
		self.team_type = kwargs.get('team_type')
		self.team_lead = kwargs.get('team_lead')

class LogTable(MySQLModel):
	project = pw.ForeignKeyField(ProjectTable)
	user = pw.ForeignKeyField(User)
	job_type = pw.ForeignKeyField(JobType)
	team_type =  pw.ForeignKeyField(TeamType)
	description = pw.TextField()
	logged_date = pw.CharField()
	log_hours = pw.IntegerField(default = 0)
	logged_time = pw.DateTimeField(default = datetime.datetime.now)
	modified_date = pw.DateTimeField(default = datetime.datetime.now)
	def __init__(self,**kwargs):
		super(LogTable, self).__init__()
		self.project = kwargs.get('project')
		self.user = kwargs.get('user')
		self.description = kwargs.get('description')
		self.logged_date = kwargs.get('logged_date')
		self.job_type = kwargs.get('job_type')
		self.logged_hours = kwargs.get('logged_hours')
		self.log_hours = kwargs.get('logged_hours')
		self.team_type = kwargs.get('team_type')

# class SessionTable(MySQLModel):
# 	user = pw.ForeignKeyField(User)
# session_ID = pw.CharField(default= 0)
# 	created_date = pw.DateTimeField(default = datetime.datetime.now)
# 	def __init__(self,**kwargs):
# 		super(SessionTable, self).__init__()
# 		self.user = kwargs.get('user')
# 		self.session_ID = kwargs.get('session_ID')
# modified_date_field = pw.DateTimeField(default = datetime.datetime.now)
myDB.connect()

# myDB.create_tables([TeamType,LogTable,JobType,ProjectUser,ProjectTable,User,ProjectLead])
# status_field = pw.IntegerField(default = 0)
# # status_field = pw.ForeignKeyField(TeamType, default = 0, to_field = 'teamtype.id')
# with myDB.transaction():
#   	migrate(
#   		 migrator.add_column('projecttable', 'ext_date_start', session_ID),
  		 
#   		 migrator.add_column('projecttable', 'ext_date_end', session_ID)
#   		 )
# # 		 migrator.add_column('projectuser', 'team_type',status_field)
# )


# obj= User(first_name = 'jon',last_name ='snow',username = 'johnny',password = 'gameee',email ='jon@snow.com',designation = 'senior software engineer',phone_number = '+91 1478523690')
# obj.save()