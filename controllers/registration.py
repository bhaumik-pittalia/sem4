from flask import render_template,request,jsonify
from flask import Flask,redirect
from flask import Blueprint
from user import login
from models import Resource
from google.appengine.ext import ndb

app = Blueprint('registration',__name__,template_folder='templates')
app.debug = True    
@app.route('/registration/save',methods=['POST'])
def save():
    context = login()
    resource = Resource()
    if request.form['id']:
        resource = ndb.Key(urlsafe=request.form['id']).get()
    resource.name = request.form['name']
    resource.email = context.get('email')
    resource.phone = int(request.form['phone'])
    resource.address = request.form['address']
    resource.put()
    if request.form['id']:
        return jsonify({'update':"successfully Updated"})
    else:
        return jsonify({'insert':"successfully inserted"})

@app.route('/update/profile')
@app.route('/registration')
def registration():
    context = login()
    resource = Resource.query(Resource.email == context.get('email')).get()
    return render_template('registration.html',resource = resource,context = context)