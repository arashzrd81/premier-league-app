from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Error import Error



# SendEmail class
class SendEmail():

    # sendEmail method that does send email operation
    def sendEmail(self, **kwargs):
        message = MIMEMultipart()

        # information needed to send email
        email = "PremierLeagueApp.v1@gmail.com"
        password = "<secret>"
        message["from"] = "Premier League App"
        message["to"] = kwargs["email"]
        message["subject"] = kwargs["subject"]

        # if subject was Verify Code, should set the message related to verify code
        if kwargs["subject"] == "Verify Code":
            message.attach(MIMEText("Hi %s, Welcome To Premier League App.\n\n" %kwargs["username"]))
            message.attach(MIMEText("Verify Code: %s" %kwargs["verifyCode"]))

        # if subject was Change Password, should set the message related to change password
        elif kwargs["subject"] == "Change Password":
            message.attach(MIMEText("Hi %s, Your account password in Premier League app was changed successfully." %kwargs["username"]))

        # if subject was Delete Account, should set the message related to delete account
        else:
            message.attach(MIMEText("Hi %s, Your Premier League App account has been successfully deleted.\n" %kwargs["username"]))
            message.attach(MIMEText("We hope you are satisfied with Premier League App :)"))

        try:
            # connect to server and send email
            with SMTP(host="smtp.gmail.com", port=587) as server:
                server.ehlo()
                server.starttls()
                server.login(email, password)
                server.send_message(message)
        except:
            obj = Error()
            obj.showError()