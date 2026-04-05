from flask_restful import Resource
from flask import request,jsonify , make_response
from Backend.user_datastore import user_datastore
from flask_security import utils,auth_token_required,roles_required,login_required,current_user
from flask_security.utils import hash_password,verify_password
from Backend.models import *

class Dashboard(Resource):
    @login_required
    @auth_token_required
    def get(self):
        user = current_user
        company= user.company_profile
        profile = {
            "username":user.username,
            "email":user.email,
            "location":company.location,
            "industry":company.industry,
            "approve_status":company.approve_status,
            "website":company.website,
            "hr_contact":company.hr_contact
        }
# show applications
        drives= []
        for d in company.drives:
            if d.approve_status =='Approved':
                drives.append({
                    "drive_id":d.drive_id,
                    "job_title":d.job_title,
                    "job_desc":d.job_desc,
                    "eligibility":d.eligibility,
                    "app_deadline":d.app_deadline.strftime("%d-%m-%Y %H:%M"),
                    "location":d.location,
                    "type":d.type,
                    "salary":d.salary,
                    "post_status":d.post_status,
                    "application_count":len(d.application_rel)
                })


        return {
            "profile":profile,
            "drives":drives
        },200
    
    @login_required
    @auth_token_required
    def post(self):
        user = current_user
        user_info = request.get_json()
        if not user_info:
            return {"message":"No data provided"},400

        if 'username' in user_info:
            user.username = user_info['username']
        if 'email' in user_info:
            user.email = user_info['email']
        if 'password' in user_info:
            user.password = hash_password(user_info['password'])

        company = user.company_profile 
        if company:
            if 'industry' in user_info:
                company.industry = user_info['industry']
            if 'location' in user_info:
                company.location = user_info['location']
            if 'hr_contact' in user_info:
                company.hr_contact = user_info['hr_contact']
            if 'website' in user_info:
                company.website =  user_info['website']
            
        db.session.commit()
        return {"message":"Company details updated successfully"},200
    

class PostJob(Resource):
    @login_required
    @auth_token_required
    def post(self):
        job_details = request.get_json()
        company = current_user.company_profile

        deadline_str = job_details.get('app_deadline')
        parsed_deadline = datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M").date() if deadline_str else None    
        
        new_drive=  PlacementDrive(
            job_title = job_details.get('job_title'),
            job_desc = job_details.get('job_desc'),
            eligibility = job_details.get('eligibility'),
            app_deadline = parsed_deadline,
            location = job_details.get('location'),
            type = job_details.get('type'),
            salary = job_details.get('salary'),
            c_id = company.company_id,
            approve_status = 'Pending'
        )
        db.session.add(new_drive)
        db.session.commit()
        return {"message":"Drive created successfuly,it will be visible after admin's approval"},201
        

class DeleteDrive(Resource):
    @auth_token_required
    @login_required
    def post(self):
        drive_id = request.get_json().get('drive_id')
        drive = PlacementDrive.query.filter_by(drive_id=drive_id).first()
        if(drive):
            db.session.delete(drive)
            db.session.commit()
            return {"message":"Drive deleted Successfully"},200
        else:
            return {"message":"Drive could not be deleted"},400
        
class DriveInfo(Resource):
    @auth_token_required
    @login_required
    def get(self,drive_id):
        drive = PlacementDrive.query.filter_by(drive_id=drive_id).first()
        drive_det= {
                    "drive_id":drive.drive_id,
                    "job_title":drive.job_title,
                    "job_desc":drive.job_desc,
                    "eligibility":drive.eligibility,
                    "app_deadline":drive.app_deadline.strftime("%d-%m-%YT%H:%M"),
                    "location":drive.location,
                    "type":drive.type,
                    "salary":drive.salary,
                    "post_status":drive.post_status,
        }
        
        students = []
        for s in drive.application_rel:
            students.append({
                "app_id":s.id,
                "id":s.student.user_id,
                "username":s.student.user_stu.username,
                "email":s.student.user_stu.email,
                "education":s.student.education,
                "skill":s.student.skill,
                "description":s.student.description,
                "status":s.status,
                "date_applied":s.date_applied.strftime("d-%m-%YT%H:%M")
                
            })
        return {"drive_det":drive_det,"stu_appli":students},200


class UpdateAppStatus(Resource):
    @auth_token_required
    @login_required
    def post(self):
        app_id= request.get_json().get('id')
        app = Application.query.filter_by(id=app_id).first()
        if app:
            if app.status=='Applied':
                app.status='Shortlisted'
            elif app.status=='Shortlisted':
                app.status='Interview'
            elif app.status=='Interview':
                app.status='Selected'
            elif app.status=='Selected':
                app.status='Rejected'
            else:
                app.status='Applied'
            db.session.commit()
            return {"message":f"Application status updated to: {app.status}"},200
        return {"message":"Application cannot be updated"},404
    

class DriveStatus(Resource):
    @auth_token_required
    @login_required
    def post(self):
        drive_id = request.get_json().get('drive_id')
        drive = PlacementDrive.query.filter_by(drive_id=drive_id).first()
        if drive:
            if drive.post_status=='Active':
                drive.post_status='Closed'
            else:
                drive.post_status='Active'
            db.session.commit()
            return {"message":f"Drive status updated to {drive.post_status}"},200
        return {"message":"Drive not found"},404

