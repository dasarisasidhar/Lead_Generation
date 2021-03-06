"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
import json
import requests
import time
import googlemaps 
import config
import os
import jwt
import pandas as pd
from Lead_generation import app
from Lead_generation import db
from flask import render_template
from flask import request
from flask import session
from flask import send_file
from flask import g
from flask import redirect
from flask import url_for
import googlemaps 

gmaps = googlemaps.Client(key = "AIzaSyCNTQTKtive3OCEaN6081u8GEEM1andX-I")
#config.dev_config.maps_key
jwt_key = config.dev_config.jwt_key
app.secret_key = config.dev_config.secret_key

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
    data = search_query(details["q"])
    return render_template(
        'search_for_leads.html',
        title='search Page',
        year=datetime.now().year,
        data = data)

@app.route('/search_for_leads')
def search_for_leads():
    return render_template(
        'search_for_leads.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/download')
def download():
    current_path = os.getcwd()
    file_name = "data.csv"
    file  = current_path + "\\Lead_generation\\static\\csv\\" + file_name
    return send_file(file, as_attachment=True)



def search_query(query):
    try:
        places_data = gmaps.places(query=str(query))
        details = list()
        for i in places_data["results"]:
            ref = i["reference"]
            data = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?placeid={ref}&key=AIzaSyD-tPkY3tKX0C9qraCTLdHEB_rZ9QqH9GI')
            data = data.json()
            print(data)
            print("--------------------------------------------------------")
            data = data["result"]
            print(results)
            details.append(i["name"] ,data["formatted_phone_number"], "email", "web address")  
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

@app.route('/create_user')
def create_user():
    if g.admin:
        return render_template(
                'admin/create_user.html',
                title='create agent',
                year=datetime.now().year,
            )
    else:
        return render_template(
        'login.html',
        title='login',
        year=datetime.now().year,
        error = "Please login as admin user to access this page"
    )
    
@app.route('/create_user', methods = ["POST"])
def creating_user():
    """create agent."""
    if g.admin:
        details = dict(request.form)
        if (len(details["name"])>3  and len(details["pswd"])>4, len(details["email"])>4  and
            db.user.create_user(details) == True):
            return render_template(
                'admin/search_for_leads.html',
                title='upload detail',
                year=datetime.now().year,
                )
        else:
            return redirect(url_for('create_user'))
    else:
        return render_template(
        'login.html',
        title='login',
        year=datetime.now().year,
        error = "Please login as admin user to access this page"
    )


@app.route('/login', methods = ["POST"])
def login_details():
    """verify login."""
    details = dict(request.form)
    session.pop("user", None)
    if(len(details["id"])> 4 and len(details["pswd"])>4):
        admin_details = db.admin.check_login(details)
        if admin_details == True:
            payload= {"admin_id" : details["id"],
                      'iat': datetime.utcnow(),
                      'exp': datetime.utcnow()+timedelta(days = 2)}
            session['admin'] = jwt.encode(payload, jwt_key, algorithm = 'HS256')
            return render_template(
                'admin/search_for_leads.html',
                title='upload detail',
                year=datetime.now().year,
                )  
    
        elif admin_details == False:
            error = "error in login details"

        user_details = db.user.check_login(details)
        if user_details == True:
            payload= {"user_id" : details["id"],
                      'iat': datetime.utcnow(),
                      'exp': datetime.utcnow()+timedelta(days = 1)}
            session['user'] = jwt.encode(payload, jwt_key, algorithm = 'HS256')
            return render_template(
                'search_for_leads.html',
                title='Search',
                year=datetime.now().year)
        else:
            error = user_details
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))