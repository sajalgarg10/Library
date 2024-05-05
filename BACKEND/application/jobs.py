from celery import Celery, Task
from flask  import current_app as app
from celery.schedules import crontab
from application.database import User , IssuedTo , db , Book , IssuedData
from datetime import datetime, timedelta


celery = Celery("Jobs", broker='redis://localhost:6379/1', backend='redis://localhost:6379/2' )
celery.conf.timezone = 'Asia/Kolkata'



        
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template

SMPTP_SERVER_HOST =  "127.0.0.1"
SMPTP_SERVER_PORT = 1025 
SENDER_ADDRESS = 'no-reply@library.com'
SENDER_PASSWORD = 'test'

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, 'html'))

    with smtplib.SMTP(host = SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT) as s:
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
    return True
    

def format_message(template_file, user):
        with open (template_file) as file_:
            template = Template(file_.read())
            message = template.render(data=user)
            return message
        
@celery.task(name="send_mail")
def mail():
    # get all the users
    users = User.query.all()
    # new_users = []
    for user in users:
        if datetime.now() - user.last_visit > timedelta(seconds=86400):
            email = user.username + "@library.com"
            name = user.username
            user_data = {"name": name, "msg": "You have not visited for a long time."}
            message = format_message("template/mail_daily.html", user_data)  # Updated file path
            send_email(email, subject="Today's Library Reminder", message=message)

        else:
            email = user.username + "@library.com"
            name = user.username
            user_data = {"name": name, "msg": "Thank you for visiting. Have a nice day!"}
            message = format_message("template/mail_daily.html", user_data)  # Updated file path
            send_email(email, subject="Today's Library Reminder", message=message)
    return "ok"

@celery.task(name="monthly_mail")
def monthly_mail():
    # get all the users
    books_hist = db.session.query(User.username,  IssuedData.issued_user , Book.name , IssuedData.issued_book).join(IssuedData, User.user_id == IssuedData.issued_user).join(Book, IssuedData.issued_book == Book.id).filter(IssuedData.date_issued >= (datetime.today() - timedelta(days=30))).all()
    user = set()
    mail_users = []
    for book in books_hist:
        if book[0] in  user:
            continue
        else:
            user.add(book[0])
            d= {}
            d["name"] = book[0]
            d["data"] = []
            mail_users.append(d)
    for i in mail_users:
        for j in books_hist:
            if i["name"] == j[0]:
                i["data"].append(j[2])
    for i in mail_users:
        email = i["name"] + "@library.com"
        message = format_message("template/monthly_mail.html", i)
        send_email(email, subject="Monthly Report", message=message)
    us =  User.query.all()
    for i in us:
        if i.username not in user:
            email = i.username + "@library.com"
            name = i.username
            user_data = {"name": name, "msg": "You have not issued any book. "}
            message = format_message("template/mail_daily.html", user_data)  # Updated file path
            send_email(email, subject="Monthly Report", message=message)


    return "ok"




@celery.task(name = "access_expire")
def access_expire():
    issued_books =   IssuedTo.query.all()
    for book in issued_books:
        if book.return_date < datetime.now():
            user = User.query.filter_by(user_id = book.issued_user).first()
            db.session.delete(book)
            user.number_of_books = user.number_of_books - 1
            print("kjdhkjdh")
    db.session.commit()  
    return "successful"    

        
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(10, mail.s(), name="send_mail")  
    #sender.add_periodic_task(10 , access_expire.s(), name="accees_expire")    
    sender.add_periodic_task(crontab(
         hour=22, minute=50, day_of_week="*"), mail.s(), name="send_mail") 
    sender.add_periodic_task( crontab(
        hour=23, minute=17, day_of_week="*"), access_expire.s(), name="accees_expire")
    sender.add_periodic_task( crontab(
        day_of_month=1 , hour=23, minute=17, day_of_week="*"), monthly_mail.s(), name="monthly_mail")

#crontab(hour=20, minute=0, day_of_week="*") crontab(
 #       hour=14, minute=25, day_of_week="*")
#  crontab(
#         hour=14, minute=25, day_of_week="*")

