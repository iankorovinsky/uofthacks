import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

global name_email_dict

def init():
    global name_email_dict
    name_email_dict = {
        "Ian": os.environ['IAN_EMAIL'],
        "Lucy": os.environ['LUCY_EMAIL'],
        "William": os.environ['WILLIAM_EMAIL'],
        "Stephen": os.environ['STEPHEN_EMAIL']
    }


def send_emails(name_email_dict, names, link, email_subject, sender_email, password):
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
                email_text = f"""
                <html>
                <body>
                    <p>Hey there {name}! 👋<br><br>
                    You've got a new memory waiting to be relived, now minted securely on the blockchain with Nostalg.ai. 🧠<br><br>
                    Click here to <a href="{link}">view your memory</a>.<br><br>
                    ✨ Thanks for using Nostalg.ai! ✨<br><br>
                    Cheers,<br>
                    Nostalg.ai Team
                    </p>
                </body>
                </html>
                """
                message.attach(MIMEText(email_text, 'html'))

                # Send the email
                server.sendmail(sender_email, receiver_email, message.as_string())
                print(f"Email sent to {name} at {receiver_email}")
            else:
                print(f"No email found for {name}")

def email_request(names, link):
    global name_email_dict
    email_subject = "📷 New Memory w/ Nostalg.ai 📷"
    sender_email = os.environ['SERVER_EMAIL']  # Replace with your email
    password = os.environ['SERVER_PASSWORD']  # Replace with your email password

    send_emails(name_email_dict, names, link, email_subject, sender_email, password)

init()
email_request(["Ian"], "https://goerli.etherscan.io/nft/0xb91876637e407b75fc5da1a81114db68f4851932/53337")
