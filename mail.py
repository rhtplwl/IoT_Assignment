import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_alert(sender, receiver, password, smtpserver, port ):
	smtp = smtplib.SMTP(smtpserver, port)
	smtp.ehlo()
	smtp.starttls();
	smtp.ehlo
	smtp.login(sender, password)
	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = receiver
	msg['Subject'] :'IoT Alert'

	body = "Your sensor is not running properly. Please Check!"
	msg.attach(MIMEText(body, 'plain'))
	text = msg.as_string()
	smtp.sendmail(sender, receiver,text)
	print("Alert Sent to " + receiver)
	smtp.close()