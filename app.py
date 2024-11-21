
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify,send_from_directory
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
import json
import time
# import sqlite3
# import pymysql
# import pyodbc



#Change App
app = Flask(__name__)
app.config['SECRET_KEY'] = "sdsdjfe832j2rj_32j"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project_assistant_db.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:tmazst41@localhost/techtlnf_project_assistant" #?driver=MySQL+ODBC+8.0+Driver"
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

if os.path.exists('client.json'):
    with open('client.json') as file:

        creds = json.load(file)

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


class user_class:
    s = None

    def get_reset_token(self, c_user_id):

        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': c_user_id, 'expiration_time': time.time() + 300}).encode('utf-8')

    @staticmethod
    def verify_reset_token(token, expires=1800):

        s = Serializer(app.config['SECRET_KEY'], )

        try:
            user_id = s.loads(token, max_age=300)['user_id']
        except itsdangerous.SignatureExpired:
           return jsonify({"Error":'Token has expired, Please Create a New Token'})
        except itsdangerous.BadSignature:
            return jsonify({"Error":'A Mismatch is Detected, Please Try Again'})
        except:
            return jsonify({"Error":'Something Wrong, Please start afresh the process'})
         
        return user_id

#Password Encryption
encrypt_password = Bcrypt()

ser = Serializer(app.config['SECRET_KEY']) 

#Populating variables across all routes
@app.context_processor
def inject_ser():
     # Define or retrieve the value for 'ser'

    return dict(ser=ser)



@app.route("/", methods=['POST','GET'])
def home():

    with app.app_context():
        db.create_all()

    return render_template("index.html")


def send_pat():

    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] ='pro.dignitron@gmail.com' # creds.get('email') # os.getenv("MAIL")  
        pwd = app.config["MAIL_PASSWORD"] =   creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)
        ser = Serializer(app.config['SECRET_KEY']) 
        # token = ser.dumps({"data":user.id})

        # try:
        #     db.session.add(App_Access_Credits(app_id=user.id,token=token))
        #     db.session.commit()

        # except IntegrityError:
        #     db.session.rollback()
        
        msg = Message(subject="Greetings and Exciting News About My New Project", sender="no-reply@gmail.com", recipients=["pat@starterstory.com",'pro.dignitron@gmail.com'])

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
              <div style="flex-direction: ;margin-bottom:-10px" class="topic-con container">
                <div style="font-weight:600;font-size: 25px;color:#5f2364" class="topic"> Greetings and Exciting News About My New Project!
                </div>
              </div>
            </div>
            
            <!-- Subject  -->
  
            <!-- Body Message  -->
            <section style="flex-wrap: nowrap;" class="padding:10px">
                
                <div style="width:80%;margin:10px auto" class="content objectives">
                    
                    <!-- Greeting Message  -->
                <h3 style="color:#00a550;">Good day, Pat</h3>
                 <div style="color:rgb(53, 53, 53)">
                    I hope this message finds you well! I am Thabo Maziya, I want to personally thank you for the emails you sent through – they have truly inspired me. Your Starter Story interviews are also an inspiration as well and have energized my entrepreneurial spirit to push forward even harder.
                 </div><br>
                <div style="color:rgb(53, 53, 53)">
                   As someone with aspirations to join the SS Academy, I find myself in a challenging position due to limited resources at the moment. However, I remain hopeful that I will be able to take that step soon.
                 </div><br>
                <div style="color:rgb(53, 53, 53)">
                   With over five years of experience, I create web applications and produce graphic design artwork for my clients. I’m continuously working towards organizing my ecosystem to enhance my offerings.
                 </div><br>
                    
                <div style="color:rgb(53, 53, 53)">
                   <b>Moreover,</b> I am excited to share with you that I am currently working on a new project called "Your Project Assistant."Suprisingly! you're the first one to know about this project. This initiative aims to support developers and designers by providing comprehensive reviews and hands-on assistance for their projects. I specialize in identifying common issues such as broken links, missing images, layout problems, and more. Clients can expect detailed reports filled with screenshots and direct URLs, which makes resolving any issues easier and faster.
                 </div><br>
                    <div style="margin:20px auto;width:font-weight:600;"><span style="font-weight:500;"></span>
                        <a href="https://assistant.techxolutions.com" target="_blank">
                    <span style="background-color: #00a550;color:white;padding:5px 10px;
                                 border-radius: 15px;font-weight: 600;font-size: 16px; border-radius: 15px;">Visit Site</span></a></div><br>
                    
                <div style="color:rgb(53, 53, 53)"> Regarding compensation, I calculate payments at the end of each day after consolidating all completed tasks. Charges typically start at a minimum of $5.00, and in some cases, I may perform smaller tasks at no charge at my discretion. I am also open to discussions if you'd prefer a different approach to align with your project needs.
                </div><br>

                    
                <div style="color:rgb(53, 53, 53)"> If you have any insights or could connect me with others who might benefit from my services, I would greatly appreciate your assistance. I truly value your experience and perspective in this industry.
                </div><br>
                    
                <div style="color:rgb(53, 53, 53)"> Thank you once again for the inspiration, and I look forward to hearing from you soon!
                </div><br>
                
                <div style="color:rgb(53, 53, 53)"> Visit my website <a href="https://assistant.techxolutions.com" target="_blank">"Your Project Assistant"</a> to learn more about my services and take action today! Let’s enhance your project’s quality together.
                </div><br>
                     
                    
                <!-- Footer / Email Signature -->
                </div><br><br>
                <p  class="">Kind Regards,</p> 
                <table style="font-size: medium;flex-wrap:nowrap;background-color: #f1f1f1;width:100% !important" class="email-sign-cont ">
                    <tr style="font-size: medium;flex-wrap:nowrap;width:100% !important" >
                        <td style="vertical-align: top;" class="sign-column">
                            <span style="font-size: large;font-weight: 600;color:#606060">Thabo Maziya,
                            <div class="mail-links"><a href="https://assistant.techxolutions.com" target="_blank">Your Project Assistant</a></div>
                            <div class="mail-links"><img style="height:25px" src="https://techxolutions.com/images/email_icon.png"/><span>thabo@techxolutions.com</span></div>
                            <div class="mail-links"><img style="height:25px" src="https://techxolutions.com/images/telephone_icon.png"/><span>(+268) 7641 2255</span></div>
                             <div class="mail-links"><img style="height:25px" src="https://pngtree.com/free-png-vectors/whatsapp-icon.png"/><span>(+268) 7641 2255</span></div>
                        </td>
                        
                    </tr>
                </table><br><br>
                
            </section>
            <div style="" class="email-signature">

            </div>
        </div>
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

@app.route("/send_pat", methods=['POST','GET'])
def email_pat():

    send_pat()

    return jsonify({"Success!":f"Mail Sent Successfully!"})


def send_prospects(name,email):
   
    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email') # os.getenv("MAIL")  'pro.dignitron@gmail.com'
        pwd = app.config["MAIL_PASSWORD"] =   creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)
        ser = Serializer(app.config['SECRET_KEY']) 
        # token = ser.dumps({"data":user.id})

        # try:
        #     db.session.add(App_Access_Credits(app_id=user.id,token=token))
        #     db.session.commit()

        # except IntegrityError:
        #     db.session.rollback()
        
        msg = Message(subject="Your Project Assistant", sender="no-reply@gmail.com", recipients=[email,'pro.dignitron@gmail.com'])

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
                <div style="font-weight:600;font-size: 25px;color:#5f2364" class="topic"> Enhance Your Project's Quality with My Assistance!
                </div>
              </div>
            </div>
            
            <!-- Subject  -->
  
            <!-- Body Message  -->
            <section style="flex-wrap: nowrap;" class="padding:10px">
                
                <div style="width:100%;margin:10px auto" class="content objectives">
                    
                <!-- Greeting Message  -->
                <h3 style="color:#00a550;">Good day, {name}</h3>
                <div style="color:rgb(53, 53, 53)">
                    Are you feeling the crunch of impending deadlines? Do you want to ensure the highest quality in your projects without the stress? Look no further! I'm here to help streamline your workflow and enhance the quality of your work.
                    If you're employed and working on side projects, and if your work duties are becoming overwhelming, I can provide support to help organize your current ecosystem.
                 </div><br>
                    
                <div style="color:rgb(53, 53, 53)">
                   <b>Why Choose My Services?</b> With comprehensive reviews and hands-on assistance tailored to your needs, I specialize in identifying common issues such as broken links, missing images, layout problems, and more. You can expect detailed reports filled with screenshots and direct URLs, making it easier for you to address any issues swiftly.
                 </div><br>
                <div style="margin:20px auto;width:font-weight:600;"><span style="font-weight:500;"></span>
                        <a href="https://assistant.techxolutions.com" target="_blank">
                    <span style="background-color: #00a550;color:white;padding:5px 10px;
                                 border-radius: 15px;font-weight: 600;font-size: 16px; border-radius: 15px;">Visit Site</span></a></div><br>
                <div style="color:rgb(53, 53, 53)"> Payments are calculated at the of each day after consolidating every tasks completed. The charges starts at the minimum of <b>$5.00</b>  upwards
                    and some small tasks can be perfomed at <b>$0</b> fee at my discretion. I am open to discussions if you may prefer a different approach aligned with your project needs.
                </div><br>

                    
                <!-- Sub Topic  -->
                <h2 style="color:coral">What I Can Help You With:</h2>
<!--
                    <div style="color:rgb(53, 53, 53)">Here are the login details that you will need to create assignments or tasks for the current project. The project will be broken down into assignments (tasks) to provide more flexibility and clarity.
                </div>
-->
                <p style="vertical-align: top;"><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Find Broken Links: </span><span >Ensure all your links are functional and accurate.
                    </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Solve Formatting Issues: </span> <span> Get your text and visuals perfectly aligned.
                </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Layout Problems: </span> <span> Fix issues with misaligned graphics or blurry images.
                </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Improper Element Alignment: </span> <span> Create a clean, professional presentation.
                </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Spelling and Grammar Checks: </span> <span> Polish your content with error-free text.
                </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Optimize Images: </span> <span> Reduce load times by addressing overly large images.
                </span></p>
                 <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Responsive Design Testing: </span> <span> Ensure your project looks great on any device.
                </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">User Experience Insights: </span> <span> Gain feedback to enhance usability.
                </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Design Manuals: </span> <span> Create comprehensive guides for your software applications.
                </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">Graphic Design Assistance: </span> <span> Get help with icon creation and other design tasks.
                </span></p>
                <p><span><img style="height:20px" src="https://techxolutions.com/images/tick-icon.png" /></span>
                    <span style="font-weight:600">And more! </span> <span>
                </span></p>
                    
                <div style="color:rgb(53, 53, 53)"> By focusing on what matters most, you can reduce project deadline headaches and deliver exceptional results. Let me take care of these details so you can dedicate your time to aligning your vision with your project goals.
                </div><br>
                
                <div style="color:rgb(53, 53, 53)"> Ready to get started? You contact me directly or Visit my website <a href="https://assistant.techxolutions.com" target="_blank">"Your Project Assistant"</a> to learn more about my services and take action today! Let’s enhance your project’s quality together.
                </div><br>
                     
                    
                <!-- Footer / Email Signature -->
                </div><br><br>
                <p  class="">Kind Regards,</p> 
                <table style="font-size: medium;flex-wrap:nowrap;background-color: #f1f1f1;width:100% !important" class="email-sign-cont ">
                    <tr style="font-size: medium;flex-wrap:nowrap;width:100% !important" >
                        <td style="vertical-align: top;" class="sign-column">
                            <span style="font-size: large;font-weight: 600;color:#606060">Thabo Maziya,</span>
                            <div class="mail-links"><a href="https://assistant.techxolutions.com" target="_blank">Your Project Assistant</a></div>
                            <div class="mail-links"><img style="height:25px" src="https://techxolutions.com/images/email_icon.png"/><span>thabo@techxolutions.com</span></div>
                            <div class="mail-links"><img style="height:25px" src="https://techxolutions.com/images/telephone_icon.png"/><span>(+268) 7641 2255</span></div>
                           
                        </td>
                        
                    </tr>
                </table><br><br>
                
            </section>
            <div style="" class="email-signature">

            </div>
        </div>
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

@app.route("/send_prospects", methods=['POST','GET'])
def email_prospects():
    email_form = SendEmailForm()

    if request.method == "POST":
        name = email_form.name.data
        email = email_form.emails.data

        if email and name:
            send_prospects(name,email)
        else:
            return jsonify({"Error":f"Make Sure You Enter Valid Name and Email Address"})

    return render_template("send_prospects.html",email_form=email_form)

def send_email(user,passw):
    
    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email') # os.getenv("MAIL")  'pro.dignitron@gmail.com'
        pwd = app.config["MAIL_PASSWORD"] =   creds.get('gpass') #os.getenv("PWD")
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
    proj_assigns = Assignment.query.filter_by(uid=current_user.id).all()
    access=False
    flash(f"Here You will find all reports about prevoius Jobs/Tasks",'success')

    return render_template("assigns_n_reports.html",report=reports,proj_assigns=proj_assigns,project=project,access=access)

@app.route("/all_assignments")
def all_assignments():

    auth = request.args.get('auth')
    access=True

    if auth == 'tmazst':
        project = Project_Description
        reports = Project_Reporting
        proj_assigns = Assignment.query.all()
    else:
        return jsonify({'Error':'Wrong auth key'})

    return render_template("assigns_n_reports.html",report=reports,proj_assigns=proj_assigns,project=project,access=access)


@app.route("/project_assignments")
@login_required
def project_assignments():

    project_info = Project_Description.query.get(ser.loads(request.args.get("pid"))['data'])

    project = Project_Description
    reports = Project_Reporting
    proj_assigns = Assignment.query.filter_by(uid=current_user.id,pid=project_info.id).all()

    return render_template("project_assignments.html",report=reports,proj_assigns=proj_assigns,project=project,project_info=project_info)


@app.route("/project_reports")
@login_required
def projects():

    projects = Project_Description.query.filter_by(uid=current_user.id).all()
    view_details = False
    flash(f"Hey {current_user.name}, Here You will find the current & previous Jobs/Tasks you assigned",'success')

    return render_template("projects.html",projects=projects,view_details=view_details)


@app.route("/assitant_sitemap.xml")
def sitemap():
    
    return send_from_directory(application.static_folder,"assistant_sitemap.xml")


@app.route("/robot.txt")
def sitemap():
    
    return send_from_directory(application.static_folder,"robot.txt")

# @app.route("/send_email", methods=['POST','GET'])
# def email():
#     app_name_rq = None
#     email_form = SendEmailForm()

#     if request.method == "POST":
#         app_name = email_form.app_name.data

#         if app_name:
#             app_name_rq = App_Info.query.filter_by(name=app_name).first()

#         if app_name_rq:
#             send_email(app_name_rq)
#         else:
#             return jsonify({"Error":f"App Name {app_name_rq} Does Not Exists in the System"})

#     return render_template("send_email.html",email_form=email_form)


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

@app.route("/signup", methods=["POST","GET"])
def signup():
    register = UserForm()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':

        if register.validate_on_submit():    

            hashd_pwd = encrypt_password.generate_password_hash(register.password.data).decode('utf-8')

            user = User(name=register.name.data, email=register.email.data, password=hashd_pwd,
                    confirm_password=hashd_pwd,image="default.jpg",contacts=register.contacts.data,
                    timestamp=datetime.now(),role = 'user')

            # try:
            if not UserForm().validate_email(register.email.data):
                db.session.add(user)
                db.session.commit()
                print('Sign up successful!')
                flash(f"Account Successfully Created for {register.name.data}", "success")
            else:
                return jsonify({'Error':'Email Already Exists'})
            
            return redirect(url_for('login'))

        elif register.errors:
            print(register.errors)
            return jsonify({'Error':'Please Check If You Correctly Your Signup'})
            

    return render_template("signup.html",register=register)


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
                    # # print("Creditantials are ok")
                    # print("No Verification Needed: ", user_login.verified)
                    # req_page = request.args.get('next')
                    # flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                    # return redirect(req_page) if req_page else redirect(url_for('projects'))
                    # if user_login:
                    if not user_login.verified:
                        return redirect(url_for('verification'))
                    else:
                        # After login required prompt, take me to the page I requested earlier
                        print("No Verification Needed: ", user_login.verified)
                        req_page = request.args.get('next')
                        flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                        return redirect(req_page) if req_page else redirect(url_for('projects'))
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


@app.route("/verification", methods=["POST", "GET"])
# User email verification @login
# @login the user will register & when the log in the code checks if the user is verified first...
def verification():

    usr_ = User.query.get(current_user.id)

    def send_veri_mail():
        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email')  # os.getenv("MAIL")
        app.config["MAIL_PASSWORD"] =  creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        token = user_class().get_reset_token(current_user.id)
        usr_email = usr_.email

        msg = Message(subject="Email Verification", sender="no-reply@gmail.com", recipients=[usr_email])

        msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
            <!-- Header Title  -->
            <div class="header">
              <div style="flex-direction: ;" class="topic-con container">
                <div style="font-weight:600;font-size: 25px;color:#5f2364" class="topic"> Thank You for Your Account Activation!
                </div>
              </div>
            </div>
        <h2>Hi, {usr_.name}</h2>

        <p>Please use the link below to verify your email address.</p>
        <p>Thank you for opening an account with me! I am excited to assist you and look forward to providing you with the best technical support possible.</p>
        <p style="font-weight:600">Verification link;</p>
        <a href="{ url_for('verified', token=token, _external=True) }" 
            style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #4CAF50; 
                    border: none; border-radius: 15px; text-decoration: none; text-align: center;">
            Verify Email
        </a>
        <p class="footer">Your Project Assistant</p>
    </div>
</body>
</html>
"""
        # try:
        mail.send(msg)
        flash(f'An email has been sent with a verification link to your email account', 'success')
        log_out()
    try:
        if not usr_.verified:
            send_veri_mail()
        else:
            return redirect(url_for("home"))
    except:
        # flash(f'{usr_.email} Something went wrong', 'error')
        return redirect(url_for("login"))

    return render_template('verification.html')


@app.route("/verified/<token>", methods=["POST", "GET"])
# Email verification link verified with a token
def verified(token):
    # Check to verify the token received from the user email
    # process the user_id for the following script
    user_id = user_class.verify_reset_token(token)

    try:
        usr = User.query.get(user_id)
        usr.verified = True
        db.session.commit()
        if usr.verified:
            qry_usr = User.query.get(user_id)
            if not current_user.is_authenticated:
                login_user(usr)
            flash(f"You're Welcome, {qry_usr.name}", "success")
            return redirect(url_for('projects'))
    except Exception as e:
        flash(f"Something went wrong, Please try again ", "error")

    return jsonify({"Verification":"Verification Failed!"})


@app.route("/report_form", methods=['POST','GET'])
def report():

    project_assn = None
    report_form = ProjectReportingForm()

    if request.args.get("assid"):
        project_assn =Assignment.query.get(ser.loads(request.args.get("assid"))['data'])
        print("Assign: ", project_assn)

    #Pending PID
    if request.method == "POST":#and app_form.validate_on_submit()
        assignment=Assignment.query.get(ser.loads(request.args.get("assid"))['data'])
        report_info = Project_Reporting(
            report=report_form.report.data, comments=report_form.comments.data,  price=report_form.price.data, 
            pending=report_form.pending.data, pending_payment=report_form.pending_payment.data,  status=report_form.status.data,
            date_finished=report_form.date_finished.data,uid=assignment.uid,assignid=assignment.id
            # url = report_form.url.data
        )

        # report_info = Project_Reporting(
        #      report=report_form.report.data, comments=report_form.comments.data,  price=report_form.price.data, 
        #      pending=report_form.pending.data, pending_payment=report_form.pending_payment.data,  status=report_form.status.data,
        #      date_finished=report_form.date_finished.data,uid=project.uid,pid=project.id,
        #      url = report_form.url.data
        # )

        if report_form.rep_img1.data:
            report_info.rep_img1 = process_file(report_form.rep_img1.data)
        if report_form.rep_img2.data:
            report_info.rep_img2 = process_file(report_form.rep_img2.data)
        if report_form.rep_img3.data:
            report_info.rep_img3 = process_file(report_form.rep_img3.data)

        db.session.add(report_info)
        db.session.commit()
        flash("Successful","success")

    return render_template("report_form.html",report_form=report_form,project_assn=project_assn,usr=User)


@app.route("/assignment_form", methods=['POST','GET'])
@login_required
def assignment():

    
    project = Project_Description.query.get(ser.loads(request.args.get("pid"))['data'])

    if current_user.id != project.uid:
        flash("Here are your projects listed below","error")

        return redirect(url_for("projects"))

    asignment_form = AssignmentForm()
    #Pending PID
    if request.method == "POST" :#and app_form.validate_on_submit()
        assignment_info = Assignment(
            assignment = asignment_form.assignment.data,url = asignment_form.url.data, status = asignment_form.status.data,
            pid=project.id,timestamp=datetime.now(),uid=project.uid
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

@app.route('/all_jobs')
def all_jobs():

    projects = Project_Description.query.all()
    if current_user.is_authenticated:
        projects = Project_Description.query.filter_by(uid=current_user.id).all()
    view_details = True

    return render_template("projects.html",projects=projects,view_details=view_details)

@app.route('/mini-dash')
def minidashboard():

    return render_template('mini-dashboard.html')

    projects = Project_Description.query.all()
    if current_user.is_authenticated:
        projects = Project_Description.query.filter_by(uid=current_user.id).all()
    view_details = True

    return render_template("projects.html",projects=projects,view_details=view_details)

@app.route("/project_form", methods=['POST','GET'])
@login_required
def project_form():

    project_form = ProjectForm()

    if request.method == "POST":#and app_form.validate_on_submit()
        project_info = Project_Description(
            proj_name = project_form.proj_name.data,description = project_form.description.data, proj_assistance = project_form.proj_assistance.data,
             proj_duration_start = project_form.proj_duration_start.data,
            proj_duration_end = project_form.proj_duration_end.data,timestamp=datetime.now(),
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
        # print("Check User1: ",User.query.filter_by(email=project_form.company_email.data).first())
        # if not User.query.filter_by(email=project_form.company_email.data).first():
        #     #generate password
        #     passw = pass_gen()
        #     hashd_pwd = encrypt_password.generate_password_hash(passw).decode('utf-8')
        #     sign_up_usr = User(name = project_form.company_name.data, email=project_form.company_email.data,password=hashd_pwd,confirm_password=hashd_pwd)
        #     db.session.add(sign_up_usr)
        #     db.session.commit()

        #     #Query user to get email and id
        #     user = User.query.filter_by(email=project_form.company_email.data).first()
        #     # assign user.id to project.uid for the current project 
        #     project = Project_Description.query.filter_by(company_email=user.email).first()
        #     project_info.uid = user.id
        #     db.session.add(project_info)
        #     db.session.commit()
        #     print("Registered User was not Reg: ",project_form.company_email.data, 'pass: ',passw)
        #     send_email(user,passw)
            
        #     return redirect(url_for("login_details"))
        # else:
        #     user = User.query.filter_by(email=project_form.company_email.data).first()
        #     project_info.uid = user.id
        #     db.session.add(project_info)
        #     db.session.commit()
        #     print("Registered User was Reg: ",project_form.company_email.data)

        flash("Project Created Successfully","success")
        return redirect(url_for("projects"))

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


@app.route("/contact", methods=["POST", "GET"])
def contact_form():

    contact_form = Contact_Form()
    
    if request.method == 'POST':
       
        if contact_form.validate_on_submit():
            
            
            # Get user details through their email
            

            def send_link():
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = creds.get('email') #os.getenv("EMAIL")
                app.config["MAIL_PASSWORD"] = creds.get('gpass') # os.getenv("PWD")

                mail = Mail(app)

                # token = user_class().get_reset_token(usr_email.id)
                msg = Message("Inquiry Message", sender="noreply@demo.com", recipients=[em])
                msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <br>
        <h4>Name:       {contact_form.name.data}</h4>
        <h4>Email:      {contact_form.email.data}</h4>
        <h4>Contact:    {contact_form.contact.data}</h4>
        <h4>Message:</h4>
        <p> {contact_form.message.data}</p>

        
        <p class="footer"></p>
    </div>
</body>
</html>
"""

                try:
                    mail.send(msg)
                    flash('Email Successful Sent!', 'success')
                    return "Email Sent"
                except Exception as e:

                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"
        


            # Send the pwd reset request to the above email
            send_link()

            return redirect(url_for('home'))
        elif contact_form.errors:
            for error in contact_form.errors:
                flash(f"Error! Please Check the {error} Field", 'error')

    return render_template("contact.html", contact_form=contact_form,user=User)


@app.route("/reset/<token>", methods=['POST', "GET"])
def reset(token):

    reset_form = Reset()

    if request.method == 'POST':

        # try:

        usr_id = user_class().verify_reset_token(token)
        
        pass_reset_hash = encrypt_password.generate_password_hash(reset_form.new_password.data)
        usr_obj = User.query.get(usr_id)
        if usr_obj:
            usr_obj.password = pass_reset_hash
            usr_obj.confirm_password = pass_reset_hash
            db.session.commit()
        else:
            return jsonify({"Error":'Token has expired, Please Create a New Token'})

        flash(f"You have Successfully Changed your Password! You can now Login with your New Password", "success")

        return redirect(url_for("login"))
        # except:
        #     print("Password Reset Failed!!")
        #     flash(f"Password Reset Failed, Please try again later", "error")
        #     return f'Reset Failed, Try again later'

    return render_template("pass_reset.html", reset_form=reset_form)


@app.route("/forgot_password", methods=['POST', "GET"])
def reset_request():

    reset_request_form = Reset_Request()

    if current_user.is_authenticated:
        logout_user()

    if request.method == 'POST':
        if reset_request_form.validate_on_submit():
            # Get user details through their email
            usr_email = User.query.filter_by(email=reset_request_form.email.data).first()

            if usr_email is None:
                # print("The email you are request for is not register with T.H.T, please register first, Please Retry")
                flash("The email you are requesting a password reset for, is not registered, please register an account first",
                    'error')

                return redirect(url_for("reset_request"))

            def send_link(usr_email):
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = creds.get('email') #os.getenv("EMAIL")
                app.config["MAIL_PASSWORD"] = creds.get('gpass') # os.getenv("PWD")

                mail = Mail(app)

                token = user_class().get_reset_token(usr_email.id)
                msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[usr_email.email])
                msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <h2>Good day, {usr_email.name}</h2>

        <p>You have requested a password reset for your account.</p>
        <p style="font-weight:600">To reset your password, visit the following link;</p>
        <a href="{url_for('reset', token=token, _external=True)}" 
            style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #4CAF50; 
                    border: none; border-radius: 15px; text-decoration: none; text-align: center;">
            Reset
        </a>
        <p class="footer">If you did not request the above message please ignore it, and your password will remain unchanged.</p>
    </div>
</body>
</html>
"""

                try:
                    mail.send(msg)
                    flash('An email has been sent with instructions to reset your password', 'success')
                    return "Email Sent"
                except Exception as e:

                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"


            # Send the pwd reset request to the above email
            send_link(usr_email)

            return redirect(url_for('login'))

    return render_template("password_reset_req.html", reset_request_form=reset_request_form)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


