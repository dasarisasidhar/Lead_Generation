"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from get_top_results import app
from flask import request
import json
import requests
import time
from flask import send_file
import googlemaps 
from get_top_results import db


gmaps = googlemaps.Client(key = "AIzaSyCFUBzYLW1sVSF2Q8laM_Sbo9JhOKqYiU0")

@app.before_request
def before_request(): 
    g.user = None 
    g.admin = None
    if "user" in session:
        try:
            jwt.decode(session["user"], jwt_key, algorithms=['HS256'])
            g.user = session["user"]
        except jwt.ExpiredSignatureError:
            g.admin = False

    elif "admin" in session:
        try:
            jwt.decode(session["admin"], jwt_key, algorithms=['HS256'])
            g.admin = session["admin"]
        except jwt.ExpiredSignatureError:
            g.admin = False

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title = "Page Not Found"), 404

@app.route('/logout')
def logout():
    session.pop("admin", None)
    return render_template(
        'login.html',
        title='Home Page',
        year=datetime.now().year,
        message = "logged out successfully"
        )

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/search', methods = ["POST"])
def search():
    details = dict(request.form)
    #data = get_details(details["q"])
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        data = data,
    )

@app.route('/download')
def download():
    data  = ["a", "b"]
    df = pd.DataFrame(data)
    return send_file(df.to_csv(), as_attachment=True)

def get_data(query):
    try:
        pass
         
    except Exception as e:
            print(e)
            details = ["details not found"]
            return details


def get_details(q):
    try:
        places_data = gmaps.places(query=str(q))
        details = list()
        for i in places_data["results"]:
            ref = i["reference"]
            data = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?placeid={ref}&key=AIzaSyCFUBzYLW1sVSF2Q8laM_Sbo9JhOKqYiU0')
            data = data.json()
            data = data["result"]
            details.append(i["name"] ,data["formatted_phone_number"])  
            break
        return details
    except Exception as e:
            print(e)
            details = ["details not found"]
            return details


@app.route('/login')
def login():
    """Renders the login page."""
    return render_template(
        'login.html',
        title='login',
        year=datetime.now().year
    )

@app.route('/login', methods = ["POST"])
def login_details():
    """verify login."""
    details = dict(request.form)
    session.pop("user", None)
    if(len(details["id"])> 4 and len(details["pswd"])>4):
        admin_details = db.check_login(details)
        if admin_details == True:
            payload= {"admin_id" : details["id"],
                      'iat': datetime.utcnow(),
                      'exp': datetime.utcnow()+timedelta(days = 2)}
            session['admin'] = jwt.encode(payload, jwt_key, algorithm = 'HS256')
            return render_template(
                'admin/upload_details.html',
                title='upload detail',
                year=datetime.now().year,
                )  
    
        elif admin_details == False:
            error = "error in login details"
        agent_details = db.check_login(details)
        if agent_details == True:
            payload= {"user_id" : details["id"],
                      'iat': datetime.utcnow(),
                      'exp': datetime.utcnow()+timedelta(days = 1)}
            session['user'] = jwt.encode(payload, jwt_key, algorithm = 'HS256')
            applications = agent.agent_control.get_applications(details["id"])
            return render_template(
                'agent/process.html',
                title='upload detail',
                year=datetime.now().year,
                applications = applications,
                response = status_response,
                agent = details["id"])
        else:
            error = agent_details
            return redirect(url_for('assign_agent'))
    else:
        return redirect(url_for('login'))