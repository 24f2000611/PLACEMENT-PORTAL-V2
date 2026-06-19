from flask_restful import Resource
from flask import request,jsonify , make_response
from Backend.user_datastore import user_datastore
from flask_security import utils,auth_token_required,roles_required ,hash_password
from Backend.models import *
from flask import render_template
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
            return {
                "message":"Username is already taken"
            },400
        
        new_user = user_datastore.create_user(username =username,email=email ,password =hash_password(password) , roles=[role],fs_uniquifier=str(uuid.uuid4()))
        db.session.flush()
        new_company_profile = Company(company_id = new_user.id,approve_status='Pending')
        db.session.add(new_company_profile)
        db.session.commit() 

        return {
            "message":"Company Registered Successful",
            "user_details":{
                "username":username,
                "roles":[role.name]
            }

        },200

    
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
            return {
                "message":"Username is already taken"
            },400
        
        new_user = user_datastore.create_user(username =username,email=email ,password =hash_password(password) , roles=[role],fs_uniquifier=str(uuid.uuid4()))
        db.session.flush()
        new_student_profile = Student(user_id = new_user.id)
        db.session.add(new_student_profile)
        db.session.commit() 

        return {
            "message":"Registration Successful",
            "user_details":{
                "username":username,
                "roles":[role.name]
            }

        },200


        
class LoginAPI(Resource):
    def post(self):
        login_credentials = request.get_json()
        if not login_credentials:
            return {
                'message':'Login credentials are required'
            },400
        
        username = login_credentials.get('username',None)
        password = login_credentials.get('password',None)

        if not username or not password:
            return {
                "message":"Email and Password are required"
            },400            
        
        user = user_datastore.find_user(username=username)
        if not user:
            return {
                "message":"User does not exist"
            },404            
        
        if not utils.verify_password(password,user.password):
            return{"message":"Invalid password"},404
        
        auth_token = user.get_auth_token() 

        company_data = None
        if user.has_role('company'):
            company_profile = Company.query.filter_by(company_id = user.id).first()
            if company_profile:
                company_data = {"approve_status":company_profile.approve_status}
        utils.login_user(user)
        return{
            "message":"Login Successfuly",
            "user_details":{
                "username":user.username,
                "roles":[role.name for role in user.roles],
                "auth_token":auth_token,
                "company_profile":company_data
            }
        },200
        
    
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        return{"message":"Logout Successfuly"},200
    

