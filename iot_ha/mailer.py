import sys
import os
import smtplib
import camera
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os.path

email = 'iothomeauto@gmail.com'
password = 'helloworld1'

def notify_with_image(reciever, subject, messageText):

    print 'Composing email with attachment...'
    img_data = open('captured/test.jpg', 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = reciever
    msg['Text'] =  messageText
    text = MIMEText(messageText)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename('test.jpg'))
    msg.attach(image)
    
    print 'Starting SMTP...'
    mail = smtplib.SMTP('smtp.gmail.com:587')
    mail.ehlo()
    print 'Starting TLS...'
    mail.starttls()
    print 'Logging in...'
    mail.login(email, password)
    print 'Sending email to ' + reciever + '... '
    mail.sendmail('iothomeauto@gmail.com', reciever, msg.as_string())
    mail.close()
    print 'email sent.'

if __name__ == '__main__':

    per = camera.identify()
    sub = 'IoT Notification'
    msg = 'Camera detected the presence of someone.\nPossible identity: ' + per
    print 'Possible Identity: ' + per
    # notify_with_image('tarek.elsherif9@gmail.com', sub, msg)

