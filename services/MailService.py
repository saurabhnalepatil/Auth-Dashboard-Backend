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

            html_content_formatted = html_content.format(
                username=user_name, email=receiver_email, password=password
            )

            html_part = MIMEText(html_content_formatted, "html")
            message.attach(html_part)

            smtp_server.sendmail(self.sender_email, receiver_email, message.as_string())
            smtp_server.quit()

            self.logger.info("Email sent successfully!")
        except Exception as e:
            self.logger.error(
                "An error occurred while sending the email:", exc_info=True
            )


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
        .template {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}

        .container {{
            max-width: device-width;
            min-width: calc(100% - 70%);
            background-color: white;
            padding: 20px;
            border: 7px solid gray;
            border-style: groove;
            text-align: center;
        }}

        .container img {{
            height: 250px;
            width: 250px;
        }}

        .container button {{
            padding: 10px 20px;
            background-color: rgb(0, 255, 170);
            border: none;
            font-size: 15px;
            border-radius: 10px;
        }}

        .footer {{
            margin-top: 20px;
            font-size: 14px;
        }}
        .footer a {{
            margin: 0 5px;
            text-decoration: none;
        }}
        .footer a img{{
            height: 40px;
            width: 40px;
        }}
        .footer a:hover {{
            color: darkblue;
        }}
    </style>
</head>
<body>
    <div class="template">
        <div class="container">
            <img src="https://drive.google.com/thumbnail?id=1fsPrjMj-4fsNknOwIvjupSzc-op5heih" alt="">
            <h1>Verification Code</h1>
            <p>Hello, [Username]!</p>
            <p>Please use the following credentials to sign in:</p>
            <p>Username: [Email]</p>
            <p>Password: <strong>[Password]</strong></p>
            <button><strong>Reset my password</strong></button>
            <p>If you did not request this, you can ignore this email.</p>
            <p>Thanks,<br>The Team</p>
            <div class="footer">
                <p>Follow us on social media</p>
                <a href="https://www.facebook.com/profile.php?id=61556388266304" target="_blank"
                    class="text-white px-2">
                    <img class="social-icon" src="https://img.icons8.com/3d-fluency/188/facebook-circled.png"
                        alt="facebook-circled" loading="lazy" />
                </a>
                <a href="https://www.instagram.com/invites/contact/?i=y2g5u5sly94a&utm_content=tmb1mkp"
                    class="text-white px-2" target="_blank">
                    <img class="social-icon" src="https://img.icons8.com/3d-fluency/94/instagram-new.png"
                        alt="instagram-new" loading="lazy" />
                </a>
                <a href="https://www.linkedin.com/company/99411614/admin/feed/posts/" class="text-white px-2"
                    target="_blank">
                    <img class="social-icon" src="https://img.icons8.com/3d-fluency/94/linkedin.png" alt="linkedin" />
                </a>
                <a href="https://twitter.com" class="text-white px-2" target="_blank">
                    <img class="social-icon" src="https://img.icons8.com/3d-fluency/94/twitter-circled.png" alt="twitter-circled" />
                </a>
                <p>Copyright &copy; 2024 YourCompany. All rights reserved.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
"""
