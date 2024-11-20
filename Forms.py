from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, TextAreaField,BooleanField, SelectField,DateField, URLField,RadioField,FloatField,TelField
from wtforms.validators import DataRequired,Length,Email, EqualTo, ValidationError,Optional
from flask_login import current_user
from flask_wtf.file import FileField , FileAllowed
# from wtforms.fields.html5 import DateField,DateTimeField


class UserForm(FlaskForm):

    name = StringField('name', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('confirm', validators=[DataRequired(),EqualTo('password'), Length(min=8, max=64)])
    contacts = TelField('Contacts')
    address = StringField('Physical Address')
    image = FileField('Profile Image', validators=[FileAllowed(['jpg','png',"webp",'jpeg','avi'])])

    submit = SubmitField('Create Account!')

    def validate_email(self,email):
        from app import db, User,app

        # with db.init_app(app):
        user_email = User.query.filter_by(email = self.email.data).first()
        if user_email:
            return ValidationError(f"Email already registered in this platform")


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):

    proj_name = StringField('Project Title*', validators=[DataRequired()])
    description = TextAreaField('Briefly Describe The Project*', validators=[DataRequired(),Length(max=100)])
    proj_assistance = TextAreaField('What Assistance Do You Need?*', validators=[DataRequired(),Length(max=500)])
    proj_duration_start = DateField("Start Date")
    proj_duration_end = DateField("Projected End Date (Estimated)")
    # company_name = StringField('Name / Company Name', validators=[DataRequired()])
    # company_email = StringField('Email', validators=[DataRequired()])
    attachment = FileField('Attachment (Optional)', validators=[Optional()])
    submit=SubmitField('submit')


class AssignmentForm(FlaskForm):

    assignment = TextAreaField("What's The Assignment Today?", validators=[Length(max=600)])
    assign_img = FileField('Attachment', validators=[Optional()])
    upload = FileField('Attachment ', validators=[Optional()])
    upload1 = FileField('Attachment', validators=[Optional()])
    url = URLField('URL (Optional)')
    status = RadioField("Status",choices=[("Open","Open"),("Closed","Closed")])
    submit = SubmitField('submit')


class ProjectReportingForm(FlaskForm):

    report = TextAreaField('Report*', validators=[DataRequired()])
    rep_img1 = FileField('Attachment 1', validators=[Optional()])
    rep_img2 = FileField('Attachment 2', validators=[Optional()])
    rep_img3 = FileField('Attachment 3', validators=[Optional()])
    comments = TextAreaField('Report', validators=[Optional()])
    price = FloatField("Fee")
    pending = BooleanField('Work Still Pending?', validators=[Optional()])
    pending_payment = BooleanField('Payment Pending?', validators=[Optional()])
    status = RadioField("Status",choices=[("Started","Started"),("Halfway Done","Halfway Done"),("Almost Done","Almost Done"),("Finished","Finished")])
    date_finished=DateField("Finished Date")
    submit = SubmitField('submit')


class SendEmailForm(FlaskForm):

    name = StringField('Name', validators=[Length(max=120)])
    emails = StringField('Emails', validators=[Length(max=120)])
    submit = SubmitField('submit')


class Contact_Form(FlaskForm):

    name = StringField('name')
    email = StringField('email', validators=[DataRequired(),Email()])
    contact = TelField('contact')
    subject = StringField("subject")
    message = TextAreaField("Message",validators=[Length(min=8, max=255)])
    submit = SubmitField("Send")



class Reset(FlaskForm):

    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password'), Length(min=8, max=64)])

    reset = SubmitField('Reset')


class Reset_Request(FlaskForm):

    email = StringField('email', validators=[DataRequired(), Email()])
    reset = SubmitField('Submit')
