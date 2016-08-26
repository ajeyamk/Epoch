from flask.ext.api import status
from flask.ext.api import status
from flask import json,jsonify,request,Response
import model,uuid
from model import User,ProjectTable,ProjectUser,JobType,TeamType
from responseservice import ResponseClass
import requests, config
from decorators import validate_user

def convToJson(inputdata):
	data = {"data": inputdata}
	return (json.dumps(data))

def authorisation(user_id):
	user_object = User.get(User.id == user_id)
	if user_object.admin_status == True:
		return True
	else:
		return False

def getIssues():
	issue_list = []
	for issue in JobType.select():
		issueobj = {}
		issueobj['jobtype'] = issue.jobtype
		issueobj['jobtype_id'] = issue.id
		issue_list.append(issueobj)
	obj = convToJson(issue_list)
	client_response = Response(obj, mimetype='application/json')
	return client_response,status.HTTP_200_OK
	
def getTeams():
	team_list = []
	for team in TeamType.select():
		teamobj = {}
		teamobj['teamtype'] = team.team_type
		teamobj['teamtype_id'] = team.id
		team_list.append(teamobj)
	obj = convToJson(team_list)
	client_response = Response(obj, mimetype='application/json')
	return client_response,status.HTTP_200_OK


def createProject():
	return_response = validate_user()
	return_data = json.loads(return_response.text)
	if return_response.status_code == 200:
		authority = authorisation(return_data['User_id'])
		if authority:
			data = request.json
			if ProjectTable.select().where((ProjectTable.name == data['name']) & (ProjectTable.date_start == data['date_start']) & (ProjectTable.date_end == data['date_end'])).exists():
				message = ResponseClass.project_existing.value
				obj = ResponseClass.creationerror_message(message)
				client_response = Response(obj, mimetype='application/json')
				return client_response,status.HTTP_400_BAD_REQUEST
			else:
				proj_data = {'name':data['name'],'description':data['description'],'date_start':data['date_start'],'date_end':data['date_end']}	
				proj_object = ProjectTable(**proj_data)
				proj_object.save()
				team_member_data = data['team_member']
				for member in team_member_data:
					team_member_object = {}
					team_member_object['project'] = proj_object.id
					team_member_object['team_member'] = member
					team_member_object['team_lead'] = 1
					save_object = ProjectUser(**team_member_object)
					save_object.save()
				message = {'name':data['name'],'description':data['description']}
				obj = ResponseClass.creationsuccess_message(message)
				client_response = Response(obj, mimetype='application/json')
				return client_response,status.HTTP_201_CREATED
		else:
			client_message = ResponseClass.authority_exception.value
			obj = ResponseClass.creationerror_message(client_message)
			client_response = Response(obj, mimetype='application/json')
			return client_response,status.HTTP_400_BAD_REQUEST
	else:
		obj = json.dumps(return_data)
		ret_status = return_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,ret_status
	

def getProjects():
	return_response = validate_user()
	data = json.loads(return_response.text)
	if return_response.status_code == 200:
		proj_query = ProjectTable.select().join(ProjectUser).order_by(-ProjectTable.created_at).where(ProjectUser.team_member == data['User_id'])
		if proj_query.exists():
			project_list=[]
			for proj in proj_query:
				projobj = {}
				projobj['title'] = proj.name
				projobj['description'] = proj.description
				projobj['created time'] = proj.created_at
				projobj['proj_id'] = proj.id
				project_list.append(projobj)
			obj = convToJson(project_list)
			client_response = Response(obj, mimetype='application/json')		
			return client_response,status.HTTP_200_OK
		else:
			client_message = ResponseClass.notes_absent.value
			obj = ResponseClass.creationerror_message(client_message)
			client_response = Response(obj, mimetype='application/json')
			return client_response,status.HTTP_404_NOT_FOUND
	else:
		obj = json.dumps(data)
		ret_status = return_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,ret_status
	

def getAllProjects():
	return_response = validate_user()
	data = json.loads(return_response.text)
	if return_response.status_code == 200:
		authority = authorisation(data['User_id'])
		if authority:
			proj_query = ProjectTable.select()
			project_list=[]
			for proj in proj_query:
				projobj = {}
				projobj['title'] = proj.name
				projobj['description'] = proj.description
				projobj['created time'] = proj.created_at
				projobj['proj_id'] = proj.id
				project_list.append(projobj)
			obj = convToJson(project_list)
			resp = Response(obj, mimetype='application/json')
			return resp,status.HTTP_200_OK
		else:
			client_message = ResponseClass.authority_exception.value
			obj = ResponseClass.creationerror_message(client_message)
			client_response = Response(obj, mimetype='application/json')
			return client_response,status.HTTP_400_BAD_REQUEST
	else:
		obj = json.dumps(data)
		ret_status = return_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,ret_status
	
def temp():
	try:
		data = request.json
		if ProjectTable.select().where((ProjectTable.name == data['name']) & (ProjectTable.date_start == data['date_start']) & (ProjectTable.date_end == data['date_end'])).exists():
			message = ResponseClass.project_existing.value
			obj = ResponseClass.creationerror_message(message)
			client_response = Response(obj, mimetype='application/json')
			return client_response,status.HTTP_400_BAD_REQUEST
		else:
			proj_data = {'name':data['name'],'description':data['description'],'date_start':data['date_start'],'date_end':data['date_end'],'project_manager':data['project_manager']}	
			proj_object = ProjectTable(**proj_data)
			proj_object.save()
			team_member_data = data['team_member']
			project_lead_data = data['project_lead']
			for member in team_member_data:
				team_member_object = {}
				team_member_object['project'] = proj_object.id
				team_member_object['team_type'] = member.team_type
				team_member_array = member.members_id
				for members in team_member_array:
					team_member_array_object = {}
					team_member_array_object['team_member'] = members
				team_member_object.append(team_member_array_object)
				save_team_member_object = ProjectUser(**team_member_object)
				save_team_member_object.save()
			for lead in project_lead_data:
				team_lead_object = {}
				team_lead_object['project'] = lead.id
				team_lead_object['team_type'] = lead.team_type
				team_lead_object['team_lead'] = lead.lead_id
			save_project_lead_object = ProjectLead(**team_lead_object)
			save_project_lead_object.save()
			message = {'name':data['name'],'description':data['description']}
			obj = ResponseClass.creationsuccess_message(message)
			client_response = Response(obj, mimetype='application/json')
			return client_response,status.HTTP_201_CREATED
	except Exception as e:
		print(e)
