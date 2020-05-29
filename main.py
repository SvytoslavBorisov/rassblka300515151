from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.emails import Emails
from data.users import User
from data.groups import Group
from forms.write_messange import SendMessage
from forms.add import AddEmail
from forms.register import RegisterForm
from forms.login import LoginForm
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from platform import python_version


application = Flask(__name__)
application.config.update(
    JSON_AS_ASCII=False
)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/baseDate.sqlite")
login_manager = LoginManager()
login_manager.init_app(application)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@application.route('/login', methods=['GET', 'POST'])
def login():

    session = db_session.create_session()

    param = {}

    param['title'] = 'Вход'

    param['styles'] = os.listdir('static/css/styleForLogin/')
    param['path_for_style'] = '/static/css/styleForLogin/'

    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, **param)
    return render_template('login.html', form=form, **param)


@application.route('/', methods=['POST', 'GET'])
def main_page():

    if current_user.is_authenticated:
        param = {}

        session = db_session.create_session()

        emails = session.query(Emails).all()
        param['emails'] = emails

        groups = session.query(Group).filter(current_user.id == Group.admin).all()

        param['groups'] = []
        param['groups_title'] = []
        param['groups_id'] = []
        for group in groups:
            param['groups'].append([])
            param['groups_title'].append(group.title)
            param['groups_id'].append(group.id)
            for member in str(group.members).split():
                param['groups'][-1].append([session.query(Emails).filter(int(member) == Emails.id).first(), group.id])

        param['title'] = 'Главная страница'

        param['styles'] = os.listdir('static/css/styleForSendMessage/')
        param['path_for_style'] = '/static/css/styleForSendMessage/'

        if request.method == 'POST':
            server = 'smtp.mail.ru'

            group = request.form['send_message'].split("'")[1]

            user = current_user.email
            password = current_user.password_for_email

            temp_recipients = [x for x in str(session.query(Group).filter(Group.title == group, Group.admin == current_user.id).first().members).split()]
            recipients = []
            for x in temp_recipients:
                recipients.append(session.query(Emails).filter(Emails.id == int(x)).first().email)
            sender = user
            subject = 'Рассылка'
            if request.form['type_message'] == 'html':
                text = ''
                html = request.form['text_message']

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
            else:
                text = request.form['text_message']
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
            if request.files.get('file_message'):
                img = MIMEImage(request.files['file_message'].read())
                msg.attach(img)

            msg.attach(part_text)
            msg.attach(part_html)
            # msg.attach(part_file)

            mail = smtplib.SMTP_SSL(server)
            mail.login(user, password)
            mail.sendmail(sender, recipients, msg.as_string())
            mail.quit()
            return redirect('/')

        return render_template('send_message.html', **param)
    else:
        return redirect('/login')


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

    return render_template('add_to.html', **param, form=form)


@application.route('/user_info', methods=['POST', 'GET'])
def user_info():
    session = db_session.create_session()

    param = {}

    param['title'] = 'Регистрация'

    param['styles'] = os.listdir('static/css/styleForUserInfo/')
    param['path_for_style'] = '/static/css/styleForUserInfo/'

    if current_user.is_authenticated:
        if request.method == 'POST':
            if request.form.get('send'):
                user = session.query(User).filter(current_user.id == User.id).first()
                user.email = request.form['email']
                user.set_password_for_email(request.form['password'])
                session.commit()
            elif request.form.get('add_group'):
                group = Group()
                group.members = []
                all_emails = {x.email: x.id for x in session.query(Emails).all()}
                for email in request.form['members_group'].split():
                    if email in set(all_emails.keys()):
                        if email in set(group.members):
                            pass
                        else:
                            group.members.append(all_emails[email])
                    else:
                        temp_email = Emails()
                        temp_email.email = email
                        session.add(temp_email)
                        session.commit()
                        group.members.append(temp_email.id)
                group.members = ' '.join([str(x) for x in group.members])
                group.title = request.form['title_group']
                group.admin = current_user.id
                session.add(group)
                session.commit()
            else:
                temp = request.form['del_or_add_group'].split('_')
                if temp[0] == 'del':
                    group = session.query(Group).filter(int(temp[2]) == Group.id).first()
                    data = str(group.members).split()
                    data.remove(temp[1])
                    group.members = ' '.join(data)
                    session.commit()
                elif temp[0] == 'add':
                    group = session.query(Group).filter(int(temp[1]) == Group.id).first()
                    all_emails = {x.email: x.id for x in session.query(Emails).all()}
                    group.members = [x for x in str(group.members).split()]
                    for email in request.form['members_group'].split():
                        if email in set(all_emails.keys()):
                            if str(all_emails[email]) in set(group.members):
                                pass
                            else:
                                group.members.append(all_emails[email])
                        else:
                            temp_email = Emails()
                            temp_email.email = email
                            session.add(temp_email)
                            session.commit()
                            group.members.append(temp_email.id)
                    group.members = ' '.join([str(x) for x in group.members])
                    session.commit()
            return redirect('/user_info')
        else:
            groups = session.query(Group).filter(current_user.id == Group.admin).all()

            param['groups'] = []
            param['groups_title'] = []
            param['groups_id'] = []
            for group in groups:
                param['groups'].append([])
                param['groups_title'].append(group.title)
                param['groups_id'].append(group.id)
                for member in str(group.members).split():
                    param['groups'][-1].append([session.query(Emails).filter(int(member) == Emails.id).first(), group.id])

            return render_template('user_info.html', **param)
    else:
        return redirect('/login')


@application.route('/register', methods=['POST', 'GET'])
def register():

    session = db_session.create_session()

    param = {}

    param['title'] = 'Регистрация'

    param['styles'] = os.listdir('static/css/styleForRegister/')
    param['path_for_style'] = '/static/css/styleForRegister/'

    form = RegisterForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.login == form.login.data).first()
        if user:
            return render_template('register.html',
                                   message="Пользователь с такой почтой уже есть",
                                   form=form, **param)
        else:
            user = session.query(User).filter(User.name == form.name.data).first()
            if user:
                return render_template('register.html',
                                       message="Пользователь с таким ником уже есть",
                                       form=form, **param)
            else:
                user = User()
                user.name = request.form['name']
                user.login = request.form['login']
                user.set_password(request.form['password'])
                session.add(user)
                session.commit()
                session.commit()
                login_user(user)

                return redirect('/user_info')

    return render_template('register.html', form=form, **param)


#application.run()