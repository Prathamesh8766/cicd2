import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_mail(workflow_name, repo_name, workflow_run_id):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not all([sender_email, sender_password, receiver_email]):
        print("Error: Missing environment variables.")
        return

    subject = f"Workflow {workflow_name} in repo {repo_name} failed"
    body = f"Hi,\n\nWorkflow '{workflow_name}' from repo '{repo_name}' has failed. For more details, please check the logs.\n\nMore Details: {workflow_run_id}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject    
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Call function with environment variables
send_mail(os.getenv("WORKFLOW_NAME"), os.getenv("REPO_NAME"), os.getenv("WORKFLOW_RUN_ID"))