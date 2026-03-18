from flask_restful import Resource
from flask import request,jsonify , make_response
from Backend.user_datastore import user_datastore
from flask_security import utils,auth_token_required,roles_required
from Backend.models import *
from flask_security import current_user


class UpdateProfile(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        user = current_user
        student = user.student_profile
        return {
            "username":user.username,
            "password":user.password,
            "email":user.email,
            "education":student.education,
            "skill":student.skill,
            "description":student.description
        },200


    @auth_token_required
    @roles_required('student')
    def put(self):
        user = current_user
        user_info = request.get_json()
        if not user_info:
            return {"message":"No data provided"},400
        
        if 'username' in user_info:
            user.username = user_info['username']
        if 'email':
            user.email = user_info['email']
        if 'password' in user_info:
            user.password = user_info['password']
        
        student= user.student_profile
        if student:
            if 'education' in user_info:
                student.education = user_info['education']
            if 'skill' in user_info:
                student.skill = user_info['skill']

            if 'description' in user_info:
                student.description = user_info['description'] 

        db.session.commit()
        return {"message":"Profile updated successfully"},200


class ApplyJob(Resource):
    @auth_token_required
    @roles_required('student')
    def post(self):
        data = request.get_json()
        drive_id = data.get('drive_id')
        
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message":"Placement Drive not found"},404
        
        if drive.app_deadline< datetime.utcnow():
            return {"message":"Application deadline has passed"},400
        
        existing_app = Application.query.filter_by(student_id =current_user.id,drive_id=drive_id).first()

        if existing_app:
            return {"message":"You have already applied for this drive"},400
        
        new_application = Application(student_id =current_user.id,drive_id= drive_id)
        db.session.add(new_application)
        db.session.commit()
        return {"message":"Application submitted successfully"},200


class MyApplications(Resource):
    @auth_token_required
    def get(self):
        applications =Application.query.filter_by(student_id=current_user.id).all()
        if not applications:
            return {"message":"No applications found"},404
        
        result = []
        for app in applications:
            result.append({
                'application_id':app.app_id,
                "job_title":app.drive.job_title,
                "job_desc":app.drive.job_desc,
                "eligibility":app.drive.eligibility,
                "app_deadline":app.drive.app_deadline.strftime("%Y-%m-%d"),
                "location":app.drive.location,
                "type":app.drive.type,
                "salary":app.drive.salary,
                "company_name":app.drive.company.user_comp.username,
                "industry":app.drive.company.industry,
                "status":app.status

            })

        return result, 200


class Interview(Resource):
    @roles_required('student')
    @auth_token_required
    def get(self):
        placement = Placement.query.filter_by(student_id=current_user.id).all()
        if not placement:
            return {"message":"No applications found"},404
        
        result = []
        for offer in placement:
            result.append({
                'application_id':offer.app_id,
                "job_title":offer.drive.job_title,
                "job_desc":offer.drive.job_desc,
                "location":offer.drive.location,
                "type":offer.drive.type,
                "company_name":offer.drive.company.user_comp.username,
                "industry":offer.drive.company.industry,
                "package_offered":offer.package_offered,
                "interview_date":offer.interview_date.strftime("%Y-%m-%d")

            })
        return result,200

class OfferLetter(Resource):
    @roles_required('student')
    @auth_token_required
    def get(self):
        placement = Placement.query.filter_by(student_id=current_user.id).all()
        if not placement:
            return {"message":"No Offer Letters Yet"},401
        
        result = []
        for offer in placement:
            result.append({
                "company_name":offer.drive.company.user_comp.username,
                "industry":offer.drive.company.industry,
                "package_offered":offer.package_offered,
                "joining_date": offer.joining_date.strftime("%Y-%m-%d") if offer.joining_date else "TBD",  
                "location":offer.drive.location,
                "type":offer.drive.type,
                "description":offer.description


            })
        return result ,200


class Search(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        title = request.args.get('title','')
        company = request.args.get('company','')
        type = request.args.get('type','')
        location = request.args.get('location','')

        query = PlacementDrive.query.join(Company).join(User,Company.company_id == User.id)

        if title:
            query = query.filter(PlacementDrive.job_title.ilike(f"%{title}%"))

        if company:
            query= query.filter(PlacementDrive.company.user_comp.username.ilike(f"%{company}%"))

        if type:
            query = query.filter(PlacementDrive.type.ilike(f"%{type}%"))

        if location:
            query = query.filter(PlacementDrive.location.ilike(f"%{location}%"))

        results = query.all()

        output = []
        for drive in results:
            output.append({
                "drive_id": drive.id,
                "job_title": drive.job_title,
                "job_description":drive.job_desc,
                "eligibility":drive.eligibility,
                "company_name": drive.company.user.username,
                "location": drive.location,
                "salary": drive.salary,
                "skills": drive.skills_required,
                "deadline": drive.app_deadline.strftime("%Y-%m-%d") if drive.app_deadline else None
            })

        return output, 200
    
