"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from get_top_results import app
from flask import request
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

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
    print(data)
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        data = data,
    )

chromeOptions = Options()
chromeOptions.add_argument("--headless")
# headless  kiosk

def get_data(query):
    try:
        browser = webdriver.Chrome('C:/Users/iad7kor/Documents/Sasi/chromedriver.exe', options = chromeOptions )
        browser.get("https://www.google.co.in/maps/")
        time.sleep(3)
        browser.find_element_by_id("searchboxinput").send_keys(str(query))
        browser.find_element_by_id("searchboxinput").send_keys(Keys.ENTER)
        time.sleep(5)
        data = browser.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div")
        html_code =BeautifulSoup(browser.page_source, 'lxml')
        #data_tag_code =   html_code.find_all("div", class_="section-layout section-scrollbox scrollable-y scrollable-show section-layout-flex-vertical")
        data_tag_code =   html_code.find_all("div", class_="section-result")
        #print(data_tag_code1)
        details = list()
        for i in data_tag_code:
            if(i["aria-label"]):
                details.append(i["aria-label"])

        return details

    except Exception as e:
            print(e)
            details = ["details not found"]
            return details
