from google.appengine.api import users

def login():
    user = link = False
    user = users.get_current_user()
    email = None
    if user:
        link = users.create_logout_url('/')
        user = users.User()
        email = user.email()
    else:
        link = users.create_login_url('/')
    return{
        'url':link,
        'user':user,
        'email':email 
    }