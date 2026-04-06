from Backend.database import db 
from flask_security import UserMixin ,RoleMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class User(db.Model,UserMixin,RoleMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean()) # true,false
    student_profile = db.relationship('Student',backref='user_stu',uselist=False,cascade='all,delete')
    company_profile = db.relationship('Company',backref='user_comp',uselist=False,cascade = 'all,delete')

    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    fs_uniquifier = db.Column(db.String(255),unique=True,nullable=False)
    fs_token_uniquifier = db.Column(db.String(255),unique=True,nullable=False)


    roles = db.relationship('Role',secondary='user_roles',backref=db.backref('users', lazy='dynamic'))


class Role(db.Model,RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name  = db.Column(db.String(80),unique=True,nullable=False)
    description = db.Column(db.String(255))


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id',ondelete='CASCADE'))



class PlacementDrive(db.Model):
    __tablename__='drives'
    drive_id= db.Column(db.Integer,primary_key =True)
    c_id = db.Column(db.Integer,db.ForeignKey('company.company_id'),nullable=False,unique=False)
    job_title = db.Column(db.String(100),nullable=False)
    job_desc = db.Column(db.Text,nullable=False)
    eligibility = db.Column(db.String(100),nullable=False)
    app_deadline = db.Column(db.DateTime,nullable=False)
    approve_status = db.Column(db.String(50),default='Pending') # pending,approved ,rejected(by admin)
    location = db.Column(db.String(100),nullable=True)
    type = db.Column(db.String(20),nullable=False)
    salary = db.Column(db.Integer,nullable=False)
    post_status = db.Column(db.String(50),default = 'Active') # active ,closed(by company)

    application_rel = db.relationship('Application',backref='drive',cascade='all,delete-orphan')


class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    app_id = db.Column(db.Integer,db.ForeignKey('students.id'))
    drive_id = db.Column(db.Integer,db.ForeignKey('drives.drive_id'))
    date_applied = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.String(30),default='Applied') # applied ,rejected, selected, shorlisted,interview


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer,primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))
    industry = db.Column(db.String(150),nullable=True)
    location = db.Column(db.String(150),nullable=True) 
    approve_status = db.Column(db.String(20),nullable=True,default='Pending') # pending,approved,rejected
    hr_contact = db.Column(db.String(150),nullable=True)
    website = db.Column(db.String(200),nullable=True)
    drives = db.relationship('PlacementDrive',backref='company',cascade = 'all,delete')


class Student(db.Model):
    __tablename__  ='students'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    education = db.Column(db.String(200),nullable=True)
    skill = db.Column(db.String(250),nullable=True)
    description = db.Column(db.String(300),nullable=True)
    # location = db.Column(db.String(100),nullable=True)
    applications = db.relationship('Application',backref='student',cascade='all,delete-orphan')


class Placement(db.Model):
    __tablename__ = 'placements'
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    drive_id = db.Column(db.Integer,db.ForeignKey('drives.drive_id'),nullable=False)
    joining_date = db.Column(db.DateTime)
    package_offered = db.Column(db.Integer)
    interview_date = db.Column(db.DateTime,nullable=True)
    description = db.Column(db.String(350))
    app_id = db.Column(db.Integer,db.ForeignKey('applications.id'))
    application = db.relationship('Application',backref='offer_letter') 