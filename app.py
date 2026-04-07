from flask import Flask
from flask_security import Security,hash_password
from Backend.database import db
from Backend.config import Config
from Backend.user_datastore import user_datastore
from flask_restful import Api 
from flask_cors import CORS

from Backend.cache import cache

def create_app():
    app =Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    cache.init_app(app)

    security = Security(app,user_datastore)
    api = Api(app)
    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin',description='Administrator')
        student_role = user_datastore.find_or_create_role(name='student',description='Student')
        company_role = user_datastore.find_or_create_role(name='company',description='Company')

        if not user_datastore.find_user(username='admin'):
            user_datastore.create_user(username='admin',email='admin@gmail.com',password=hash_password('harsh'),roles=[admin_role])
        db.session.commit()
    return app,api

app ,api = create_app()
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)


from Backend.AuthAPI import *
from Backend.Student import * 
from Backend.company import *
from Backend.admin import *


# api.add_resource(Home,'/')
# authentication

api.add_resource(LoginAPI,'/api/login')
api.add_resource(LogoutAPI,'/api/logout')
api.add_resource(CompanyRegisterAPI,'/api/company/register')
api.add_resource(StudentRegisterAPI,'/api/student/register')

# student

api.add_resource(Mydashboard,'/api/student','/api/student/profile','/api/student/profile/update')
api.add_resource(ApplyJob,'/api/student/applyjob')
api.add_resource(Interview,'/api/student/interviews')
api.add_resource(Search,'/api/student/search')
api.add_resource(GetOffer,'/api/student/offer-letters')

# admin
api.add_resource(DashBoardInfo,'/api/admin')
api.add_resource(Approvals,'/api/admin/approvals')
api.add_resource(Delete,'/api/admin/delete')
api.add_resource(AdminSearch,'/api/admin/search')

# company
api.add_resource(PostJob,'/api/company/profile/post-job')
api.add_resource(Dashboard,'/api/company/profile','/api/company','/api/company/profile/update')
api.add_resource(DeleteDrive,'/api/company/delete')
api.add_resource(DriveStatus,'/api/company/drive-status')
api.add_resource(UpdateAppStatus,'/api/company/drive/info/status')
api.add_resource(DriveInfo,'/api/company/drive/info/<int:drive_id>')
api.add_resource(OfferLetter,'/api/company/drive/info/offer-letter')

if __name__=='__main__':
    app.run(debug=True)