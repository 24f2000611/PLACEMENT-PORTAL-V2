from flask_restful import Resource
from flask import request,jsonify , make_response
from Backend.user_datastore import user_datastore
from flask_security import utils,auth_token_required,roles_required,login_required,current_user
from Backend.models import *
from Backend.cache import cache 


def dynamic_admin_key(*args,**kwargs):
    return f"admin_dash_{current_user.id}"

class DashBoardInfo(Resource):
    @roles_required('admin')
    @auth_token_required
    @cache.cached(timeout=10,make_cache_key=dynamic_admin_key)
    def get(self):
        stats = {
            "TotalStudents":Student.query.count(),
            "TotalCompanies":Company.query.count(),
            "TotalApplications":Application.query.count(),
            "TotalDrives":PlacementDrive.query.count()
        }

        reg_students = []
        for s in Student.query.all():
            reg_students.append({
                "id":s.user_id,
                "username":s.user_stu.username,
                "email":s.user_stu.email,
                "skill":s.skill,
                "education":s.education,
                "description":s.description
                # "location":s.location,
            })

        reg_companies = []
        for c in Company.query.all():
            reg_companies.append({
                "company_id":c.company_id,
                "username":c.user_comp.username,
                "email":c.user_comp.email,
                "industry":c.industry,
                "hr_contact":c.hr_contact,
                "website":c.website,
                "location":c.location,
                "approve_status":c.approve_status
                })

        applications = []
        for a in Application.query.all():
            drive_obj = a.drive
            company_obj = drive_obj.company if drive_obj else None
            student_obj = a.student
            applications.append({
                "application_id":a.id,
                "student_name":student_obj.user_stu.username,
                "company_name":company_obj.user_comp.username,
                "job_title":drive_obj.job_title,
                "job_desc":drive_obj.job_desc,
                "location":drive_obj.location,
                "salary":drive_obj.salary,
                "type":drive_obj.type,
                "date_applied":a.date_applied.strftime("%d-%m-%Y"),
                "app_status":a.status

            })

        drives = []
        for d in PlacementDrive.query.filter(PlacementDrive.approve_status=='Approved').all():
            drives.append({
                "drive_id":d.drive_id,
                "job_title":d.job_title,
                "job_desc":d.job_desc,
                "eligibility":d.eligibility,
                "app_deadline":d.app_deadline.strftime("%d-%m-%Y"),
                "location":d.location,
                "type":d.type,
                "salary":d.salary,
                "post_status":d.post_status
        })

       
        return {
            "dashboard_info":stats,
            "reg_companies" : reg_companies,
            "reg_students": reg_students,
            "drives" : drives,
            "applications" : applications
        },200


class Approvals(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        pending_comp = []
        for c in Company.query.filter(Company.approve_status !='Approved').all():
            pending_comp.append({
                "id":c.company_id,
                "username":c.user_comp.username,
                "email":c.user_comp.email,
                "industry":c.industry,
                "location":c.location,
                "hr_contact":c.hr_contact,
                "website":c.website,
                "approve_status":c.approve_status
            })

        pending_drives = []
        for d in PlacementDrive.query.filter(PlacementDrive.approve_status!='Approved').all():
            pending_drives.append({
                "id":d.drive_id,
                "job_title":d.job_title,
                "company_name":d.company.user_comp.username,
                "job_desc":d.job_desc,
                "eligibility":d.eligibility,
                "approve_status":d.approve_status,
                "salary":d.salary,
                "type":d.type,
                "app_deadline":d.app_deadline.strftime("%Y-%m-%d"),
                "location":d.location,
                "industry":d.company.industry
            })

        return {
            "pending_comp":pending_comp,
            "pending_drives" :pending_drives
        },200
    def post(self):
        data = request.get_json()
        target_type = data.get('type')
        target_id = data.get('id')

        if target_type == 'Company':
            target = Company.query.filter_by(company_id=target_id).first()
            cache.delete(f"company_id_{target.company_id}")
        else:
            target = PlacementDrive.query.filter_by(drive_id=target_id).first()
            cache.delete(f"company_id_{target.c_id}")

        if target:
            if target.approve_status=='Pending':
                target.approve_status = "Rejected"
            elif target.approve_status=='Rejected':
                target.approve_status='Approved'
        
            db.session.commit() 
            cache.delete(f"admin_dash_{current_user.id}")
            cache.delete('active_drives')

            if target_type=='Company':
                cache.delete(f"company_id_{target.company_id}")
            else:
                cache.delete(f"company_id_{target.c_id}")
            return {
                "message":f"Status Updated to :{target.approve_status}",
                "messageType":"success"
            },200
        return {"message":"Not found"},404
    

class Delete(Resource):
    def post(self):
        target_id = request.get_json().get('id')
        type = request.get_json().get('type')
        target = None
        if type=='Company':
            target = Company.query.filter_by(company_id=target_id).first()
        elif type=='Drive':
            target = PlacementDrive.query.filter_by(drive_id=target_id).first()
        elif type=='Application':
            target = Application.query.filter_by(id=target_id).first()
        else:
            target = User.query.filter_by(id=target_id).first()

        if target:
            db.session.delete(target)
            db.session.commit()

            cache.delete(f"admin_dash_{current_user.id}")
            cache.delete("active_drives")
            return {"message":f"{type} Deleted Successfuly"},200
        return {"message":"Not found"},404


class AdminSearch(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query','').strip()

        if not query:
            return {"results":None},200

        students = Student.query.join(User).filter(
            db.or_(User.username.ilike(f"%{query}%"))
        ).all()

        company = Company.query.join(User).filter(
            db.or_(User.username.ilike(f"%{query}%"),Company.industry.ilike(f"%{query}%"))
        ).all()

        drives = PlacementDrive.query.join(Company).filter(
            PlacementDrive.job_title.ilike(f"%{query}%")).all()

        apps = Application.query.join(PlacementDrive).join(Company).join(Student).filter(
            db.or_(User.username.ilike(f"%{query}%"),PlacementDrive.job_title.ilike(f"%{query}%"))
        ).all()

        return {
            "results":{
                "students":[{
                    "id":s.id,
                    "username":s.user_stu.username,
                    "email":s.user_stu.email,
                    "skill":s.skill,
                    "education":s.education,
                    "description":s.description
                } for s in students],
                "companies":[{
                        "company_id":c.id,
                        "username":c.user_comp.username,
                        "email":c.user_comp.email,
                        "industry":c.industry,
                        "hr_contact":c.hr_contact,
                        "website":c.website,
                        "location":c.location,
                        "approve_status":c.approve_status
                }for c in company],
                "drives":[{
                    "id":d.drive_id,
                    "job_title":d.job_title,
                    "company_name":d.company.user_comp.username,
                    "job_desc":d.job_desc,
                    "eligibility":d.eligibility,
                    "approve_status":d.approve_status,
                    "salary":d.salary,
                    "type":d.type,
                    "app_deadline":d.app_deadline.strftime("%d-%m-%Y"),
                    "location":d.location,
                    "industry":d.company.industry  
                }for d in drives],
                "applications":[{
                        "application_id":a.id,
                        "student_name":a.student.user_stu.username,
                        "company_name":a.drive.company.user_comp.username,
                        "job_title":a.drive.job_title,
                        "job_desc":a.drive.job_desc,
                        "location":a.drive.location,
                        "salary":a.drive.salary,
                        "type":a.drive.type,
                        "date_applied":a.date_applied.strftime("%d-%m-%Y")
                }for a in apps]
            }
        },200





