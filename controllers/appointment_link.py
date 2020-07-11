from flask import Flask
from flask import request
from flask import Blueprint
from flask import render_template,jsonify
from user import login
from models import Resource
from google.appengine.api.mail import EmailMessage

app = Blueprint('appointment_link',__name__,template_folder='templates')

@app.route('/appointment-link')
def appointment():
    context = login()
    link = request.headers['host'] + "/appointment/schedule/" 
    resource = Resource.query(Resource.email == context.get('email')).get()
    return render_template('appointment-link.html',context = context,link = link,resource = resource)

@app.route('/send-email',methods=['POST'])
def email():
    context = login()
    email = request.form['email']
    link = request.form['link']
    if email and link:
        subject = "Link for appointment"
        body = render_template("send_email.html",email=str(context.get('email')),link=link)
        resource = Resource.query(Resource.email == context.get('email')).get()
        send_email(str(context.get('email')),email,subject,body)
        return jsonify({'success':"Successfully sent email"})
    else:
        return jsonify({'fail':"Failed to sent email"})

def send_email(email_from,email_to, subject, body):
    message = EmailMessage()
    message.sender = email_from
    message.to = [email_to]
    message.subject = subject
    message._add_body('text/html', body)
    message.check_initialized()
    message.send()