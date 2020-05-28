'''

server = 'smtp.mail.ru'
user = 'sv_borisov03@mail.ru'
password = 'eyeshot2003'

recipients = ['sv_borisov03@mail.ru', 'v_s_borisov@rambler.ru']
sender = 'sv_borisov03@mail.ru'
subject = 'Рассылка'
text = 'ПОКА!'
html = ''

# filepath = "/var/log/maillog"
# basename = os.path.basename(filepath)
# filesize = os.path.getsize(filepath)

msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = 'Python script <' + sender + '>'
msg['To'] = ', '.join(recipients)
msg['Reply-To'] = sender
msg['Return-Path'] = sender
msg['X-Mailer'] = 'Python/' + (python_version())

part_text = MIMEText(text, 'plain')
part_html = MIMEText(html, 'html')
#part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
# part_file.set_payload(open(filepath, "rb").read())
# part_file.add_header('Content-Description', basename)
# part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
#encoders.encode_base64(part_file)

msg.attach(part_text)
msg.attach(part_html)
#msg.attach(part_file)

mail = smtplib.SMTP_SSL(server)
mail.login(user, password)
mail.sendmail(sender, recipients, msg.as_string())
mail.quit()'''

from flask import Flask, render_template, redirect, request, make_response, jsonify
from data import db_session
from data.users import Emails
from forms.write_messange import SendMessage
from forms.add import AddEmail
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version


application = Flask(__name__)
application.config.update(
    JSON_AS_ASCII=False
)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/baseDate.sqlite")


@application.route('/', methods=['POST', 'GET'])
def main_page():

    param = {}

    param['title'] = 'Главная страница'

    session = db_session.create_session()

    emails = session.query(Emails).all()
    param['emails'] = emails

    form = SendMessage()
    if form.validate_on_submit():
        server = 'smtp.mail.ru'
        user = 'sv_borisov03@mail.ru'
        password = 'eyeshot2003'

        recipients = [x.email for x in session.query(Emails).all()]
        sender = 'sv_borisov03@mail.ru'
        subject = 'Рассылка'
        if request.form['type'] == 'html':
            text = ''
            html = request.form['text']

            # filepath = "/var/log/maillog"
            # basename = os.path.basename(filepath)
            # filesize = os.path.getsize(filepath)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = 'Python script <' + sender + '>'
            msg['To'] = ', '.join(recipients)
            msg['Reply-To'] = sender
            msg['Return-Path'] = sender
            msg['X-Mailer'] = 'Python/' + (python_version())

            part_text = MIMEText(text, 'plain')
            part_html = MIMEText(html, 'html')
            # part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
            # part_file.set_payload(open(filepath, "rb").read())
            # part_file.add_header('Content-Description', basename)
            # part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
            # encoders.encode_base64(part_file)

            msg.attach(part_text)
            msg.attach(part_html)
            # msg.attach(part_file)

            mail = smtplib.SMTP_SSL(server)
            mail.login(user, password)
            mail.sendmail(sender, recipients, msg.as_string())
            mail.quit()
        else:
            text = request.form['text']
            html = '''
                    <!DOCTYPE html>
                        <html lang="en">
                            <head>
                            </head>
                            <body>
                                <p>''' + text + '''</p>
                            </body>         
                   '''

            # filepath = "/var/log/maillog"
            # basename = os.path.basename(filepath)
            # filesize = os.path.getsize(filepath)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = 'Python script <' + sender + '>'
            msg['To'] = ', '.join(recipients)
            msg['Reply-To'] = sender
            msg['Return-Path'] = sender
            msg['X-Mailer'] = 'Python/' + (python_version())

            part_text = MIMEText(text, 'plain')
            part_html = MIMEText(html, 'html')
            # part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
            # part_file.set_payload(open(filepath, "rb").read())
            # part_file.add_header('Content-Description', basename)
            # part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
            # encoders.encode_base64(part_file)

            msg.attach(part_text)
            msg.attach(part_html)
            # msg.attach(part_file)

            mail = smtplib.SMTP_SSL(server)
            mail.login(user, password)
            mail.sendmail(sender, recipients, msg.as_string())
            mail.quit()
        return redirect('/')
    return render_template('index.html', **param, form=form)


@application.route('/add', methods=['POST', 'GET'])
def add():

    param = {}

    param['title'] = 'Главная страница'

    session = db_session.create_session()

    form = AddEmail()
    if form.validate_on_submit():
        email = Emails()
        email.email = request.form['email']
        session.add(email)
        session.commit()
        return redirect('/')

    return render_template('add.html', **param, form=form)

#application.run()
