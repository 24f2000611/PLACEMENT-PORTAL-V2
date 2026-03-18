from flask_restful import Resource
from flask import request,jsonify , make_response
from Backend.user_datastore import user_datastore
from flask_security import utils,auth_token_required,roles_required ,hash_password
from Backend.models import *
import uuid

class CompanyRegisterAPI(Resource):
    def post(self):
        register_creds = request.get_json()
        if not register_creds:
            return {"message":"Credentials are required"},400
        
        username = register_creds.get('username',None)
        password = register_creds.get('password',None)
        email = register_creds.get('email',None)
        role = user_datastore.find_role('company')

        if not username or not password or not email:
            return {"message":"Credentails cannot be empty"},400
        
        if len(password) < 6:
            return {"message":"Password cannot be less than 6 characters"},400
        
        if user_datastore.find_user(username=username) or user_datastore.find_user(email=email):
            result={
                "message":"Username is already taken"
            }
            return make_response(jsonify(result),400)
        
        new_user = user_datastore.create_user(username =username,email=email ,password =hash_password(password) , roles=[role],fs_uniquifier=str(uuid.uuid4()))
        db.session.flush()
        new_company_profile = Company(company_id = new_user.id,approve_status='pending')
        db.session.add(new_company_profile)
        db.session.commit() 

        response = {
            "message":"Company Registered Successful",
            "user_details":{
                "username":username,
                "roles":[role.name]
            }

        }

        return make_response(jsonify(response),201)
    
class StudentRegisterAPI(Resource):
    def post(self):
        register_creds = request.get_json()
        if not register_creds:
            return {"message":"Credentials are required"},400
        
        username = register_creds.get('username',None)
        password = register_creds.get('password',None)
        email = register_creds.get('email',None)
        role = user_datastore.find_role('student')

        if not username or not password or not email:
            return {"message":"Credentails cannot be empty"},400
        
        if len(password) < 6:
            return {"message":"Password cannot be less than 6 characters"},400
        
        if user_datastore.find_user(username=username) or user_datastore.find_user(email=email):
            result={
                "message":"Username is already taken"
            }
            return make_response(jsonify(result),400)
        
        new_user = user_datastore.create_user(username =username,email=email ,password =hash_password(password) , roles=[role],fs_uniquifier=str(uuid.uuid4()))
        db.session.flush()
        new_student_profile = Student(user_id = new_user.id)
        db.session.add(new_student_profile)
        db.session.commit() 

        response = {
            "message":"Registration Successful",
            "user_details":{
                "username":username,
                "roles":[role.name]
            }

        }

        return make_response(jsonify(response),201)

        
class LoginAPI(Resource):
    def post(self):
        login_credentials = request.get_json()
        if not login_credentials:
            result = {
                'message':'Login credentials are required'
            }
            return make_response(jsonify(result),400)
        
        username = login_credentials.get('username',None)
        password = login_credentials.get('password',None)

        if not username or not password:
            result = {
                "message":"Email and Password are required"
            }            
            return make_response(jsonify(result),400)
        
        user = user_datastore.find_user(username=username)
        if not user:
            result = {
                "message":"User does not exist"
            }            
            return make_response(jsonify(result),404)
        
        if not utils.verify_password(password,user.password):
            result ={"message":"Invalid password"}
            return make_response(jsonify(result),400)
        
        auth_token = user.get_auth_token() 

        company_data = None
        if user.has_role('company'):
            company_profile = Company.query.filter_by(company_id = user.id).first()
            if company_profile:
                company_data = {"approve_status":company_profile.approve_status}
        response = {
            "message":"Login Successfuly",
            "user_details":{
                "username":user.username,
                "roles":[role.name for role in user.roles],
                "auth_token":auth_token,
                "company_profile":company_data
            }
        }
        utils.login_user(user)
        
        return make_response(jsonify(response),200)
    
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        response = {"message":"Logout Successfuly"}
        return make_response(jsonify(response),200)    
    
