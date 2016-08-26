from functools import wraps
from jsonschema import validate
import jsonschema,schema,model
from model import User
from responseservice import ResponseClass
from flask import request,json
from flask import Response
from flask.ext.api import status
import requests,config


def login_validate_schema(schema_name):
   def decorator(f):
	   @wraps(f)
	   def wrapper(*args, **kw):
		   try:
			   data=request.json
			   validate(request.json, schema_name)
		   except jsonschema.ValidationError as ex:
			   print (ex.relative_schema_path)
			   try:
				   err = ex.absolute_path[0] + " is invalid "
			   except Exception as e:
				   err = ex.message 
			   return(ResponseClass.creationerror_message(err),status.HTTP_400_BAD_REQUEST)
		   except jsonschema.SchemaError as e:
		   	errmessage = e.message 
		   	return(ResponseClass.creationerror_message(errmessage),status.HTTP_400_BAD_REQUEST)       
		   except Exception as e:
			   print(e)
			   message=ResponseClass.log_in_exception.value
			   return(ResponseClass.creationerror_message(message),status.HTTP_400_BAD_REQUEST)
		   return f(*args, **kw)
	   return wrapper
   return decorator

def signup_validate_schema(schema_name):
   def decorator(f):
	   @wraps(f)
	   def wrapper(*args, **kw):
		   try:
			   data=request.json
			   validate(request.json, schema_name)
		   except jsonschema.ValidationError as ex:
			   print (ex.relative_schema_path)
			   try:
				   err = ex.absolute_path[0] + " is invalid "
			   except Exception as e:
				   err = ex.message 
			   return(ResponseClass.creationerror_message(err),status.HTTP_400_BAD_REQUEST)
		   except jsonschema.SchemaError as e:
		   	errmessage = e.message 
		   	return(ResponseClass.creationerror_message(errmessage),status.HTTP_400_BAD_REQUEST)       
		   except Exception as e:
			   print(e)
			   message=ResponseClass.signup_exception.value
			   return(ResponseClass.creationerror_message(message),status.HTTP_400_BAD_REQUEST)
		   return f(*args, **kw)
	   return wrapper
   return decorator



def validate_token(f):
	@wraps(f)
	def wrapper(*args, **kw):
		try:
			reqheader = request.headers.get('User_token')
			if (reqheader == None):
				message = ResponseClass.invalid_token.value
				response = ResponseClass.creationerror_message(message)
				return response,status.HTTP_400_BAD_REQUEST
			else:
				squery = SessionTable.get(SessionTable.session_ID == reqheader)
				user_data = User.get(User.id == squery.user_id)
				data = {'username': user_data.username,'email-ID':user_data.email}
		except Exception as  e:
			print(e)
			message =  ResponseClass.invalid_token.value
			response = ResponseClass.creationerror_message(message)
			return response,status.HTTP_400_BAD_REQUEST
		return f(user_data.id,*args, **kw)
	return wrapper


def validate_user():
	try:
		reqheader = request.headers.get('User_token')
		if (reqheader == None):
			message = ResponseClass.invalid_token.value
			response = ResponseClass.creationerror_message(message)
			return response,status.HTTP_400_BAD_REQUEST
		else:
			url = config.EXT_API_AUTH
			headers = {'Session_token': reqheader}
			delegate_data = {'Content-Type' : 'application/json'}
			return_response = requests.get(url, headers=headers)
			return return_response
	except Exception as  e:
		print(e)
		message =  ResponseClass.invalid_token.value
		response = ResponseClass.creationerror_message(message)
		return response,status.HTTP_400_BAD_REQUEST
		
