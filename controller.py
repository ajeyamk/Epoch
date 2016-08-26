from flask import Flask,request,Response
import responseservice,userservice,projectservice,logservice,schema
from projectservice import authorisation
from flask.ext.api import status
from flask.ext.cors import CORS
from responseservice import ResponseClass
from decorators import signup_validate_schema,login_validate_schema,validate_token,validate_user
import config

app = Flask(__name__)
CORS(app)

@app.route('/signup',methods = ['POST'])
@signup_validate_schema(schema.Validation.signup_schema)
def api_signup():
	api_object = userservice.signup()
	return api_object

@app.route('/login',methods = ['POST'])
@login_validate_schema(schema.Validation.login_schema)
def api_login():
	api_object = userservice.login()
	return api_object

@app.route('/getprojects',methods = ['GET'])
def api_getprojects():
	api_object = projectservice.getProjects()
	return api_object
	
@app.route('/getusers',methods = ['GET'])
def api_getusers():
	api_object = userservice.getUsers()
	return api_object

@app.route('/getteams',methods = ['GET'])
def getteams():
	api_object = projectservice.getTeams()
	return api_object

@app.route('/getissues',methods = ['GET'])
def api_getissues():
	api_object = projectservice.getIssues()
	return api_object

@app.route('/getallprojects',methods = ['GET'])
def api_getallprojects():
	api_object = projectservice.getAllProjects()
	return api_object	

@app.route('/createproject',methods = ['POST'])
def api_createproject():
	api_object = projectservice.createProject()
	return api_object

@app.route('/loghours',methods = ['POST'])
def api_loghours():
	api_object = logservice.logHours()
	return api_object

@app.route('/getprojectdetails',methods = ['POST'])
def api_proj_details():
	api_object = logservice.projectDetails()
	return api_object	

@app.route('/get-loghistory',methods = ['GET'])
def api_project_history_details():
    api_object = logservice.getHistory()
    return api_object

@app.route('/logout',methods = ['PUT'])
def api_logout():
	api_object = userservice.logout()
	return api_object

@app.route('/editpassword',methods = ['POST'])
def api_editpassword():
	api_object = userservice.editPassword()
	return api_object

@app.route('/edit',methods = ['POST'])
def api_edit():
	api_object = logservice.editLog()
	return api_object

@app.route('/getteammembers',methods = ['GET'])
def api_getteammembers():
	api_object = userservice.getTeamMembers()
	return api_object

@app.route('/temp',methods = ['POST'])
def api_temp():
	api_object = projectservice.temp()
	return api_object

	
if __name__ == "__main__":
	app.run(host= config.HOST, port=config.PORT, debug=False)
