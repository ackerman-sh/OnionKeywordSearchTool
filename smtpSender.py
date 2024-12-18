import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sender_email = "xyz@gmail.com" #change this
receiver_email = "xyz@gmail.com" #change this
subject = f"Results - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
body = "Please find attached the KeywordSearchResults.txt file."

smtp_server = "smtp.gmail.com"
smtp_port = 587

filename = "result/KeywordSearchResults.txt"
attachment = open(filename, "rb")

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))

part = MIMEBase("application", "octet-stream")
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename=KeywordSearchResults.txt")
msg.attach(part)

try:
    print(f"[STATUS] Sending mail to {receiver_email} ")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, "your app password") #change this
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("[SUCCESS] Email sent successfully.")
except Exception as e:
    print(f"[ERROR] Failed to send email: {e}")
