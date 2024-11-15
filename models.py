
# from alchemy_db import db.Model
from sqlalchemy import  MetaData, ForeignKey
from flask_login import login_user, UserMixin
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from app import app

db = SQLAlchemy()

#from app import login_manager

metadata = MetaData()

#Users class, The class table name 'h1t_users_cvs'
class User(db.Model,UserMixin):
     
    __table_args__ = {'extend_existing': True}
    #Create db.Columns
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    image = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120), unique=True)
    confirm_password = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120))
    contacts = db.Column(db.String(120))
    verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(120))
    timestamp =db.Column(db.DateTime())
    project = relationship("Project_Description",backref="User",lazy=True)
    # project_briefs = relationship("Project_Brief", backref="Project_Brief", lazy=True)

    __mapper_args__={
        "polymorphic_identity":'user',
        'polymorphic_on':role
    }



class Project_Description(db.Model,UserMixin):

    __tablename__ = "project_description"

    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer,ForeignKey("user.id"))
    proj_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    proj_assistance = db.Column(db.String(600))
    work_specifications = db.Column(db.String(50))
    proj_duration_start = db.Column(db.DateTime(255))
    proj_duration_end = db.Column(db.DateTime(255))
    project_finished = db.Column(db.Boolean)
    timestamp=db.Column(db.DateTime)
    attachment=db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    company_email = db.Column(db.String(100))
    assignments=relationship("Assignment",backref="Project_Description",lazy=True)
    reports=relationship("Project_Reporting",backref="Project_Description",lazy=True)


class Assignment(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.Integer,ForeignKey("project_description.id"))
    uid = db.Column(db.Integer,ForeignKey("user.id"))
    assignment = db.Column(db.String(600))
    assign_img = db.Column(db.String(100))
    upload = db.Column(db.String(30))
    upload1 = db.Column(db.String(30))
    url = db.Column(db.String(255))
    status = db.Column(db.String(50))
    timestamp=db.Column(db.DateTime)
    paid = db.Column(db.Boolean)
    report=relationship("Project_Reporting",backref="Assignment",lazy=True)
    

class Project_Reporting(db.Model,UserMixin):

    __tablename__ = "project_reporting"

    id = db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.Integer,ForeignKey("project_description.id"))
    assignid = db.Column(db.Integer,ForeignKey("assignment.id"))
    uid = db.Column(db.Integer,ForeignKey("user.id"))
    report = db.Column(db.String(600))
    rep_img1 = db.Column(db.String(100))
    rep_img2 = db.Column(db.String(100))
    rep_img3 = db.Column(db.String(100))
    comments = db.Column(db.String(600))
    price = db.Column(db.Float(255))
    pending = db.Column(db.Boolean)
    pending_payment = db.Column(db.Boolean)
    status = db.Column(db.String(50))
    date_finished=db.Column(db.DateTime)
    timestamp=db.Column(db.DateTime)
    access=relationship("Invoice",backref="Project_Reporting",lazy=True)


class Invoice(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer,ForeignKey("user.id"))
    proj_id = db.Column(db.Integer,ForeignKey("project_reporting.id"))
    assignid = db.Column(db.Integer)
    balance = db.Column(db.Float(255))
    timestamp=db.Column(db.DateTime)
    token = db.Column(db.String(255))

