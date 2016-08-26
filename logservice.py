from flask.ext.api import status
from flask import json,jsonify,request,Response
from model import User,ProjectUser,LogTable,ProjectTable,JobType
from responseservice import ResponseClass
import projectservice
from decorators import validate_user
from projectservice import authorisation
from datetime import datetime
from datetime import timedelta
import config

def logHours():
	try:
		return_response = validate_user()
		return_data = json.loads(return_response.text)
		if return_response.status_code == 200:
			data= request.json
			print(data)
			if ProjectUser.select().where((ProjectUser.team_member == return_data['User_id']) & (ProjectUser.project == data['proj_id'])).exists():
				proj_query = ProjectTable.get(ProjectTable.id == data['proj_id'])
				log_query = LogTable.select().where((LogTable.user == return_data['User_id']) & (LogTable.logged_date == data['log_date']))
				total_hours =0
				for hours in log_query:
					total_hours = total_hours + hours.log_hours
				if total_hours < 24 :
					if data['log_hours'] < 24:
						time_now = datetime.now()
						project_expiry = proj_query.ext_date_end
						date = datetime.strptime(project_expiry, '%Y-%m-%d')
						if date >= time_now :
							log_data = {'project':data['proj_id'],'user':return_data['User_id'],'job_type':data['jobtype_id'],'description':data['description'],'logged_date':data['log_date'],'logged_hours':data['log_hours'],'team_type':"1"}
							log_object = LogTable(**log_data)
							log_object.save()
							obj = projectservice.convToJson(log_data)
							client_response = Response(obj, mimetype='application/json')
							return client_response,status.HTTP_200_OK
						else:
							message = ResponseClass.log_expiry.value
							obj = ResponseClass.creationerror_message(message)
							client_response = Response(obj, mimetype='application/json')
							return client_response,status.HTTP_400_BAD_REQUEST	
					else:
						message = ResponseClass.day_threshold_error.value
						obj = ResponseClass.creationerror_message(message)
						client_response = Response(obj, mimetype='application/json')
						return client_response,status.HTTP_400_BAD_REQUEST
				else:
					message = ResponseClass.log_threshold_error.value
					obj = ResponseClass.creationerror_message(message)
					client_response = Response(obj, mimetype='application/json')
					return client_response,status.HTTP_400_BAD_REQUEST	
			else:
				message = ResponseClass.log_failure.value
				obj = ResponseClass.creationerror_message(message)
				client_response = Response(obj, mimetype='application/json')
				return client_response,status.HTTP_400_BAD_REQUEST
		else:
			obj = json.dumps(return_data)
			ret_status = return_response.status_code
			client_response = Response(obj, mimetype='application/json')
			return client_response,ret_status
	except Exception as e:
		print(e)
		message = ResponseClass.project_details_exception.value
		obj = ResponseClass.creationerror_message(message)
		resp = Response(obj, mimetype='application/json')
		return resp,status.HTTP_400_BAD_REQUEST
		
def projectDetails():
	return_response = validate_user()
	return_data = json.loads(return_response.text)
	if return_response.status_code == 200:
		authority = authorisation(return_data['User_id'])
		if authority:
			data = request.json
			project_query = LogTable.select().where(LogTable.project == data['proj_id'])
			if project_query.exists():
				user_query = ProjectUser.select().where(ProjectUser.project == data['proj_id'])
				if user_query.exists():
					job_type_list =[]
					user_list =[]
					member_list=[]
					for user in user_query:
						user_object ={}
						user_object = user.team_member_id
						user_list.append(user_object)
					for member_data in user_list:
						member_data_query = User.select().where(User.id == member_data).paginate(1,15)
						log_hour_query = LogTable.select().where((LogTable.user == member_data) & (LogTable.project == data['proj_id'])).paginate(1,15)
						hour_list = []
						cummulative_hour_list=[]
						hour_job_list = []
						for hour in log_hour_query:
							hour_array={}	
							hour_array['hour'] = hour.logged_hours
							hour_array['jobtype_ID'] = hour.job_type_id
							hour_array['timestamp'] = hour.logged_time
							hour_list.append(hour_array)
						hour = 0
						for cummulative_hour in log_hour_query:
							hour = hour + cummulative_hour.log_hours
						cummulative_hour_list.append(hour)
						for member in member_data_query:
							member_data_array={}
							member_data_array['name'] = member.username
							member_data_array['designation'] = member.designation
							member_data_array['user_id'] = member.id
							member_data_array['job_type_hours'] = hour_list
							member_data_array['total_hours'] = cummulative_hour_list
							member_list.append(member_data_array)				
					return_object = projectservice.convToJson(member_list)
					client_response = Response(return_object, mimetype='application/json')
					return client_response,status.HTTP_200_OK
				else:
					message = ResponseClass.user_query_failure.value
					obj = ResponseClass.creationerror_message(message)
					client_response = Response(obj, mimetype='application/json')
					return client_response,status.HTTP_400_BAD_REQUEST
			else:
				message = ResponseClass.project_query_failure.value
				obj = ResponseClass.creationerror_message(message)
				client_response = Response(obj, mimetype='application/json')
				return client_response,status.HTTP_400_BAD_REQUEST
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
		

def getHistory():
	return_response = validate_user()
	return_data = json.loads(return_response.text)
	if return_response.status_code == 200:
		log_query = LogTable.select().where(LogTable.user == return_data['User_id']).paginate(1,50)
		if log_query.exists():
			log_hour_query = LogTable.select().order_by(LogTable.logged_time.desc()).where(LogTable.user == return_data['User_id']).paginate(1,50)
			hour_list=[]
			cummulative_hour_list=[]
			member_list=[]
			hour = 0
			for cummulative_hour in log_hour_query:
				hour = hour + cummulative_hour.log_hours
			cummulative_hour_list.append(hour)
			for hour in log_hour_query:
				proj_query = ProjectTable.get(ProjectTable.id == hour.project_id)
				hour_array={}
				member_data_array={}
				hour_array['hour'] = hour.log_hours
				hour_array['jobtype_ID'] = hour.job_type_id
				hour_array['timestamp'] = hour.logged_time
				hour_array['datestamp'] = hour.logged_date
				hour_array['description'] = hour.description
				hour_array['proj_id'] = hour.project_id
				hour_array['proj_name'] = proj_query.name
				hour_list.append(hour_array)
			member_data_array['job_type_hours'] = hour_list
			member_data_array['total_hours'] = cummulative_hour_list
			member_list.append(member_data_array)		
			return_object = projectservice.convToJson(member_list)	
			return return_object
		else:
			message = ResponseClass.user_query_failure.value
			obj = ResponseClass.creationerror_message(message)
			client_response = Response(obj, mimetype='application/json')
			return client_response,status.HTTP_400_BAD_REQUEST
	else:
		obj = json.dumps(return_data)
		ret_status = return_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,ret_status
	
def editLog():
	return_response = validate_user()
	return_data = json.loads(return_response.text)
	if return_response.status_code == 200:
		data= request.json
		if ProjectUser.select().where((ProjectUser.team_member == return_data['User_id']) & (ProjectUser.project == data['proj_id'])).exists():
			proj_query = ProjectTable.get(ProjectTable.id == data['proj_id'])
			log_query = LogTable.select().where((LogTable.user == return_data['User_id']) & (LogTable.logged_date == data['log_date']))
			total_hours =0
			for hours in log_query:
				total_hours = total_hours + hours.log_hours
			if total_hours < 24 :
				if data['log_hours'] < 24:
					time_now = datetime.now()
					project_expiry = proj_query.date_end
					date = datetime.strptime(project_expiry, '%Y-%m-%d %H:%M:%S')
					if date >= time_now :
						check_log_query = LogTable.select().where((LogTable.logged_date == data['log_date']) & (LogTable.user == return_data['User_id']) & (LogTable.project == data['proj_id']) & (LogTable.job_type == data['jobtype_id']))
						if check_log_query.exists():
							update_log_query= LogTable.select().where((LogTable.logged_date == data['log_date']) & (LogTable.user == return_data['User_id']) & (LogTable.project == data['proj_id']) & (LogTable.job_type == data['jobtype_id'])).get()
							update_log = {'description':data['description'],'log_hours':data['log_hours']}
							update_log_object = LogTable.update(**update_log).where(LogTable.id == update_log_query.id)
							update_log_object.execute()
							last_update = LogTable.get(LogTable.id == update_log_query.id)
							last_update.modified_date = datetime.now()
							last_update.save()
							message = ResponseClass.re_edit.value
							obj = ResponseClass.creationsuccess_message(message)
							client_response = Response(obj, mimetype='application/json')
							return client_response,status.HTTP_200_OK	
						else:	
							log_data = {'project':data['proj_id'],'user':return_data['User_id'],'job_type':data['jobtype_id'],'description':data['description'],'logged_date':data['log_date'],'logged_hours':data['log_hours']}
							log_object = LogTable(**log_data)
							log_object.save()
							message = ResponseClass.editsuccess.value
							obj = ResponseClass.creationsuccess_message(message)
							client_response = Response(obj, mimetype='application/json')
							return client_response,status.HTTP_200_OK
					else:
						message = ResponseClass.log_expiry.value
						obj = ResponseClass.creationerror_message(message)
						client_response = Response(obj, mimetype='application/json')
						return client_response,status.HTTP_400_BAD_REQUEST	
				else:
					message = ResponseClass.day_threshold_error.value
					obj = ResponseClass.creationerror_message(message)
					client_response = Response(obj, mimetype='application/json')
					return client_response,status.HTTP_400_BAD_REQUEST
			else:
				message = ResponseClass.log_threshold_error.value
				obj = ResponseClass.creationerror_message(message)
				client_response = Response(obj, mimetype='application/json')
				return client_response,status.HTTP_400_BAD_REQUEST	
		else:
			message = ResponseClass.log_failure.value
			obj = ResponseClass.creationerror_message(message)
			client_response = Response(obj, mimetype='application/json')
			return client_response,status.HTTP_400_BAD_REQUEST
	else:
		obj = json.dumps(return_data)
		ret_status = return_response.status_code
		client_response = Response(obj, mimetype='application/json')
		return client_response,ret_status



		
	

		