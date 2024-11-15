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
    contacts = TelField('Contacts', validators=[DataRequired()])
    address = StringField('Physical Address', validators=[DataRequired()])
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
    description = TextAreaField('Briefly Describe The Project*', validators=[DataRequired()])
    proj_assistance = TextAreaField('What Assistance Do You Need?*', validators=[DataRequired()])
    proj_duration_start = DateField("Start Date")
    proj_duration_end = DateField("Projected End Date (Estimated)")
    company_name = StringField('Name / Company Name', validators=[Optional()])
    company_email = StringField('Email', validators=[Optional()])
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
    rep_img1 = FileField('Image', validators=[Optional()])
    rep_img2 = FileField('Image', validators=[Optional()])
    rep_img3 = FileField('Image', validators=[Optional()])
    comments = TextAreaField('Comments', validators=[Optional()])
    price = FloatField("Fee")
    pending = BooleanField('Work Still Pending?', validators=[Optional()])
    pending_payment = BooleanField('Payment Pending?', validators=[Optional()])
    status = RadioField("Status",choices=[("Started","Started"),("Halfway Done","Halfway Done"),("Almost Done","Almost Done"),("Finished","Finished")])
    date_finished=DateField("Finished Date")
    submit = SubmitField('submit')




    # def validate_email(self,email):
    #     user = user.query.filter_by