
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify
from flask_login import login_user, LoginManager,current_user,logout_user, login_required
from sqlalchemy.exc import IntegrityError
from Forms import *
from models import *
from flask_bcrypt import Bcrypt
import secrets
# import MySQLdb
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
# from bs4 import BeautifulSoup as bs
from flask_colorpicker import colorpicker
from image_processor import ImageProcessor
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import itsdangerous
import random
import string
# import sqlite3
# import pymysql
# import pyodbc



#Change App
app = Flask(__name__)
app.config['SECRET_KEY'] = "sdsdjfe832j2rj_32j"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project_assistant_db.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:tmazst41@localhost/eswatini_apps_db" #?driver=MySQL+ODBC+8.0+Driver"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://techtlnf_tmaz:!Tmazst41#@localhost/techtlnf_project_assistant"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle':280}
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOADED"] = 'static/uploads'

# Initialise App with DB 
db.init_app(app)

application = app

#Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Process image files, covert text, save in db and server 

def process_file(file):
        global img_checker
        
        filename = secure_filename(file.filename)

        # img_checker.img = file.filename

        _img_name, _ext = os.path.splitext(file.filename)
        gen_random = secrets.token_hex(8)
        new_file_name = gen_random + _ext

        print("DEBIG IMAGE: ",new_file_name)

        if file.filename == '':
            return 'No selected file'

        if file.filename:
            file_saved = file.save(os.path.join(app.root_path, 'static\images', new_file_name))
            flash(f"File Upload Successful!!", "success")
            return new_file_name


#Password Encryption
encrypt_password = Bcrypt()

#Populating variables across all routes
@app.context_processor
def inject_ser():
    global ser
    ser = Serializer(app.config['SECRET_KEY'])  # Define or retrieve the value for 'ser'

    return dict(ser=ser)



@app.route("/", methods=['POST','GET'])
def home():

    return render_template("index.html")


def send_email(user,passw):
    
    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] ='pro.dignitron@gmail.com' # os.getenv("MAIL")  creds.get('email')
        pwd = app.config["MAIL_PASSWORD"] = os.getenv("PWD")  #creds.get('gpass')
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)
        ser = Serializer(app.config['SECRET_KEY']) 
        # token = ser.dumps({"data":user.id})

        # try:
        #     db.session.add(App_Access_Credits(app_id=user.id,token=token))
        #     db.session.commit()

        # except IntegrityError:
        #     db.session.rollback()
        
        msg = Message(subject="Your Project Assistant", sender="no-reply@gmail.com", recipients=[user.email,'pro.dignitron@gmail.com'])

        msg.html = f"""<html> 
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        

        <style>
           body{{background-color: #e0e0e0;font-family: "Roboto" ,"Times New Roman";}}
           .mail-container{{width:60%;background-color: #ffffff;border-radius: 20px;margin:20px auto;  padding: 25px;}}
           .header{{height:100px;display: flex;justify-content: space-around;padding:15px;margin-bottom:80px ;}}
           .sub-titles{{background-color: #c4c4c4;color:white;padding:5px 10px;border-radius: 15px;font-weight: 600;font-size: 16px;}}
           p,label,small{{color:rgb(53, 53, 53)}}
           .content{{color:rgb(53, 53, 53)}}
           .scroll-container{{display: flex;justify-content: flex-start;gap:10px;align-items:center;width:max-content;}}
           .app-container{{display: flex;justify-content: center;align-items: center;flex-direction: column;width:200px;min-height: 200px;
                            gap:5px;padding:25px;border:1px solid grey;border-radius: 25px;}}
            .icon-cont img{{width:100%;border: 1px solid rgb(235, 235, 235);}}
            .app-name{{font-weight:500;font-size:23px;text-align: center;}}
            .owner-name{{font-weight:500;font-size:16px;color:#134f72;display: flex;align-items: center;}}
            .icon-imgs{{transition: all 0.3s ease;height: 30px;}}
            .icon-imgs:hover{{transform:scale(1.5)}}
            .description{{font-size:12px;color:#606060;text-align: center;}}
            .btns{{padding:10px;color:coral;border-radius:20px;border:1px solid coral;font-size: 16px;background: none;min-width:70px;  
                text-align: center;}}
            .btns:hover{{border:1px solid rgb(117, 117, 117) !important;color:rgb(117, 117, 117) !important;cursor: pointer;}}
            a{{text-decoration: none;}}
            .bolden{{font-weight:600}}
            img{{border-radius: 15px;}}
            .general-flex{{display:flex;justify-content:flex-start;align-items:center;gap:10px;flex-wrap:wrap;}}
            .mail-links{{display: flex;align-items: center;}}
            .mail-links span{{font-weight:600;font-size: 13px;color:#134f72}}
            .sign-column{{}}
            .email-sign-cont{{background-color: #f7f6f6;border-radius: 20px;padding:15px}}
            .div-line{{background-color: white;border-radius: 10px;width:7px;height:150px}}
            .services{{font-weight: 600;color:#134f72;font-size: 20px;}}
            .service{{font-weight: 500;color:#49565e}}
            .app-container {{width: 200px;min-height: 200px;border: 1px solid grey;border-radius: 25px;padding: 25px;background-color: #fff;
                overflow: hidden; /* Clear floats within the container */
            }}
            .app-cell {{
            text-align: center; /* Center the text */
        }}
        </style>
    </head>
    <body>
        <div  class="mail-container"><br>
            
            <!-- Header Title  -->
            <div class="header">
              <div style="flex-direction: ;" class="topic-con container">
                <div style="font-weight:600;font-size: 25px;color:#5f2364" class="topic">Your Project's Virtual Assistant
                </div>
              </div>
            </div>
            
            <!-- Subject  -->
  
            <!-- Body Message  -->
            <section style="flex-wrap: nowrap;" class="padding:10px">
                
                <div style="width:80%;margin:10px auto" class="content objectives">
                    
                    <!-- Greeting Message  -->
                <h3 style="color:#00a550;">Good day, {user.name}</h3>
                <div style="color:rgb(53, 53, 53)">Thank you for hiring my services as your project assistant. I look forward to a productive collaboration. For any follow-ups or clarifications on assignments, please feel free to message me.</div><br>
                    
                <div style="color:rgb(53, 53, 53)">Payments are calculated at the end of each day after consolidating the completed tasks. Charges start at a minimum of $5.00, with the possibility of performing smaller tasks at no fee, depending on my discretion. 
                I am open to discussing alternative payment approaches that align with your project needs.</div><br>
                    
                <!-- Sub Topic  -->
                <h2 style="color:coral">Login Details</h2>
                    <div style="color:rgb(53, 53, 53)">Here are the login details that you will need to create assignments or tasks for the current project. You might like to break this job down into each day's assignment (task) to provide more flexibility and clarity.
                </div>
                <p style="vertical-align: top;"><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Email: </span><span >{user.email}
                    </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Password: </span> <span> {passw}
                </span></p>
                    
                <div style="margin:20px auto;width:font-weight:600;"><a href="{url_for('login',_external=True)}"><span style="font-weight:500;"></span>
                <span style="background-color: #00a550;color:white;padding:5px 10px;
                border-radius: 15px;font-weight: 600;font-size: 16px; border-radius: 15px;">Login</span></a></div><br>
                    
                <!-- Sub Topic  -->
                <h2 style="color:coral">Report</h2>
                <p  style="font-weight:;"> Corresponding reports will be generated for each assignment rendered when the task is completed.
                </p>
                    
                <!-- Assignment Link -->
                <div style="margin:20px auto;width:font-weight:600;"><a href="{url_for('assignment',_external=True)}"><span style="font-weight:500;">Create First Assignment</span>
                    <span style="background-color: #00a550;color:white;padding:5px 10px;
                    border-radius: 15px;font-weight: 600;font-size: 16px; border-radius: 15px;">here</span></a></div>
                <br><br>

                    
                <!-- Footer / Email Signature -->
                </div><br><br>
                <p  class="">Kind Regards,</p> 
                <table style="font-size: medium;flex-wrap:nowrap;background-color: #f1f1f1;width:100% !important" class="email-sign-cont ">
                    <tr style="font-size: medium;flex-wrap:nowrap;width:100% !important" >
                        <td style="vertical-align: top;" class="sign-column">
                            <span style="font-size: large;font-weight: 600;color:#606060">Thabo Maziya,</span>
                            <span style="font-size: large;font-weight: 600;color:#606060">Project Assistant</span>
                            <div class="mail-links"><img style="height:25px" src="https://techxolutions.com/images/email_icon.png"/><span>thabo@techxolutions.com</span></div>
                            <div class="mail-links"><img style="height:25px" src="https://techxolutions.com/images/telephone_icon.png"/><span>(+268) 7641 2255</span></div>
                        </td>
                        
                    </tr>
                </table><br><br>
                
            </section>
            <div style="" class="email-signature">

            </div>
        </div>

        <script>
        
        </script>
    </body>
</html>

"""

        try:
            mail.send(msg)
            flash(f'Email Sent Successfully!', 'success')
            return "Email Sent"
        except Exception as e:
            flash(f'Email not sent here', 'error')
            return "The mail was not sent"

    # try:
    send_veri_mail() 


@app.route("/assigns_n_reports")
@login_required
def assigns_n_reports():

    project = Project_Description
    reports = Project_Reporting
    proj_assigns = Assignment.query.filter_by(uid=current_user).all()

    return render_template("assigns_n_reports.html",reports=reports,proj_assigns=proj_assigns,project=project)


@app.route("/project_reports")
@login_required
def project_reports():

    project = Project_Description.query.filter_by(uid=current_user).all()

    return render_template("projects.html",project=project)


@app.route("/send_email", methods=['POST','GET'])
def email():
    app_name_rq = None
    email_form = SendEmailForm()

    if request.method == "POST":
        app_name = email_form.app_name.data

        if app_name:
            app_name_rq = App_Info.query.filter_by(name=app_name).first()

        if app_name_rq:
            send_email(app_name_rq)
        else:
            return jsonify({"Error":f"App Name {app_name_rq} Does Not Exists in the System"})

    return render_template("send_email.html",email_form=email_form)


@app.route("/signup", methods=["POST","GET"])
def sign_up():

    register = UserForm()
    user = None

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':

        if register.validate_on_submit():    

            hashd_pwd = encrypt_password.generate_password_hash(register.password.data).decode('utf-8')

            user = User(name=register.name.data, email=register.email.data, password=hashd_pwd,
                    confirm_password=hashd_pwd,image="default.jpg",address=register.address.data,contacts=register.contacts.data,role = 'user',
                    timestamp=datetime.now())
                             
            # try:
            if not UserForm().validate_email(register.email.data):
                db.session.add(user)
                db.session.commit()
                print('Sign up successful!')
                flash(f"Account Successfully Created for {register.name.data}", "success")
            else:
                flash(f"Something went wrong, check for errors", "error")
                print('Sign up unsuccessful')
            return redirect(url_for('login'))
            # except: # IntegrityError:
            #     pass

        elif register.errors:
            flash(f"Account Creation Unsuccessful ", "error")
            print(register.errors)

    # from myproject.models import user
    return render_template("signup.html",register=register)


@app.route("/account", methods=["POST","GET"])
def account():

    register = UserForm()
    user = User.query.get(current_user.id)

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':

        if register.validate_on_submit():    

            user.name=register.name.data
            user.email=register.email.data
            user.address=register.address.data
            user.contacts=register.contacts.data
                             
            db.session.commit()
            flash('Update Successful!', "success")
            return redirect(url_for('login'))

    # from myproject.models import user
    return render_template("vac-signup-form.html",register=register,user=user)


@app.route("/login", methods=["POST","GET"])
def login():

    login = Login()

    # print(f"Submtion: ")
    if request.method == 'POST':
        print(f"Submtion: ")

        if login.validate_on_submit():    

                user_login = User.query.filter_by(email=login.email.data).first()
                print(f"Query: ",user_login)
                # flash(f"Hey! {user_login.password} Welcome", "success")
                if user_login and encrypt_password.check_password_hash(user_login.password, login.password.data):
                    login_user(user_login)
                    # print("Creditantials are ok")
                    print("No Verification Needed: ", user_login.verified)
                    req_page = request.args.get('next')
                    flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                    return redirect(req_page) if req_page else redirect(url_for('home'))
                    # if user_login:
                    # # if not user_login.verified:
                    #     return redirect(url_for('verification'))
                    # else:
                    #     # After login required prompt, take me to the page I requested earlier
                    #     print("No Verification Needed: ", user_login.verified)
                    #     req_page = request.args.get('next')
                    #     flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                    #     return redirect(req_page) if req_page else redirect(url_for('home'))
                else:
                    flash(f"Login Unsuccessful, please use correct email or password", "error")
                    # print(login.errors)
        else:
            print("No Validation")
            if login.errors:
                for error in login.errors:
                    print("Errors: ", error)
            else:
                print("No Errors found", login.email.data, login.password.data)

    return render_template("login.html",login=login)


@app.route("/report_form", methods=['POST','GET'])
def report():

    project = None
    report_form = ProjectReportingForm()

    if request.args.get("pid"):
        project = Project_Description.query.get(ser.loads(request.args.get("pid"))['data'])

    #Pending PID
    if request.method == "POST":#and app_form.validate_on_submit()
        project = Project_Description.query.get(ser.loads(request.args.get("pid"))['data'])
        report_info = Project_Reporting(
             report=report_form.report.data, comments=report_form.comments.data,  price=report_form.price.data, 
             pending=report_form.pending.data, pending_payment=report_form.pending_payment.data,  status=report_form.status.data,
             date_finished=report_form.date_finished.data,uid=project.uid,pid=project.id,
             url = report_form.url.data
        )

        if report_form.rep_img1.data:
            report_info.rep_img1 = process_file(report_form.rep_img1.data)
        if report_form.rep_img2.data:
            report_info.rep_img2 = process_file(report_form.rep_img2.data)
        if report_form.rep_img3.data:
            report_info.rep_img3 = process_file(report_form.rep_img3.data)

        db.session.add(report_info)
        db.session.commit()
        flash("Successful","success")

    return render_template("report_form.html",report_form=report_form,project=project,usr=User)


@app.route("/assignment_form", methods=['POST','GET'])
@login_required
def assignment():

    project = Project_Description.query.get(current_user.id)

    asignment_form = AssignmentForm()
    #Pending PID
    if request.method == "POST" :#and app_form.validate_on_submit()
        assignment_info = Assignment(
            assignment = asignment_form.name.data,url = asignment_form.url.data, status = asignment_form.status.data,
            pid=project.id
        )

        if asignment_form.assign_img.data:
            assignment_info.assign_img = process_file(asignment_form.assign_img.data)
        if asignment_form.upload.data:
            assignment_info.upload = process_file(asignment_form.upload.data)
        if asignment_form.upload1.data:
            assignment_info.upload1 = process_file(asignment_form.upload1.data)

        db.session.add(assignment_info)
        db.session.commit()
        flash("Successful","success")

    return render_template("assignment_form.html",asignment_form=asignment_form,project=project)


def pass_gen():
    
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))


@app.route("/project_form", methods=['POST','GET'])
def project_form():

    project_form = ProjectForm()

    if request.method == "POST" :#and app_form.validate_on_submit()
        project_info = Project_Description(
            proj_name = project_form.proj_name.data,description = project_form.description.data, proj_assistance = project_form.proj_assistance.data,
             proj_duration_start = project_form.proj_duration_start.data,
            proj_duration_end = project_form.proj_duration_end.data,
            company_name = project_form.company_name.data, company_email = project_form.company_email.data
        )

        if project_form.attachment.data:
            project_info.attachment = process_file(project_form.attachment.data)
        
        # assign user.id to project.uid for registered users 
        if current_user.is_authenticated:
            project_info.uid = current_user.id
            db.session.add(project_info)
            db.session.commit()
            # return redirect(url_for("assignment"))
            

        #If user not yet registered
        print("Check User: ",User.query.filter_by(email=project_form.company_email.data).first())
        if not User.query.filter_by(email=project_form.company_email.data).first():
            #generate password
            passw = pass_gen()
            hashd_pwd = encrypt_password.generate_password_hash(passw).decode('utf-8')
            sign_up_usr = User(name = project_form.company_name.data, email=project_form.company_email.data,password=hashd_pwd,confirm_password=hashd_pwd)
            db.session.add(sign_up_usr)
            db.session.commit()

            #Query user to get email and id
            user = User.query.filter_by(email=project_form.company_email.data).first()
            # assign user.id to project.uid for the current project 
            project = Project_Description.query.filter_by(company_email=user.email).first()
            project_info.uid = user.id
            db.session.commit()
            send_email(user,passw)
            print("Registered User: ",project_form.company_email.data)
            return redirect(url_for("login_details"))
        else:
            user = User.query.filter_by(email=project_form.company_email.data).first()
            project_info.uid = user.id
            db.session.add(project_info)
            db.session.commit()
        flash("Project Created Successfully","success")
        return redirect(url_for("assignment"))

    return render_template("project_form.html",project_form=project_form)


@app.route('/login_instructions')
def login_details():

    if current_user.is_authenticated:
        log_out()

    return render_template("login-details.html")


@app.route('/logout')
def log_out():

    logout_user()

    return redirect(url_for('home'))


@app.route("/project_form_edit", methods=['POST','GET'])
def project_form_edit():

    project_form_edit = ProjectForm()
    project_obj = Project_Description.query.get()

    if request.method == "POST" :#and app_form_edit.validate_on_submit()
        if project_form_edit.name.data:
            project_obj.proj_name = project_form_edit.name.data
        if project_form_edit.description.data:
            project_obj.description = project_form_edit.description.data
        if project_form_edit.proj_assistance.data:
            project_obj.proj_assistance = project_form_edit.proj_assistance.data
        if project_form_edit.work_specifications.data:
            project_obj.work_specifications = project_form_edit.work_specifications.data
        if project_form_edit.proj_duration_start.data: 
            project_obj.proj_duration_start = project_form_edit.proj_duration_start.data
        if project_form_edit.proj_duration_end.data:
            project_obj.proj_duration_end = project_form_edit.proj_duration_end.data 
        if project_form_edit.project_finished.data:
            project_obj.project_finished = project_form_edit.project_finished.data
        if project_form_edit.company_name.data:
            project_obj.company_name = project_form_edit.company_name.data
        if project_form_edit.company_email.data:
            project_obj.company_email = project_form_edit.company_email.data
        if project_form.attachment.data:
            project_obj.attachment = process_file(project_form.attachment.data)

        db.session.commit()
        flash("Successful","success")

    return render_template("project_form_edit.html",project_form=project_form)


@app.route('/search', methods=['GET'])
def search_in_table():

    apps_obj = App_Info()

    search_value = request.args.get('search_value')
    table_name = "app_info"  # request.args.get('table_name')

    # Database connection parameters
    db_config = {
        'user': 'root',
        'password': 'tmazst41',
        'host': 'localhost',  # or your MySQL server address
        'database': 'eswatini_apps_db'
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Use parameters to avoid SQL injection
    query = f"SELECT * FROM `{table_name}` WHERE CONCAT(COALESCE(name, ''), COALESCE(company_name, ''), COALESCE(app_category, ''), COALESCE(platform, ''))  LIKE %s"
    cursor.execute(query, ('%' + search_value + '%',))
    rows = cursor.fetchall()

    # Print results for debugging
    for row in rows:
        print("Car Make: ", row)

    # Convert the results to a list of dictionaries (depending on your needs)
    apps = [{'id': row[0], 'cid': row[1], 'name': row[2], 'description': row[3], 'app_category': row[4], 
             'platform': row[5], 'version_number': row[6], 'playstore_link': row[7], 'ios_link': row[8],'uptodown_link': row[9],
               'facebook_link': row[10], 'whatsapp_link': row[11], 'x_link': row[12],'linkedin_link': row[13], 'youtube_link': row[14], 'web_link': row[15],
            'github_link': row[16], 'app_icon': row[17], 'publish': row[18],'approved': row[19], 'timestamp': row[20], 'company_name': row[21],
            'company_contact': row[22],'company_email': row[23],} for row in rows]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return render_template('search_results.html', apps_obj=apps_obj, apps=apps,search_value=search_value)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


