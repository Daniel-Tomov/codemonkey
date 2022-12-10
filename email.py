from email.message import EmailMessage
import smtplib


EMAIL_PASSWORD = 'Your password'
EMAIL_ADDRESS = 'Your email'
RECIEVER_ADDRESS = 'Your receiver'

verifyMessage = 'Click the button below to verify your account on Codemonkey. If you did not ask for this message, DO NOT CLICK ON THE LINK.'


msg = EmailMessage()
msg['Subject'] = 'New message from Codemonkey'
msg['From'] = EMAIL_ADDRESS
msg['To'] = RECIEVER_ADDRESS
msg.set_content(verifyMessage)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
  smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
  smtp.send_message(msg)