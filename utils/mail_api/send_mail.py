from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from data.config import MAIL, MAIL_PASSWORD


def send_mail(to, message, subject):
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 587)
    server_ssl.ehlo()
    server_ssl.starttls()
    server_ssl.login(MAIL, MAIL_PASSWORD)
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(MAIL, to, message)
    # server_ssl.quit()
    server_ssl.close()