from smtplib import SMTP_SSL as SMTP  # this invokes the secure SMTP protocol (port 465, uses SSL)
import sys
from email.mime.text import MIMEText
from src.auth.config import username, password


# SMTPserver = 'smtp.gmail.com'
# sender = "project.synergy.info@gmail.com"
# destination = ['mever.ya@gmail.com']
#
# # typical values for text_subtype are plain, html, xml
# text_subtype = 'plain'
#
# content = """\
# Test message
# """
#
# subject = "david, priyatnogo appetita"

class MailSender:
    def __init__(self, smtp_server, username, password, sender):

        self.smtp_server = smtp_server
        self.username = username
        self.password = password
        self.sender = sender

    def send_mail(self, destination, subject, content, text_subtype='plain', sender=None):

        if not sender:
            sender = self.sender

        try:
            msg = MIMEText(content, text_subtype)
            msg['Subject'] = subject
            msg['From'] = sender  # some SMTP servers will do this automatically, not all

            conn = SMTP(self.smtp_server)
            conn.set_debuglevel(False)
            conn.login(self.username, self.password)
            try:
                conn.sendmail(sender, destination, msg.as_string())
            finally:
                conn.quit()
        except:
            sys.exit("mail failed; %s" % "CUSTOM_ERROR")


MS = MailSender(
    smtp_server="smtp.gmail.com",
    username=username,
    password=password,
    sender=username
)


