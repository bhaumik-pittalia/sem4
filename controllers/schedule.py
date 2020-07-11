from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from user import login
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Schedule,Resource
import datetime,time
app = Blueprint('schedule',__name__,template_folder = 'templates')
app.debug = True

@app.route('/schedule/<day>')
@app.route('/schedule')
def schedule():
    context = login()
    danger = False
    danger = request.args.get('danger')
    if danger:
        context.update({'danger':danger})
    resource = Resource.query(Resource.email==context.get('email')).get()
    schedule = None
    if resource:
        schedule = Schedule.query(Schedule.resource == resource.key).get()
    if schedule and resource:
        monday = Schedule.query(Schedule.day=="monday").filter(Schedule.resource==resource.key).order(Schedule.time_from).fetch()
        tuesday = Schedule.query(Schedule.day=="tuesday").filter(Schedule.resource==resource.key).order(Schedule.time_from).fetch()
        wednesday = Schedule.query(Schedule.day=="wednesday").filter(Schedule.resource==resource.key).order(Schedule.time_from).fetch()
        thursday = Schedule.query(Schedule.day=="thursday").filter(Schedule.resource==resource.key).order(Schedule.time_from).fetch()
        frieday = Schedule.query(Schedule.day=="frieday").filter(Schedule.resource==resource.key).order(Schedule.time_from).fetch()
        saturday = Schedule.query(Schedule.day=="saturday").filter(Schedule.resource==resource.key).order(Schedule.time_from).fetch()
        return render_template('schedule.html',
                            danger = danger,
                            context = context,
                            resource = resource,
                            monday=monday,
                            tuesday=tuesday,
                            wednesday=wednesday,
                            thursday=thursday,
                            frieday=frieday,
                            saturday=saturday)
    else:
        return render_template('schedule.html',
                            danger = danger,
                            context = context,
                            resource = resource)

@app.route('/schedule/drop/<schedule_drop>')
def drop_schedule(schedule_drop=None):
    if schedule_drop:
        ndb.Key(urlsafe=schedule_drop).delete()
    return redirect('/schedule')
    
@app.route('/delete_slots',methods=['Post'])
def delete_slots():
    monday = tuesday = wednesday = thursday = frieday = saturday = []
    if request.form.getlist('monday'):
        monday = request.form.getlist('monday')
        for key in monday:
            ndb.Key(urlsafe=key).delete()

    if request.form.getlist('tuesday'):
        tuesday = request.form.getlist('tuesday')
        for key in tuesday:
            ndb.Key(urlsafe=key).delete()
    
    if request.form.getlist('wednesday'):
        wednesday = request.form.getlist('wednesday')
        for key in wednesday:
            ndb.Key(urlsafe=key).delete()

    if request.form.getlist('thursday'):
        thursday = request.form.getlist('thursday')
        for key in thursday:
            ndb.Key(urlsafe=key).delete()

    if request.form.getlist('frieday'):
        frieday = request.form.getlist('frieday')
        for key in frieday:
            ndb.Key(urlsafe=key).delete()

    if request.form.getlist('saturday'):
        saturday = request.form.getlist('saturday')
        for key in saturday:
            ndb.Key(urlsafe=key).delete()

    return redirect('/schedule')

@app.route('/schedule/time',methods=['POST'])
def shedule_time():
    resource = Resource()
    resource = resource.browse(request.form.get('resource_id'))
    if check_exists(request.form.get('time_from_hour')+":"+request.form.get('time_from_minute')+":00 "+request.form.get('time_from_period'),resource):
        return redirect('/schedule?danger=Already exists')
    else:
        time_from_hour = int(request.form.get('time_from_hour'))
        time_from_minute = int(request.form.get('time_from_minute'))
        time_from_period =request.form.get('time_from_period')
        time_to_hour = int(request.form.get('time_to_hour'))
        time_to_minute = int(request.form.get('time_to_minute'))
        time_to_period = request.form.get('time_to_period')
        time_slot = int(request.form.get('time_slot'))
        time_from = None
        time_to = None
        proceed = 0
        if time_slot > 0:
            while proceed == 0:
                schedule = Schedule()
                schedule.resource = resource.key
                schedule.day = request.form.get('day') 
                time_to_min = time_from_minute + time_slot
                time_to_hr = time_from_hour
                time_to_per = time_from_period
                if time_to_hr == 11 and time_to_min >= 60:
                    if time_to_per == "am":
                        time_to_per = "pm"
                    else:
                        time_to_per = "am"
                if time_to_min >= 60:
                    time_to_min -= 60
                    time_to_hr += 1
                if time_to_hr > 12:
                    time_to_hr = 1 
                if time_from_hour == time_to_hour and time_from_period == time_to_period:
                    if time_from_minute >= time_to_minute:
                        proceed = 1
                    else:
                        if not check_exists(str(time_from_hour)+":"+str(time_from_minute)+":00 "+time_from_period,resource):
                            schedule.time_from = get_time(str(time_from_hour)+":"+str(time_from_minute)+":00 "+time_from_period)
                            schedule.time_to = get_time(str(time_to_hr)+":"+str(time_to_min)+":00 "+time_to_per)
                            schedule.put()
                        time_from_hour = time_to_hr
                        time_from_minute = time_to_min
                else:
                    if not check_exists(str(time_from_hour)+":"+str(time_from_minute)+":00 "+time_from_period,resource):
                        schedule.time_from = get_time(str(time_from_hour)+":"+str(time_from_minute)+":00 "+time_from_period)
                        schedule.time_to = get_time(str(time_to_hr)+":"+str(time_to_min)+":00 "+time_to_per)
                        schedule.put()
                    time_from_hour = time_to_hr
                    time_from_minute = time_to_min
                    time_from_period = time_to_per
        return redirect('/schedule')

def convert24(time):
    if time[-2:] == "am" and time[:2] == "12":
        return "00" + time[2:-2]
    elif time[-2:] == "am": 
        if time[1] == ":":
            return "0" + time[:-2]
        else:
            return time[:-2] 
    elif time[-2:] == "pm" and time[:2] == "12": 
        return time[:-2] 
    else:
        if time[1]==":":
            time = "0" + time
        return str(int(time[:2]) + 12) + time[2:8]
    
def get_time(time):
    if time[1:2] == ":" and time[3:4] == ":":
        time = time[:2] + "0" + time[2:]
    elif time[2:3] == ":" and time[4:5] == ":":
        time = time[:3] + "0" + time[3:]
    time = convert24(time)
    return datetime.time(int(time[:2]),int(time[3:5]),int(time[6:]))

@app.context_processor
def utility():
    def convert12(time):
        time = datetime.datetime.strptime(str(time),"%H:%M:%S")
        return time.strftime("%I:%M %p")
    return dict(convert12=convert12)

def check_exists(time,resource):
    schedule = Schedule()
    time = get_time(time)
    schedule = schedule.query(Schedule.day==request.form.get('day')).filter(Schedule.resource == resource.key,Schedule.time_from==time).fetch()
    if schedule:
        return True
    else:
        return False

@app.route('/week/schedule/<resource_id>')
def week_schedule(resource_id=None):
    day_name = ['monday','tuesday','wednesday','thursday','frieday','saturday']
    for day in day_name:
        resource = Resource()
        resource = resource.browse(resource_id)
        time_from_hour = 9
        time_from_minute = 00
        time_from_period = 'am'
        time_to_hour = 8
        time_to_minute = 00
        time_to_period = 'pm'
        time_slot = 60
        time_from = None
        time_to = None
        proceed = 0
        if time_slot > 0:
            while proceed == 0:
                schedule = Schedule()
                schedule.resource = resource.key
                schedule.day = day 
                time_to_min = time_from_minute + time_slot
                time_to_hr = time_from_hour
                time_to_per = time_from_period
                if time_to_hr == 11 and time_to_min >= 60:
                    if time_to_per == "am":
                        time_to_per = "pm"
                    else:
                        time_to_per = "am"
                if time_to_min >= 60:
                    time_to_min -= 60
                    time_to_hr += 1
                if time_to_hr > 12:
                    time_to_hr = 1 
                if time_from_hour == time_to_hour and time_from_period == time_to_period:
                    if time_from_minute >= time_to_minute:
                        proceed = 1
                    else:
                        schedule.time_from = get_time(str(time_from_hour)+":"+str(time_from_minute)+":00 "+time_from_period)
                        schedule.time_to = get_time(str(time_to_hr)+":"+str(time_to_min)+":00 "+time_to_per)
                        schedule.put()
                        time_from_hour = time_to_hr
                        time_from_minute = time_to_min
                else:
                    schedule.time_from = get_time(str(time_from_hour)+":"+str(time_from_minute)+":00 "+time_from_period)
                    schedule.time_to = get_time(str(time_to_hr)+":"+str(time_to_min)+":00 "+time_to_per)
                    schedule.put()
                    time_from_hour = time_to_hr
                    time_from_minute = time_to_min
                    time_from_period = time_to_per
    return redirect('/schedule')