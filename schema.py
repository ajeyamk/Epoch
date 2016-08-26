import jsonschema
from flask import json
from flask import app,jsonify,request

class Validation():
	EmailFormat = "[^@]+@[^@]+\.[^@]+"
	signup_schema = {
	"$schema": "http://json-schema.org/draft-04/schema#",
	"type": "object",
	"properties": {
		"username": {
				 "type": "string",
				 "minLength": 3,
				 "maxLength": 30,
		},
		"email": {
				 "type": "string",
				  "pattern":"[^@]+@[^@]+\.[^@]+",
				  "maxLength": 60,
		},
		"password": {
			"type": "string",
			"minLength": 6,
			"maxLength": 50,
		},

		"username":{
		 	"type": "string",
		 	"minLength": 5,
			"maxLength": 50,

		},
		"first_name":{
			"type": "string",
			"maxLength": 50,
		 	
		},

		"last_name":{
			"type": "string",
		 	"minLength": 5,
			"maxLength": 50,
		 	
		},

		"phone_number": {
			"type": "string",
			"minLength": 10,
			"maxLength": 15,
		},

		"designation":{
			"type": "string",
		}

	},
	"required": ["username","password", "email","designation"]
}

	login_schema = {
		"$schema": "http://json-schema.org/draft-04/schema#",
		"type": "object",
		"properties": {
			"email": {
				 	"type": "string",
				  	"pattern":"[^@]+@[^@]+\.[^@]+",
			},

			"password": {
			"type": "string",
		},
		},"required" :["email","password"]
	}


