import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_host, smtp_port, username, password, recipients):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.recipients = recipients

    def create_message(self, subject, html_content):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ','.join(self.recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))
        return msg

    def send_email(self, message):
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, self.recipients, message.as_string())
                print("Email sent successfully")
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")