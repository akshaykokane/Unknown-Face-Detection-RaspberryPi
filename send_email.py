
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

  
def sendEmail(content):
    msg = MIMEText(content)
    msg['Subject'] = 'ALERT: %s' % content
    msg['From'] = "<from-email>"  #ex : from@gmail.com
    msg['To'] = "<to-email>" #ex : to@gmail.com
    print("sending email")

    #need to configure SMTP server. Can use gmail account for configuring SMTP server
    s = smtplib.SMTP('mail.gmail.com',26)
    s.set_debuglevel(True)
  # s.esmtp_features['auth'] = 'LOGIN PLAIN'
    s.login("<e-mail id>", "<password>") #login credentials for your SMTP server (beware that you are using password in plain-text)
    
    s.sendmail("<e-mail id>", "<to>", msg.as_string())
    s.quit()
    
    
