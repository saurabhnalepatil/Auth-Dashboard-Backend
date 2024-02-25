import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from services.DbService import DbService


class MailService:
    def __init__(self):
        self.db = DbService()
        self.sender_email = os.environ.get("SENDER_EMAIL")
        self.sender_password = os.environ.get("SENDER_PASSWORD")
        self.logger = logging.getLogger(__name__)

    def send_email(self, user_name, password, receiver_email, subject):
        try:
            smtp_server = smtplib.SMTP("smtp.hostinger.com", 587)
            smtp_server.starttls() 
            smtp_server.login(self.sender_email, self.sender_password)

            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            html_content_formatted = html_content.format(username=user_name, email=receiver_email, password=password)

            html_part = MIMEText(html_content_formatted, "html")
            message.attach(html_part)

            smtp_server.sendmail(self.sender_email, receiver_email, message.as_string())
            smtp_server.quit()

            self.logger.info("Email sent successfully!")
        except Exception as e:
            self.logger.error("An error occurred while sending the email:", exc_info=True)


html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
    <style>
        /* Add your inline CSS styles here */
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }}
        .container {{
            max-width: 700px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border: 7px solid gray;
            border-style: groove;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Verification code</h1>
        <p>Hello, {username}!</p>
        <p>Please use the following credentials to sign in:</p>
        <p>Username: {email}</p>
        <p>Password: <strong>{password}</strong></p>
        <p>If you did not request this, you can ignore this email.</p>
        <p>Thanks,<br>The team</p>
    </div>
</body>
</html>
"""
