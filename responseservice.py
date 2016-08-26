
from flask import json,jsonify,request,Response
from enum import Enum
from flask.ext.api import status

class ResponseClass(Enum):
	user_success = "User created successfully"
	user_input_error = "email already exists.Please try with another email-ID"
	user_input_error2 = "something went wrong.check your inputs" # manually do something wrong in your signup catch block
	user_unknown = "The required user is not present"
	notes_absent = "The User has no projects"
	notes_unknown = "Fatal error while retrieving projects"
	user_absent = "The user is absent"
	users_unknown = "Unable to retrieve users"
	project_exception = "unable to create the project"
	allusers_exception = "Oops! Something went wrong.Check the Url"
	getuser_exception = "Error! in fetching the user.Check the Url"
	getnotes_exception = "Error! in fetching the projects.Check the Url"
	signup_exception = "Oops! Something went wrong.Unable to signup "
	log_in_exception = "Oops! Something went wrong.Unable to login "
	validation_error = "Error!Email and password are required fields.Recheck"
	existing_follower = "you are already following..!"
	followers_absent = "currently you don't have any followers"
	followees_absent = "you aren't following anyone"
	invalid_token = "the token is absent or corrupted"
	invalid_user = "the json is absent or corrupted"
	token_exception	= "payload is an invalid/expired token"
	following_exception = "Error in fetching your followees list"
	my_followers_exception = "Error in retrieving your followers list"
	follow_exception = "unable to follow this user. please try again later"
	login_exception = "unable to login. please try agian later"
	api_unfollow_exception = "oops! something went wrong.Coudn't unfollow the user.please try agin later"
	unfollow_user = " you unfollowed this user"
	unfollow_user_exception = "the user is already unfollowed"
	unfollow_exception  = "cannot unfollow"
	incorrect_bool = "incorrect bool value"
	login_failed = "incorrect email or password"
	project_success = "project created successfully"
	project_existing = "The project already exists"
	project_list_exception = "This's embarrassing!Coudn't load your list.Please try again"
	authority_exception = "Access Denied!"
	issues_unknown = "Unable to retrieve job type issues"
	check_query_exception = "You cannot log twice for the same issue"
	log_success = "You've successfully logged your work hours"
	log_failure = "Invalid user.Cannot log work!"
	log_hours_exception = "Sorry! Something went wrong,cannot process the request.Please try again later"
	admin_projects_unknown = "error while retrieving projects"
	project_details_exception = "Sorry! Something went wrong,cannot process the request.Please try again later"
	project_query_failure = "Cannot process the request.The requested project doesn't exist"
	user_query_failure = "Cannot process the request.The user hasn't logged work."
	logout_exception = "Sorry,unable to logout.Please try again later"
	edit_exception = "Sorry,unable to change the password.Please try again later"
	log_expiry = "The project has met it's deadline.You cannot further log!"
	log_threshold_error= "Threshold reached!You cannot log more than 24hours in a single day!"
	edit_log_hours_exception = "Access Denied!.You cannot edit"
	edit_log_hours_expiry_exception = "Time window has expired.You cannot edit after 5 days "
	editsuccess="edit successful"
	day_threshold_error = "You cannot log more than 24hours for a single day "
	re_edit = "Re-Edit successful"

	def creationsuccess_message(input_message):
		data = {"message": input_message}
		clientmessage = json.dumps(data)
		return clientmessage
		
	def creationerror_message(input_message):
		data = {"Error": input_message}
		clientmessage = json.dumps(data)
		return clientmessage