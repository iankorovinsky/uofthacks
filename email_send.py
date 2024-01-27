import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

def send_emails(name_email_dict, names, email_text, email_subject, sender_email, password):
    # Connect to the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)

        for name in names:
            if name in name_email_dict:
                receiver_email = name_email_dict[name]

                # Create the email
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = email_subject

                # Add the email body
                message.attach(MIMEText(email_text, 'plain'))

                # Send the email
                server.sendmail(sender_email, receiver_email, message.as_string())
                print(f"Email sent to {name} at {receiver_email}")
            else:
                print(f"No email found for {name}")

# Example usage
name_email_dict = {
    "Ian": os.environ['IAN_EMAIL'],
    "Lucy": os.environ['LUCY_EMAIL'],
    "William": os.environ['WILLIAM_EMAIL'],
    "Stephen": os.environ['STEPHEN_EMAIL']
}

names = ["John Doe", "Jane Smith"]
email_text = "This is a test email."
email_subject = "Test Email"
sender_email = os.environ['SERVER_EMAIL']  # Replace with your email
password = os.environ['SERVER_PASSWORD']  # Replace with your email password

send_emails(name_email_dict, names, email_text, email_subject, sender_email, password)
