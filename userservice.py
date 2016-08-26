from flask.ext.api import status
from flask import json,jsonify,request,Response
import model,uuid
from model import User,TeamType
from responseservice import ResponseClass
import requests,config
from projectservice import authorisation
from decorators import validate_user

def convToJson(inputdata):
	data = {"data": inputdata}
	return (json.dumps(data))

def login():
	data = request.json
	url = config.EXT_API_SIGN_IN
	delegate_data = {'Unique_field': data['email'], 'Password' : data['password']}
	headers = {'Content-Type' : 'application/json'}
	ext_response = requests.post(url, data = json.dumps(delegate_data), headers=headers)
	return_data = json.loads(ext_response.text)
	if ext_response.status_code == 200:
		user = User.get(User.id == return_data['User_id']) 
		return_response = {'admin_status':user.admin_status,'session_ID' :return_data['Session_token'], 'username' : user.username}
		obj = convToJson(return_response) 
		status = ext_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,status
	else:
		obj = json.dumps(return_data)
		ret_status = ext_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,ret_status	
	
def signup():
	data = request.json
	url = config.EXT_API_SIGN_UP
	delegate_data = {'Unique_field': data['email'], 'Password' : data['password']}
	headers = {'Content-Type' : 'application/json'}
	result = requests.post(url, data = json.dumps(delegate_data), headers=headers)
	if result.status_code == 201:
		return_data = json.loads(result.text)
			# data['ext_user_id']= return_data['User_id']
		saveobject = User(**data)
		saveobject.save()
		status = result.status_code
		obj = json.dumps(return_data)
		client_response = Response(obj, mimetype='application/json')
		return client_response,status
	else:
		return_data = json.loads(result.text)
		status = result.status_code
		obj = json.dumps(return_data)
		client_response = Response(obj, mimetype='application/json')
		return client_response,status
			
def logout():
	reqheader = request.headers.get('User_token')
	if (reqheader == None):
		message = ResponseClass.invalid_token.value
		response = ResponseClass.creationerror_message(message)
		return response,status.HTTP_400_BAD_REQUEST
	else:
		data = request.json
		url = config.EXT_API_LOGOUT
		headers = {'Session_token': reqheader}
		return_response = requests.delete(url, headers=headers)
		message = json.loads(return_response.text)
		status = return_response.status_code
		obj = json.dumps(message)
		client_response = Response(obj, mimetype='application/json')
		return client_response,status
	
def edit_password():
	reqheader = request.headers.get('User_token')
	url = config.EXT_API_CHANGE_PASSWORD
	req_data = request.json
	header = {'Content-Type' : 'application/json', 'Session_token': reqheader }
	del_data = {'Old_Password':req_data['old_password'], 'New_Password':req_data['new_password']}
	result = requests.post(url, data= json.dumps(del_data), headers=header)
	message = json.loads(result.text)
	status = result.status_code
	obj = json.dumps(message)
	client_response = Response(obj, mimetype='application/json')
	return client_response,status
		
def getUsers():
	return_response = validate_user()
	data = json.loads(return_response.text)
	if return_response.status_code == 200:
		authority = authorisation(data['User_id'])
		if authority:
			user_list = []
			for user in User.select():
				userobj = {}
				userobj['username'] = user.username
				userobj['designation'] =  user.designation
				userobj['user_id'] = user.id
				user_list.append(userobj)
			obj = convToJson(user_list)
			client_response = Response(obj, mimetype='application/json')
			return client_response,status.HTTP_200_OK
		else:
			client_message = ResponseClass.authority_exception.value
			objecto = ResponseClass.creationerror_message(client_message)
			client_response = Response(objecto, mimetype='application/json')
			return client_response,status.HTTP_400_BAD_REQUEST
	else:
		obj = json.dumps(data)
		ret_status = return_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,ret_status
	
def getTeamMembers():
	return_response = validate_user()
	data = json.loads(return_response.text)
	if return_response.status_code == 200:
		authority = authorisation(data['User_id'])
		if authority:
			user_list = []
			team_type_query = TeamType.select()
			for team in team_type_query:
				user_obj = {}
				user_obj['team_type'] = team.team_type
				user_obj['team_id'] = team.id
				user_query = User.select().where(User.team_type == team.id)
				team_list =[]
				for user in user_query:
					team_obj={}
					team_obj['name'] = user.username
					team_obj['user_id'] = user.id
					team_obj['designation'] = user.designation
					team_list.append(team_obj)
				user_obj['members'] = team_list
				user_list.append(user_obj)
			obj = convToJson(user_list)
			resp = Response(obj, mimetype='application/json')
			return resp,status.HTTP_200_OK
		else:
			client_message = ResponseClass.authority_exception.value
			objecto = ResponseClass.creationerror_message(client_message)
			client_response = Response(objecto, mimetype='application/json')
			return client_response,status.HTTP_400_BAD_REQUEST
	else:
		obj = json.dumps(data)
		ret_status = return_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,ret_status