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


gmaps = googlemaps.Client(key = "AIzaSyCFUBzYLW1sVSF2Q8laM_Sbo9JhOKqYiU0")
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
    data = get_data(details["q"])
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


