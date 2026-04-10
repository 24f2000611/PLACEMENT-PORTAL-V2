from celery import shared_task 
from Backend.models import *
from datetime import datetime,timedelta 
import csv ,os 
from flask_mail import Message 
from Backend.extension import mail

# Daily reminders 
@shared_task(ignore_result=True)
def send_interview_reminders():
    tomorrow = (datetime.utcnow().date() + timedelta(days=1)).strftime("%Y-%m-%d")
    upcoming_interviews = Placement.query.filter(db.func.date(Placement.interview_date)==tomorrow).all()
    
    count =0
    for interview in upcoming_interviews:
        student_email = interview.application.student.user_stu.email
        student_name = interview.application.student.user_stu.username
        company_name= interview.application.drive.company.user_comp.username
        time_formatted = interview.interview_date.strftime("%I:%M %p")

        msg = Message(
            subject = f"Reminder:Interview with {company_name} Tomorrow !",
            recipients= [student_email],
            body =f"Hello \n\nThis is a reminder that you have an interview scheduled with {company_name} tomorrow at {time_formatted}.Role:{interview.application.drive.job_title} Location:{interview.application.drive.location}",

        )
        mail.send(msg)
        count+=1
    return f"Sent {len(upcoming_interviews)} reminders"



# Monthly reports 
@shared_task(ignore_result = True)
def generate_monthly_reports():
    companies = Company.query.all()
    current_month = datetime.utcnow().strftime("%B %Y")

    for company in companies:
        company_email = company.user_comp.email
        company_name = company.user_comp.username
        total_drives = len(company.drives)
        total_applicants = 0
        total_selected = 0

        for drive in company.drives:
            total_applicants += len(drive.application_rel)
            for app in drive.application_rel:
                if app.status=='Selected':
                    total_selected+=1
        filename = f"Monthly_report_{company_name}.csv"
        filepath = os.path.join("Backend","exports",filename)

        with open(filepath,mode='w' ,newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Metric', 'Count'])
            writer.writerow(['Total Active/Past Drives', total_drives])
            writer.writerow(['Total Student Applications Received', total_applicants])
            writer.writerow(['Total Candidates Selected', total_selected])

        msg = Message(
            subject =f"Placement Analysis Report - {current_month}",
            recipients= [company_email],
            body = f"""Welcom {company_name} Your monthly reported is attached below.
            * Total Active/Past Drives :{total_drives}
            * Total Student Application Received :{total_applicants}
            * Total Candidates Selected :{total_selected}
            
            """
        )
        with open(filepath,"rb") as fp:
            msg.attach(filename,"text/csv",fp.read())

        mail.send(msg)

    return "Monthly report generated successfully."


# User Triggered export

# @shared_task()
# def export_user_data(user_id,role):
#     filename= f"export_{role}_{user_id}.csv"
#     filepath = os.path.join("Backend/exports",filename)
#     import time
#     time.sleep(5)

#     with open(filepath,mode='w', newline='') as file:
#         writer = csv.writer(file)
#         if role =='student':
#             writer.writerow(['Drive Title','Company','Status','Date Applied'])
#             apps = Application.query.filter_by(student_id = user_id).all()

#             for app in apps:
#                 writer.writerow([app.drive.job_title,app.drive.company.user_comp.username,app.status,app.date_applied])

#         elif role =='company':
#             writer.writerow(['Drive Title','Total Applicants','Status'])
#             drives = PlacementDrive.query.filter_by(c_id=user_id).all()
#             for d in drives:
#                 writer.writerow([d.job_title,len(d.application_rel),d.post_status])
#     return filepath