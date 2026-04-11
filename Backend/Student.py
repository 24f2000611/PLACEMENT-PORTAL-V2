from flask_restful import Resource
from flask import request,jsonify , make_response
from Backend.user_datastore import user_datastore
from flask_security import utils,auth_token_required,roles_required,login_required,current_user
from Backend.models import *
from flask_security.utils import hash_password,verify_password
from Backend.cache import cache



def dynamic_student_key(*args,**kwargs):
    return f"student_dash_{current_user.id}"

class Mydashboard(Resource):
    @login_required
    @auth_token_required
    @roles_required('student')
    @cache.cached(timeout=10,make_cache_key=dynamic_student_key)
    def get(self):
        user = current_user
        student = user.student_profile
        profile= {
            "username":user.username,
            "email":user.email,
            "education":student.education,
            "skill":student.skill,
            "description":student.description
        }

        applications = []
        for app in student.applications:
            interview_time='No interview scheduled'
            if app.status=='Interview':
                if app.offer_letter:
                    placement_record = app.offer_letter[0]
                    if placement_record.interview_date:
                        interview_time = placement_record.interview_date.strftime("%d-%m-%Y")
            applications.append({
                            "app_id":app.app_id,
                            "job_title":app.drive.job_title,
                            "eligibility":app.drive.eligibility,
                            "description":app.drive.job_desc,
                            "salary":app.drive.salary,
                            "type":app.drive.type,
                            "location":app.drive.location,
                            "company_name":app.drive.company.user_comp.username,
                            "industry":app.drive.company.industry,
                            "status":app.status,
                            "app_deadline":app.drive.app_deadline.strftime("%d-%m-%Y"),
                            "date_applied":app.date_applied.strftime("%d-%m-%Y"),
                            "interview_date":interview_time

                        })         

        active_drives = []
        for d in PlacementDrive.query.filter_by(approve_status='Approved').all():
            active_drives.append({
                "drive_id":d.drive_id,
                "job_title":d.job_title,
                "company_name":d.company.user_comp.username,
                "job_description":d.job_desc,
                "salary":d.salary,
                "type":d.type,
                "location":d.location,
                "app_deadline":d.app_deadline.strftime("%d-%m-%Y"),
                "eligibility":d.eligibility,
                "post_status":d.post_status

            })

        return {
            "profile":profile,
            "applications":applications,
            "active_drives":active_drives
        },200
        
            # update profile
    
    @auth_token_required
    @roles_required('student')
    def post(self):
        user = current_user
        user_info = request.get_json()
        if not user_info:
            return {"message":"No data provided"},400
        
        if 'username' in user_info:
            user.username = user_info['username']
        if 'email' in user_info:
            user.email = user_info['email']
        if 'password' in user_info and user_info['password']:
            from flask_security import hash_password
            user.password = hash_password(user_info['password'])
        
        student= user.student_profile
        if student:
            if 'education' in user_info:
                student.education = user_info['education']
            if 'skill' in user_info:
                student.skill = user_info['skill']

            if 'description' in user_info:
                student.description = user_info['description'] 

        db.session.commit()
        cache.delete(f"student_dash_{current_user.id}")

        return {"message":"Profile updated successfully"},200


class ApplyJob(Resource):
    @login_required
    @auth_token_required
    @roles_required('student')
    def post(self):
        data = request.get_json()
        drive_id = data.get('drive_id')
        
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message":"Placement Drive not found"},404
        if drive.post_status =='Closed':
            return {"message":"The drive is not accepting applications"},400

        if drive.app_deadline < datetime.utcnow():
            return {"message":"Application deadline has passed"},400
            
        existing_app = Application.query.filter_by(student_id =current_user.id,drive_id=drive_id).first()

        if existing_app:
            return {"message":"You have already applied for this drive"},400
        
        new_application = Application(student_id =current_user.id,drive_id= drive_id,app_id=current_user.student_profile.id)
        db.session.add(new_application)
        db.session.commit()

        cache.delete(f"student_dash_{current_user.id}")
        cache.delete(f"company_id_{drive.c_id}")

        return {"message":"Application submitted successfully"},200


class Interview(Resource):
    @login_required
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
                "interview_date":offer.interview_date.strftime("%d-%m-%Y")

            })
        return result,200

class Search(Resource):
    @login_required
    @auth_token_required
    @roles_required('student')
    def get(self):
        title = request.args.get('title','')
        company = request.args.get('company','')
        type = request.args.get('type','')
        location = request.args.get('location','')

        query = PlacementDrive.query.join(Company)

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
                "deadline": drive.app_deadline.strftime("%d-%m-%Y") if drive.app_deadline else None
            })

        return output, 200
    


class GetOffer(Resource):
    @auth_token_required
    @login_required
    def get(self):
        offers = []
        placement = Placement.query.filter_by(student_id=current_user.id).all()
        for p in placement:
            offers.append({
                "id":p.id,
                "username":current_user.username,
                "company_name":p.application.drive.company.user_comp.username,
                "job_title":p.application.drive.job_title,
                "job_desc":p.application.drive.job_desc,
                "location":p.application.drive.company.location,
                "hr_contact":p.application.drive.company.hr_contact,
                "website":p.application.drive.company.website,
                "joining_date":p.joining_date.strftime("%d-%m-%Y") if p.joining_date else "Pending",
                "package_offered":p.package_offered,
                "description":p.description,
                "interview_date":p.interview_date.strftime("%d-%m-%Y") if p.interview_date else "Not Scheduled"
            })

        return {"offers":offers,"message":"Offers retrieved Successfully"},200
    


class ExportStatus(Resource):
    @login_required
    @auth_token_required
    def get(self,task_id):
        from celery.result import AsyncResult
        task = AsyncResult(task_id)

        if task.state =="PENDING":
            return {"status":"Processing"},202
        elif task.state =='SUCCESS':
            return {"status":"Ready","file_url":f"/download/{task_id}"},200
        else:
            return {"status":"Failed"},500