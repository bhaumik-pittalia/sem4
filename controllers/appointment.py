from flask import Blueprint
from flask import render_template,request,redirect
from google.appengine.ext import ndb
from models import Schedule,Appointment,Resource
from google.appengine.api.mail import EmailMessage 
import datetime,time
import urllib
import urllib2 

app = Blueprint('appointment',__name__,template_folder = 'templates')
app.debug = True

resource_id = None 
@app.route('/appointment/schedule/<d>/<m>/<y>/<dy>')
@app.route('/appointment/schedule/<resource>')
def user_appointment(resource=None,d=None,m=None,y=None,dy=None):
    day_name = ['sunday','monday','tuesday','wednesday','thursday','frieday','saturday']
    day = None
    if dy:
        day = day_name[int(dy)]
    global resource_id
    if resource:
        resource = ndb.Key(urlsafe=resource).get()
        resource_id = resource
    appointment = None
    appointment_times = []
    selected_date = None
    if m:
        month = ['January','February','March','April','May','June','July','August','September','October','November','December'].index(m)
        selected_date = datetime.date(int(y),month + 1,int(d))
        appointment = Appointment.query(Appointment.resource==resource_id.key).filter(Appointment.date==selected_date).fetch()
        for appointment in appointment:
            appointment_times.append(appointment.time_from)
    schedule = Schedule.query(Schedule.resource == resource_id.key).filter(Schedule.day == day).order(Schedule.time_from).fetch()
    monday = Schedule.query(Schedule.resource == resource_id.key).filter(Schedule.day == "monday").get()
    tuesday = Schedule.query(Schedule.resource == resource_id.key).filter(Schedule.day == "tuesday").get()
    wednesday = Schedule.query(Schedule.resource == resource_id.key).filter(Schedule.day == "wednesday").get()
    thursday = Schedule.query(Schedule.resource == resource_id.key).filter(Schedule.day == "thursday").get()
    frieday = Schedule.query(Schedule.resource == resource_id.key).filter(Schedule.day == "frieday").get()
    saturday = Schedule.query(Schedule.resource == resource_id.key).filter(Schedule.day == "saturday").get()
    return render_template("appointment-schedule.html",
                            d=d,m=m,y=y,day=day,
                            schedule = schedule,
                            resource = resource_id,
                            appointment = appointment,
                            monday=monday,
                            tuesday=tuesday,
                            wednesday=wednesday,
                            thursday=thursday,
                            frieday=frieday,
                            saturday=saturday,
                            appointment_times = appointment_times)

@app.context_processor
def utility():
    def convert12(time):
        time = datetime.datetime.strptime(str(time),"%H:%M:%S")
        return time.strftime("%I:%M %p")
    return dict(convert12=convert12)

@app.route('/user-info/<d>/<m>/<y>/<resource>/<schedule>')
def user_info(d=None,m=None,y=None,resource=None,schedule=None):
    resource = ndb.Key(urlsafe=resource).get()
    schedule = ndb.Key(urlsafe=schedule).get()
    return render_template("user_info.html",d=d,m=m,y=y,resource=resource,schedule=schedule)

@app.route('/appointment/user',methods=['POST'])
def appointment_save():
    appointment = Appointment()
    resource = Resource()
    month = ['January','February','March','April','May','June','July','August','September','October','November','December'].index(request.form.get('month'))

    resource = resource.browse(request.form.get('resource'))
    schedule = ndb.Key(urlsafe=request.form.get('schedule')).get()
    appointment.resource = resource.key
    appointment.date = datetime.date(int(request.form.get('year')),month + 1,int(request.form.get('date')))
    appointment.time_from = schedule.time_from 
    appointment.time_to = schedule.time_to
    appointment.name = request.form.get('name')
    appointment.phone = int(request.form.get('phone'))
    appointment.email = request.form.get('email')
    appointment.put()
    time.sleep(3)
    appointment = Appointment.query(Appointment.date == datetime.date(int(request.form.get('year')),month + 1,int(request.form.get('date')))).filter(Appointment.resource==resource.key,Appointment.time_from==schedule.time_from,Appointment.time_to==schedule.time_to).get()
    body = render_template("confirmation_email.html",resource=resource,appointment=appointment,link=request.headers['host'] + "/appointment/view/"+appointment.key.urlsafe())
    subject = "Appointment confirmed successfully!!"
    send_email("anything@appointment-152208.appspotmail.com",request.form.get('email'),subject,body)
    values = {
    'authkey' : "279201AURBFWjn3l5cf2082c",
    'mobiles' : request.form.get('phone'),
    'message' : "your appointment is comfirmed for "+resource.name+", please check your email for more detail.",
    'sender' : "611332",
    'route' : "default"
    }
    url = "http://api.msg91.com/api/sendhttp.php" # API URL
    postdata = urllib.urlencode(values) # URL encoding the data here.
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    output = response.read() # Get Response
    print output # Print Response

    return redirect('/appointment/view/'+appointment.key.urlsafe())

def send_email(email_from,email_to, subject, body):
    message = EmailMessage()
    message.sender = email_from
    message.to = [email_to]
    message.subject = subject
    message._add_body('text/html', body)
    message.check_initialized()
    message.send()

@app.route('/appointment/view/<key>')
def view_appointment(key=None):
    appointment = ndb.Key(urlsafe=key).get()
    resource = None
    if appointment:
        resource = Resource.query(Resource.key==appointment.resource).get()
        return render_template("confirmation.html",appointment=appointment,resource=resource)
    else:
        return render_template("nofound.html")

@app.context_processor
def utility():
    def convert12(time):
        time = datetime.datetime.strptime(str(time),"%H:%M:%S")
        return time.strftime("%I:%M %p")
    return dict(convert12=convert12)

@app.route('/appointment/cancel/<key>')
def cancel(key=None):
    ndb.Key(urlsafe=key).delete()
    return render_template("cancel_appointment.html")

@app.route('/appointment/reschedule/<resource>/<appointment>')
def reschedule(resource=None,appointment=None):
    ndb.Key(urlsafe=appointment).delete()
    return redirect('/appointment/schedule/'+resource)