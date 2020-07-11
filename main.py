from flask import Flask,render_template
from flask import redirect
from user import login
from flask import jsonify
from controllers import registration,schedule,appointment_link,appointment
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Resource,Appointment
import datetime

app = Flask(__name__)
app.debug = True

app.register_blueprint(registration.app)
app.register_blueprint(schedule.app)
app.register_blueprint(appointment_link.app)
app.register_blueprint(appointment.app)
@app.route('/')
def index():
    context = login()
    user = context.get('user')
    url = context.get('url')
    if not user:
        return redirect(url)
    resource = False
    resource = Resource.query(Resource.email == context.get('email')).fetch()
    if not resource:
        return redirect('/registration')
    resource = Resource.query().fetch()
    logged_resource =Resource.query(Resource.email==context.get('email')).get() 
    next_appointment = Appointment.query(Appointment.resource == logged_resource.key).filter(Appointment.date>datetime.datetime.today()).order(Appointment.date).fetch()
    previous_appointment = Appointment.query(Appointment.resource == logged_resource.key).filter(Appointment.date<datetime.datetime.today()).order(Appointment.date).fetch() 
    today_appointment = Appointment.query(Appointment.resource == logged_resource.key).filter(Appointment.date==datetime.datetime.today()).order(Appointment.date).fetch()
    return render_template('index.html',context = context,today=today_appointment,next=next_appointment,previous=previous_appointment)

@app.context_processor
def utility():
    def convert12(time):
        time = datetime.datetime.strptime(str(time),"%H:%M:%S")
        return time.strftime("%I:%M %p")
    return dict(convert12=convert12)
